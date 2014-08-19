#!/usr/bin/env python
"""
Download raw data from online server and store it as
handwriting_datasets.pickle.
"""

import logging
import sys
import os
logging.basicConfig(format='%(asctime)s %(levelname)s %(message)s',
                    level=logging.DEBUG,
                    stream=sys.stdout)
import cPickle as pickle
import MySQLdb
import MySQLdb.cursors
from HandwrittenData import HandwrittenData
import time
import utils


def main(destination=os.path.join(utils.get_project_root(),
                                  "archive/datasets"),
         small_dataset=False):
    time_prefix = time.strftime("%Y-%m-%d-%H-%M")
    if small_dataset:
        filename = "%s-handwriting_datasets-small-raw.pickle" % time_prefix
    else:
        filename = "%s-handwriting_datasets-raw.pickle" % time_prefix
    destination_path = os.path.join(destination, filename)
    logging.info("Data will be written to '%s'" % destination_path)
    cfg = utils.get_database_configuration()
    mysql = cfg['mysql_online']
    connection = MySQLdb.connect(host=mysql['host'],
                                 user=mysql['user'],
                                 passwd=mysql['passwd'],
                                 db=mysql['db'],
                                 cursorclass=MySQLdb.cursors.DictCursor)
    cursor = connection.cursor()

    # Get all formulas that should get examined
    if small_dataset:
        sql = ("SELECT `id`, `formula_in_latex` FROM `wm_formula` "
               # only use the important symbol subset
               "WHERE `is_important` = 1 "
               "AND id != 1 "  # exclude trash class
               "AND id <= 81 "
               "ORDER BY `id` ASC")
    else:
        sql = ("SELECT `id`, `formula_in_latex` FROM `wm_formula` "
               # only use the important symbol subset
               "WHERE `is_important` = 1 "
               "AND id != 1 "  # exclude trash class
               "ORDER BY `id` ASC")
    cursor.execute(sql)
    formulas = cursor.fetchall()

    handwriting_datasets = []
    formula_id2latex = {}

    # Go through each formula and download every raw_data instance
    for formula in formulas:
        formula_id2latex[formula['id']] = formula['formula_in_latex']
        sql = ("SELECT `id`, `data`, `is_in_testset`, `wild_point_count`, "
               "`missing_line`, `user_id` "
               "FROM `wm_raw_draw_data` "
               "WHERE `accepted_formula_id` = %s" % str(formula['id']))
        cursor.execute(sql)
        raw_datasets = cursor.fetchall()
        logging.info("%s (%i)" % (formula['formula_in_latex'],
                                  len(raw_datasets)))
        for raw_data in raw_datasets:
            try:
                handwriting = HandwrittenData(raw_data['data'],
                                              formula['id'],
                                              raw_data['id'],
                                              formula['formula_in_latex'],
                                              raw_data['wild_point_count'],
                                              raw_data['missing_line'],
                                              raw_data['user_id'])
                handwriting_datasets.append({'handwriting': handwriting,
                                             'id': raw_data['id'],
                                             'formula_id': formula['id'],
                                             'formula_in_latex':
                                             formula['formula_in_latex'],
                                             'is_in_testset':
                                             raw_data['is_in_testset']
                                             })
            except Exception as e:
                logging.info("Raw data id: %s" % raw_data['id'])
                logging.info(e)
    pickle.dump({'handwriting_datasets': handwriting_datasets,
                 'formula_id2latex': formula_id2latex,
                 },
                open(destination_path, "wb"),
                2)


if __name__ == '__main__':
    PROJECT_ROOT = utils.get_project_root()
    archive_path = os.path.join(PROJECT_ROOT, "archive/datasets")
    from argparse import ArgumentParser, ArgumentDefaultsHelpFormatter
    parser = ArgumentParser(description=__doc__,
                            formatter_class=ArgumentDefaultsHelpFormatter)
    parser.add_argument("-d", "--destination", dest="destination",
                        default=archive_path,
                        help="where do write the handwriting_dataset.pickle",
                        type=lambda x: utils.is_valid_file(parser, x),
                        metavar="FOLDER")
    parser.add_argument("-s", "--small", dest="small",
                        action="store_true", default=False,
                        help=("should only a small dataset (with all capital "
                              "letters) be created?"))
    args = parser.parse_args()
    main(args.destination, args.small)

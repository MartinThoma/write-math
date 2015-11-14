#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
Add `is_in_testset` to raw_datasets in MySQL database, so that at least 10%
of the data online has the flag `is_in_testset`.
"""

import pymysql
import pymysql.cursors
import random
import math

# hwrt modules
from hwrt.handwritten_data import HandwrittenData
import hwrt.utils as utils
import hwrt.filter_dataset as filter_dataset


def main(mysql, symbol_yml_file):
    """Add testset flag to recordings in MySQL database."""
    connection = pymysql.connect(host=mysql['host'],
                                 user=mysql['user'],
                                 passwd=mysql['passwd'],
                                 db=mysql['db'],
                                 cursorclass=pymysql.cursors.DictCursor)
    cursor = connection.cursor()

    # Get IDs of symbols we want to create testset for
    metadata = filter_dataset.get_metadata()
    datasets = filter_dataset.get_symbol_ids(symbol_yml_file, metadata)

    for i, data in enumerate(datasets):
        fid, formula_in_latex = data['id'], data['formula_in_latex']
        print("%i: Create testset for %s (id: %i)..." % (i,
                                                         formula_in_latex,
                                                         fid))
        sql = ("SELECT `id`, `is_in_testset` FROM `wm_raw_draw_data` "
               "WHERE `accepted_formula_id` = %i" % fid)
        cursor.execute(sql)
        raw_datasets = cursor.fetchall()
        is_in_testset = 0
        raw_candidate_ids = []
        for raw_data in raw_datasets:
            if raw_data['is_in_testset'] == 1:
                is_in_testset += 1
            else:
                raw_candidate_ids.append(raw_data['id'])
        testset_ratio = 0.1
        testset_total = int(math.ceil(len(raw_datasets) * testset_ratio))
        remaining = testset_total - is_in_testset

        if remaining > 0:
            print(("\t%i in testset. "
                   "Add remaining %i datasets to testset...") %
                  (is_in_testset, remaining))
            add_new = random.sample(raw_candidate_ids, remaining)
            if len(add_new) < 20:
                for el in add_new:
                    print("\thttp://write-math.com/view/?raw_data_id=%i" % el)
            for rid in add_new:
                sql = ("UPDATE `wm_raw_draw_data` SET `is_in_testset`=1 "
                       "WHERE `id` = %i LIMIT 1") % rid
                cursor.execute(sql)
            connection.commit()


def get_parser():
    """Return the parser object for this script."""
    from argparse import ArgumentParser, ArgumentDefaultsHelpFormatter
    parser = ArgumentParser(description=__doc__,
                            formatter_class=ArgumentDefaultsHelpFormatter)
    parser.add_argument("-s", "--symbol",
                        dest="symbol_filename",
                        type=lambda x: utils.is_valid_file(parser, x),
                        required=True,
                        help="symbol yml file",
                        metavar="FILE")
    return parser


if __name__ == '__main__':
    args = get_parser().parse_args()
    cfg = utils.get_database_configuration()
    if 'mysql_online' in cfg:
        main(cfg['mysql_online'], args.symbol_filename)
    if 'mysql_local' in cfg:
        main(cfg['mysql_local'], args.symbol_filename)

#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""Find outliers in the dataset."""

import pymysql.cursors
from copy import deepcopy

# My modules
from hwrt import preprocessing
from hwrt import utils
from misc import HandwrittenDataM


def main(cfg, raw_data_start_id):
    """
    Parameters
    ----------
    cfg : dict
        Configuration
    raw_data_start_id : int
        Only check data with raw_data_id > raw_data_start_id
    """
    cfg = utils.get_database_configuration()
    mysql = cfg['mysql_online']
    connection = pymysql.connect(host=mysql['host'],
                                 user=mysql['user'],
                                 passwd=mysql['passwd'],
                                 db=mysql['db'],
                                 cursorclass=pymysql.cursors.DictCursor)
    cursor = connection.cursor()

    # Get formulas
    print("Get formulas")
    sql = ("SELECT `id`, `formula_in_latex` FROM `wm_formula` WHERE `id` > %s")
    cursor.execute(sql, (raw_data_start_id, ))
    formulas = cursor.fetchall()
    formulaid2latex = {}
    for el in formulas:
        formulaid2latex[el['id']] = el['formula_in_latex']

    preprocessing_queue = [preprocessing.ScaleAndShift(),
                           # preprocessing.Douglas_peucker(EPSILON=0.2),
                           # preprocessing.Space_evenly(number=100,
                           #                            kind='cubic')
                           ]

    checked_formulas = 0
    checked_raw_data_instances = 0

    for formula_id in formulaid2latex.keys():
        if formula_id == 1:
            # This formula id is for trash. No need to look at it.
            continue
        # Get data
        print("Get data for formula_id %i (%s)" % (formula_id,
                                                   formulaid2latex[formula_id])
              )
        sql = ("SELECT `id`, `data`, `accepted_formula_id`, "
               "`wild_point_count`, `missing_line`, `has_hook`, "
               "`has_too_long_line`, `is_image`, `administrator_edit`, "
               "`other_problem`, `has_interrupted_line` "
               "FROM  `wm_raw_draw_data` "
               "WHERE `accepted_formula_id` = %i "
               "ORDER BY `administrator_edit` DESC, "
               "`creation_date` ASC;") % formula_id
        cursor.execute(sql)
        raw_datasets = cursor.fetchall()
        print("Raw datasets: %i" % len(raw_datasets))
        checked_raw_data_instances += len(raw_datasets)
        checked_formulas += 1
        if len(raw_datasets) < 100:
            continue

        for i, data in enumerate(raw_datasets):
            if data['data'] == "[]":
                continue
            b = HandwrittenDataM(data['data'],
                                 data['accepted_formula_id'],
                                 data['wild_point_count'],
                                 data['missing_line'],
                                 data['has_hook'],
                                 data['has_too_long_line'],
                                 data['is_image'],
                                 data['other_problem'],
                                 data['has_interrupted_line'],
                                 data['id'],
                                 formulaid2latex[formula_id])
            b.preprocessing(preprocessing_queue)
            bs = deepcopy(b)
            bs.preprocessing([preprocessing.DotReduction(0.01)])
            if b != bs:
                before_pointcount = sum([len(line)
                                         for line in b.get_pointlist()])
                after_pointcount = sum([len(line)
                                        for line in bs.get_pointlist()])
                print("Reduced %i lines to %i lines." %
                      (len(b.get_pointlist()), len(bs.get_pointlist())))
                print("Reduced %i points to %i points." %
                      (before_pointcount, after_pointcount))
                if before_pointcount - after_pointcount > 2:
                    b.show()
                    bs.show()

        print("[Status] Checked formulas: %i of %i" % (checked_formulas,
                                                       len(formulaid2latex)))
        print("[Status] Checked raw_data_instances: %i" %
              checked_raw_data_instances)
    print("done")

if __name__ == '__main__':
    from argparse import ArgumentParser
    parser = ArgumentParser()
    # Add more options if you like
    parser.add_argument("-i", dest="i",
                        help="at which raw_data_id should it start?",
                        metavar="RAW_DATA_ID")
    args = parser.parse_args()
    cfg = utils.get_database_configuration()
    main(cfg, args.i)

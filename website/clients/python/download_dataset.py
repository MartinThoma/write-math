#!/usr/bin/env python
"""
Download raw data from online server and store it as
handwriting_datasets.pickle.
"""


import cPickle as pickle
import MySQLdb
import MySQLdb.cursors
import yaml
from HandwrittenData import HandwrittenData


def main(cfg):
    connection = MySQLdb.connect(host=cfg['mysql_online']['host'],
                                 user=cfg['mysql_online']['user'],
                                 passwd=cfg['mysql_online']['passwd'],
                                 db=cfg['mysql_online']['db'],
                                 cursorclass=MySQLdb.cursors.DictCursor)
    cursor = connection.cursor()

    # Get all formulas that should get examined
    sql = ("SELECT `id`, `formula_in_latex` FROM `wm_formula` "
           "WHERE `is_important` = 1 "  # only use the important symbol subset
           "ORDER BY `id` ASC")
    cursor.execute(sql)
    formulas = cursor.fetchall()

    handwriting_datasets = []
    formula_id2latex = {}

    # Go through each formula and download every raw_data instance
    for formula in formulas:
        formula_id2latex[formula['id']] = formula['formula_in_latex']
        sql = ("SELECT `id`, `data`, `is_in_testset` FROM `wm_raw_draw_data` "
               "WHERE `accepted_formula_id` = %s" % str(formula['id']))
        cursor.execute(sql)
        raw_datasets = cursor.fetchall()
        print("%s (%i)" % (formula['formula_in_latex'], len(raw_datasets)))
        for raw_data in raw_datasets:
            try:
                handwriting = HandwrittenData(raw_data['data'],
                                              formula['id'],
                                              raw_data['id']),
                handwriting_datasets.append({'handwriting': handwriting,
                                             'id': raw_data['id'],
                                             'formula_id': formula['id'],
                                             'formula_in_latex':
                                             formula['formula_in_latex'],
                                             'is_in_testset':
                                             raw_data['is_in_testset']
                                             })
            except Exception as e:
                print("Raw data id: %s" % raw_data['id'])
                print(e)

    pickle.dump({'handwriting_datasets': handwriting_datasets,
                 'formula_id2latex': formula_id2latex,
                 },
                open("handwriting_datasets.pickle", "wb"))

if __name__ == '__main__':
    with open("db.config.yml", 'r') as ymlfile:
        cfg = yaml.load(ymlfile)
    main(cfg)

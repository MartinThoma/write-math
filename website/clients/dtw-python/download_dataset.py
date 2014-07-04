#!/usr/bin/env python

import cPickle as pickle
import MySQLdb
import MySQLdb.cursors
from dbconfig import mysql
from HandwrittenData import HandwrittenData


def main():
    connection = MySQLdb.connect(host=mysql['host'],
                                 user=mysql['user'],
                                 passwd=mysql['passwd'],
                                 db=mysql['db'],
                                 cursorclass=MySQLdb.cursors.DictCursor)
    cursor = connection.cursor()

    # Download all datasets
    sql = "SELECT id, formula_in_latex FROM `wm_formula`"
    cursor.execute(sql)
    datasets = cursor.fetchall()

    handwriting_datasets = []
    formula_id2latex = {}

    for dataset in datasets:
        formula_id2latex[dataset['id']] = dataset['formula_in_latex']
        sql = ("SELECT id, data FROM `wm_raw_draw_data` "
               "WHERE `accepted_formula_id` = %s" % str(dataset['id']))
        cursor.execute(sql)
        raw_datasets = cursor.fetchall()
        print("%s (%i)" % (dataset['formula_in_latex'], len(raw_datasets)))
        for raw_data in raw_datasets:
            try:
                handwriting_datasets.append({'handwriting': HandwrittenData(raw_data['data']),
                                             'id': raw_data['id'],
                                             'formula_id': dataset['id'],
                                             'formula_in_latex': dataset['formula_in_latex']
                                             })
            except Exception as e:
                print("Raw data id: %s" % raw_data['id'])
                print(e)

    pickle.dump((handwriting_datasets, formula_id2latex),
                open("handwriting_datasets.pickle", "wb"))

if __name__ == '__main__':
    main()

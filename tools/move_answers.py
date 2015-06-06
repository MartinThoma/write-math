#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""Move answers from old `wm_raw_data2formula` to new `wm_partial_answer`

wm_raw_data2formula
-------------------
* id
* raw_data_id
* formula_id
* user_id

wm_partial_answer
-----------------
* id
* recording_id
* symbol_id
* user_id
* strokes
"""


import pymysql.cursors
import logging
import sys

import hwrt.utils
import hwrt.HandwrittenData

logging.basicConfig(format='%(asctime)s %(levelname)s %(message)s',
                    level=logging.DEBUG,
                    stream=sys.stdout)


def get_old_datasets(mysql):
    """
    Parameters
    ----------
    mysql : dict
        Connection information
    """
    connection = pymysql.connect(host=mysql['host'],
                                 user=mysql['user'],
                                 passwd=mysql['passwd'],
                                 db=mysql['db'],
                                 cursorclass=pymysql.cursors.DictCursor)
    cursor = connection.cursor()

    # Get the data
    sql = ("SELECT `wm_raw_data2formula`.`id`, `raw_data_id`, `formula_id`, "
           "`wm_raw_data2formula`.`user_id`, `data`, `accepted_formula_id` "
           "FROM `wm_raw_data2formula` "
           "JOIN `wm_raw_draw_data` ON "
           "(`wm_raw_data2formula`.`raw_data_id` = `wm_raw_draw_data`.`id`) "
           "ORDER BY `wm_raw_data2formula`.`id` ASC LIMIT 10000")
    cursor.execute(sql)
    datasets = cursor.fetchall()
    for d in datasets:
        stroke_count = len(hwrt.HandwrittenData.HandwrittenData(d['data']).get_pointlist())
        d['strokes'] = ','.join([str(el) for el in range(stroke_count)])
        del d['data']
    return datasets


def transfer(mysql, old_datasets):
    """
    Parameters
    ----------
    mysql : dict
        Connection information
    """
    connection = pymysql.connect(host=mysql['host'],
                                 user=mysql['user'],
                                 passwd=mysql['passwd'],
                                 db=mysql['db'],
                                 cursorclass=pymysql.cursors.DictCursor)
    cursor = connection.cursor()

    # Insert in wm_partial_answer
    for answer in old_datasets:
        logging.info("Move answer ID %s (raw data id %s)...",
                     answer['id'],
                     answer['raw_data_id'])
        try:
            sql = ("INSERT INTO `wm_partial_answer` "
                   "(`recording_id`, `symbol_id`, `user_id`, `strokes`, "
                   "`is_accepted`) "
                   "VALUES (%s, %s, %s, %s, %s);")
            is_accepted = False
            if answer['accepted_formula_id'] is not None:
                is_accepted = answer['accepted_formula_id'] == answer['formula_id']
            cursor.execute(sql, (answer['raw_data_id'],
                                 answer['formula_id'],
                                 answer['user_id'],
                                 answer['strokes'],
                                 is_accepted))
        except pymysql.err.IntegrityError:
            pass
        # connection is not autocommit by default. So you must commit to save
        # your changes.
        connection.commit()

        # Delete from wm_raw_data2formula
        sql = ("DELETE FROM `wm_raw_data2formula` WHERE `id` = %s LIMIT 1;")
        cursor.execute(sql, (answer['id']))
        connection.commit()


def main():
    cfg = hwrt.utils.get_database_configuration()
    mysql = cfg['mysql_online']
    old_datasets = get_old_datasets(mysql)
    transfer(mysql, old_datasets)


if __name__ == '__main__':
    main()

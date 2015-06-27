#!/usr/bin/env python

"""Find recordings where the symbol count does not match the segmentation."""

import sys
import logging
logging.basicConfig(level=logging.INFO,
                    stream=sys.stdout,
                    format='%(asctime)s %(levelname)s: %(message)s')
logger = logging.getLogger(__name__)

import json

# Database stuff
import pymysql
import pymysql.cursors

# My modules
from hwrt import utils


def main():
    cfg = utils.get_database_configuration()
    mysql = cfg['mysql_online']
    find_wrong_count(mysql)


def find_wrong_count(mysql):
    connection = pymysql.connect(host=mysql['host'],
                                 user=mysql['user'],
                                 passwd=mysql['passwd'],
                                 db=mysql['db'],
                                 cursorclass=pymysql.cursors.DictCursor)
    cursor = connection.cursor()
    offset = 0
    bucket_size = 100
    sql = ("SELECT COUNT(`id`) as `count` FROM `wm_raw_draw_data` "
           "WHERE `stroke_segmentable` = 1 AND `segmentation` IS NOT NULL "
           "AND `classifiable` = 1 AND accepted_formula_id != 1 ")
    cursor.execute(sql)
    recordings_total = int(cursor.fetchall()[0]['count'])
    logging.info("Recordings (total): %i", recordings_total)
    while offset < recordings_total:
        fixed = 0
        sql = ("SELECT `id`, `segmentation`, `nr_of_symbols`, "
               "`wild_point_count` "
               "FROM `wm_raw_draw_data` "
               "WHERE `stroke_segmentable` = 1 AND `segmentation` IS NOT NULL "
               "AND `classifiable` = 1 AND accepted_formula_id != 1 "
               "ORDER BY `id` LIMIT %i, %i" % (offset, bucket_size))
        cursor.execute(sql)
        recordings = cursor.fetchall()
        for recording in recordings:
            segmentation = json.loads(recording['segmentation'])
            nr_of_symbols = int(recording['nr_of_symbols'])
            wildpoints = int(recording['wild_point_count'])
            if nr_of_symbols != len(segmentation):
                # print(('http://www.martin-thoma.de/write-math/'
                #        'view/?raw_data_id=%i (should be %i)') %
                #       (recording['id'], len(segmentation)))
                fix_symbol_count(mysql,
                                 int(recording['id']),
                                 len(segmentation))
                fixed += 1
            elif nr_of_symbols - wildpoints <= 0:
                print(('http://www.martin-thoma.de/write-math/'
                       'view/?raw_data_id=%i (wildpoints wrong)') %
                      (recording['id']))
        offset += bucket_size
        logging.info('Offset: %i (fixed %i)', offset, fixed)


def fix_symbol_count(mysql, wid, correct_count):
    connection = pymysql.connect(host=mysql['host'],
                                 user=mysql['user'],
                                 passwd=mysql['passwd'],
                                 db=mysql['db'],
                                 cursorclass=pymysql.cursors.DictCursor)
    cursor = connection.cursor()
    sql = (("UPDATE `wm_raw_draw_data` "
            "SET `nr_of_symbols` = %i "
            "WHERE `wm_raw_draw_data`.`id` =%i "
            "LIMIT 1;") % (correct_count, wid))
    cursor.execute(sql)
    connection.commit()
    cursor.close()
    connection.close()

if __name__ == '__main__':
    main()

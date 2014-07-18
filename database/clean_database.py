#!/usr/bin/env python

from __future__ import print_function
import logging
import MySQLdb
import MySQLdb.cursors
from dbconfig import mysql_local

def clean(mysql):
    connection = MySQLdb.connect(host=mysql['host'],
                                 user=mysql['user'],
                                 passwd=mysql['passwd'],
                                 db=mysql['db'],
                                 cursorclass=MySQLdb.cursors.DictCursor)
    cursor = connection.cursor()

    sql = "SET foreign_key_checks = 0;DROP TABLE `wm_challenges`, `wm_dtw_worker_data`, `wm_flags`, `wm_formula`, `wm_formula2challenge`, `wm_formula_in_paper`, `wm_formula_svg_missing`, `wm_invalid_formula_requests`, `wm_languages`, `wm_papers`, `wm_raw_data2formula`, `wm_raw_draw_data`, `wm_renderings`, `wm_similarity`, `wm_users`, `wm_user_unknown_formula`, `wm_votes`, `wm_workers`, `wm_worker_answers`;SET foreign_key_checks = 1;"
    a = cursor.execute(sql)
    print(a)

if __name__ == '__main__':
    clean(mysql_local)
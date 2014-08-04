#!/usr/bin/env python
# -*- coding: utf-8 -*-

import yaml
# Database stuff
import MySQLdb
import MySQLdb.cursors


def update_data(sql, mysql_local, mysql_online):
    # Update local
    connection_local = MySQLdb.connect(host=mysql_local['host'],
                                       user=mysql_local['user'],
                                       passwd=mysql_local['passwd'],
                                       db=mysql_local['db'],
                                       cursorclass=MySQLdb.cursors.DictCursor)
    cursor_local = connection_local.cursor()
    cursor_local.execute(sql)
    connection_local.commit()
    cursor_local.close()
    connection_local.close()

    # Update online
    connection_online = MySQLdb.connect(host=mysql_online['host'],
                                        user=mysql_online['user'],
                                        passwd=mysql_online['passwd'],
                                        db=mysql_online['db'],
                                        cursorclass=MySQLdb.cursors.DictCursor)
    cursor_online = connection_online.cursor()
    cursor_online.execute(sql)
    connection_online.commit()
    cursor_online.close()
    connection_online.close()


def fix_wrong_json(raw_data, raw_data_id, mysql_local, mysql_online):
    # Take everything from the back until the first '}' appears
    i = -1
    while raw_data[i] != '}' and i > -len(raw_data):
        i -= 1
    fixed = raw_data[0:len(raw_data)+i+1] + "]]"
    # Put it in the database
    sql = ("UPDATE `wm_raw_draw_data` "
           "SET `data` = '%s' "
           "WHERE `wm_raw_draw_data`.`id` = %i LIMIT 1; " % (fixed,
                                                             raw_data_id))
    update_data(sql, mysql_local, mysql_online)
    print("Updated http://www.martin-thoma.de/write-math/view/?raw_data_id=%i"
          % raw_data_id)


def main(mysql_local, mysql_online):
    connection = MySQLdb.connect(host=mysql_local['host'],
                                 user=mysql_local['user'],
                                 passwd=mysql_local['passwd'],
                                 db=mysql_local['db'],
                                 cursorclass=MySQLdb.cursors.DictCursor)
    cursor = connection.cursor()

    print("Get data which is wrong...")
    sql = ("SELECT `id`, `data` FROM  `wm_raw_draw_data` "
           "WHERE  `data` NOT LIKE  '%]]'")
    cursor.execute(sql)
    wrong_raw_data = cursor.fetchall()
    print("Got %i datasets." % len(wrong_raw_data))
    for d in wrong_raw_data:
        if d['data'] == '[]':
            continue
        fix_wrong_json(d['data'], d['id'], mysql_local, mysql_online)


if __name__ == '__main__':
    from argparse import ArgumentParser, ArgumentDefaultsHelpFormatter
    parser = ArgumentParser(description=__doc__,
                            formatter_class=ArgumentDefaultsHelpFormatter)
    args = parser.parse_args()
    with open("db.config.yml", 'r') as ymlfile:
        cfg = yaml.load(ymlfile)
    main(cfg['mysql_local'], cfg['mysql_online'])

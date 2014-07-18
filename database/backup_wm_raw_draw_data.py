#!/usr/bin/env python

from __future__ import print_function
import MySQLdb
from dbconfig import mysql_online
import MySQLdb.cursors
import time


def main(mysql):
    pagesize = 2000
    print("Connect to database")
    connection = MySQLdb.connect(host=mysql['host'],
                                 user=mysql['user'],
                                 passwd=mysql['passwd'],
                                 db=mysql['db'],
                                 cursorclass=MySQLdb.cursors.DictCursor)
    cursor = connection.cursor()
    print("Get counter")
    sql = "SELECT COUNT( * ) AS counter FROM  `wm_raw_draw_data`"
    cursor.execute(sql)
    count = cursor.fetchone()['counter']
    print("Counter: %i" % count)

    datacounter = 0
    filecounter = 1
    f = open("wm_raw_draw_data_%i.sql" % filecounter, "w")

    # Speed up insertion
    f.write("LOCK TABLES wm_raw_draw_data WRITE;")

    for i in range(0, count, pagesize):
        start_time = time.time()
        sql = "SELECT * FROM  `wm_raw_draw_data` LIMIT %i, %i" % (i, pagesize)
        cursor.execute(sql)
        datasets = cursor.fetchall()
        for data in datasets:
            keys = data.keys()
            keys_str = ",".join(map(lambda n: "`%s`" % str(n), keys))
            values = [data[key] for key in keys]
            values = ",".join(map(lambda n: "'%s'" % str(n), values))
            # IGNORE makes it possible to easily restart insertion
            sql = "INSERT IGNORE INTO `wm_raw_draw_data` (%s) VALUES (%s);\n" % \
                  (keys_str, values)
            f.write(sql)
            datacounter += 1
            if datacounter % 10000 == 0:
                filecounter += 1
                f.write("UNLOCK TABLES;")
                f.close()
                f = open("wm_raw_draw_data_%i.sql" % filecounter, "w")
        elapsed_time = time.time() - start_time
        print("Downloaded %i datasets. Last %i in %0.2f seconds" %
              (datacounter, pagesize, elapsed_time))
    f.write("UNLOCK TABLES;")
    f.close()
if __name__ == '__main__':
    main(mysql_online)

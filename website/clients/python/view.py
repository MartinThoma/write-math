#!/usr/bin/env python

from HandwrittenData import HandwrittenData
from dbconfig import mysql
import MySQLdb
import MySQLdb.cursors


def main(s):
    a = HandwrittenData(s)
    a.show()

if __name__ == '__main__':
    from argparse import ArgumentParser
    parser = ArgumentParser()
    parser.add_argument("-i", "--id", dest="id", default=279062,
                        type=int,
                        help="which RAW_DATA_ID do you want?")
    args = parser.parse_args()

    # Establish database connection
    connection = MySQLdb.connect(host=mysql['host'],
                                 user=mysql['user'],
                                 passwd=mysql['passwd'],
                                 db=mysql['db'],
                                 cursorclass=MySQLdb.cursors.DictCursor)
    cursor = connection.cursor()

    # Download all datasets
    sql = "SELECT `data` FROM `wm_raw_draw_data` WHERE `id`=%i" % args.id
    cursor.execute(sql)
    data = cursor.fetchone()
    if data is None:
        print("RAW_DATA_ID %i does not exist." % args.id)
    else:
        main(data['data'])

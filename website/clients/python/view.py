#!/usr/bin/env python
"""
Display a raw_data_id.
"""

from HandwrittenData import HandwrittenData
import MySQLdb
import MySQLdb.cursors
import yaml


def main(s):
    a = HandwrittenData(s)
    a.show()

if __name__ == '__main__':
    from argparse import ArgumentParser
    parser = ArgumentParser(description=__doc__)
    parser.add_argument("-i", "--id", dest="id", default=279062,
                        type=int,
                        help="which RAW_DATA_ID do you want?")
    parser.add_argument("--mysql", dest="mysql", default='mysql_online',
                        help="which mysql configuration should be used?")
    args = parser.parse_args()

    # Import configuration file
    with open("db.config.yml", 'r') as ymlfile:
        cfg = yaml.load(ymlfile)

    # Establish database connection
    connection = MySQLdb.connect(host=cfg[args.mysql]['host'],
                                 user=cfg[args.mysql]['user'],
                                 passwd=cfg[args.mysql]['passwd'],
                                 db=cfg[args.mysql]['db'],
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

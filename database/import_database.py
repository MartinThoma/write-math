#!/usr/bin/env python
# -*- coding: utf-8 -*-

from __future__ import print_function
import MySQLdb
import MySQLdb.cursors
from dbconfig import mysql_local
import subprocess
from contextlib import closing
import gzip
import os
import time
import natsort


def main(mysql, folder):
    """
    Creates the required MySQL tables in a given mysql database.
    @param mysql: A dictionary with the keys 'host', 'user', 'passwd', 'db'
    @param folder:

    This function assumes a dicrectory structure like this:
    [folder]/structure/write-math.sql
    [folder]/structure/foreign-keys.sql
    [folder]/complete-dump/single-tables/[files with .sql or .sql.gz ending]
    """
    connection = MySQLdb.connect(host=mysql['host'],
                                 user=mysql['user'],
                                 passwd=mysql['passwd'],
                                 db=mysql['db'],
                                 cursorclass=MySQLdb.cursors.DictCursor)
    with closing(connection.cursor()) as cursor:
        # Import schema
        print("Import schema")
        with open(folder + 'structure/write-math.sql') as f:
            schema_sql_queries = f.read()
        cursor.execute(schema_sql_queries)

    prefix = folder + "complete-dump/single-tables/"

    files = os.listdir(prefix)
    tables = filter(lambda n: n.endswith('.sql'), files)
    tables += filter(lambda n: n.endswith('.gz'), files)
    tables = natsort.natsorted(tables)

    for table in tables:
        start_time = time.time()
        print("Import Table '%s'" % table, end="")
        proc = subprocess.Popen(["mysql",
                                 "--user=%s" % mysql['user'],
                                 "--password=%s" % mysql['passwd'],
                                 "--host=%s" % mysql['host'],
                                 "%s" % mysql['db']],
                                stdin=subprocess.PIPE,
                                stdout=subprocess.PIPE)
        if table.endswith(".gz"):
            out, err = proc.communicate(gzip.open(prefix+table).read())
        else:
            out, err = proc.communicate(open(prefix+table).read())
        if out != "" and out is not None:
            print("out:")
            print(out)
        if err != "" and err is not None:
            print("err")
            print(err)
        elapsed_time = time.time() - start_time
        print("... done in %0.2f s" % elapsed_time)
    proc = subprocess.Popen(["mysql",
                             "--user=%s" % mysql['user'],
                             "--password=%s" % mysql['passwd'],
                             "--host=%s" % mysql['host'],
                             "%s" % mysql['db']],
                            stdin=subprocess.PIPE,
                            stdout=subprocess.PIPE)
    out, err = proc.communicate("SET foreign_key_checks = 0;" +
                                open(prefix+'wm_renderings.sql').read() +
                                open(prefix+'wm_formula.sql').read())

    print("Add foreign keys:")
    with closing(connection.cursor()) as cursor:
        with open('structure/foreign-keys.sql') as f:
            schema_sql_queries = f.read()
        cursor.execute(schema_sql_queries)
    connection.close()

if __name__ == '__main__':
    from argparse import ArgumentParser

    parser = ArgumentParser()

    # Add more options if you like
    parser.add_argument("-f", "--folder",
                        dest="folder",
                        default="/var/www/write-math/database/",
                        help="folder with all mysql tables", metavar="FILE")

    args = parser.parse_args()
    main(mysql_local, args.folder)

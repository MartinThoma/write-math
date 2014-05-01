#!/usr/bin/env python
# -*- coding: utf-8 -*-

import os
import MySQLdb
import MySQLdb.cursors
from dbconfig import mysql  # a dictionary with the connection information


def create_svg(name):
    os.system("pdflatex %s.tex -output-format=pdf" % name)
    os.system("inkscape %s.pdf --export-plain-svg=%s.svg" % (name, name))


def upload_new_symbol(symbol, latex, svg):
    try:
        connection = MySQLdb.connect(host=mysql['host'], user=mysql['user'],
                                     passwd=mysql['pwd'], db=mysql['dbname'],
                                     cursorclass=MySQLdb.cursors.DictCursor)
    except MySQLdb.Error, e:
        logging.error("Could not connect to MySQL-Database.")
        logging.error(e)
        sys.exit(1)

    with connection:
        cursor = connection.cursor()
        sql = ("INSERT INTO `wm_formula` ("
               "`formula_name` ,"
               "`description` ,"
               "`formula_in_latex` ,"
               "`svg` ,"
               "`is_single_symbol`"
               ") VALUES ("
               "'%s',  'Single symbol ''%s''',  '%s',  '%s',  '1'"
               ");" % (symbol, symbol, latex, svg))
        cursor.execute(sql)
        connection.commit()

if __name__ == "__main__":
    with open('symbol.tex') as f:
        content = f.read()

    # Create big letters
    # for i in range(ord('A'), ord('Z') + 1):
    #     with open('tmp.tex', "w") as f:
    #         tmp = content.replace("{{ content }}", chr(i))
    #         f.write(tmp)

    #     create_svg("tmp")
    #     new_filename = chr(i) + ".svg"
    #     os.rename("tmp.svg", new_filename)
    #     with open(new_filename) as f:
    #         svg = f.read()
    #     upload_new_symbol(chr(i), chr(i), svg)
    #     os.remove(new_filename)

    for latex in ["$\\rightarrow$"]:
        with open('tmp.tex', "w") as f:
            tmp = content.replace("{{ content }}", latex)
            f.write(tmp)

        create_svg("tmp")
        new_filename = chr(i) + ".svg"
        os.rename("tmp.svg", new_filename)
        with open(new_filename) as f:
            svg = f.read()
        upload_new_symbol(latex, latex, svg)
        os.remove(new_filename)

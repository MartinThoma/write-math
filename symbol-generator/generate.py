#!/usr/bin/env python
# -*- coding: utf-8 -*-

import os
import MySQLdb
import MySQLdb.cursors
from dbconfig import mysql  # a dictionary with the connection information


def create_svg(name):
    os.system("pdflatex %s.tex -output-format=pdf" % name)
    os.system("inkscape %s.pdf --export-plain-svg=%s.svg" % (name, name))


def upload_new_symbol(symbol, latex):
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

        # Check if it's already in database
        sql = ("SELECT `id` FROM `wm_formula` WHERE `formula_in_latex` = %s")
        result = cursor.execute(sql, (latex,))
        print(latex)

        if result == 0:
            create_svg("tmp")
            new_filename = "tmp.svg"
            os.rename("tmp.svg", new_filename)
            with open(new_filename) as f:
                svg = f.read()

            # insert, if not
            sql = ("INSERT INTO `wm_formula` ("
                   "`formula_name` ,"
                   "`description` ,"
                   "`formula_in_latex` ,"
                   "`svg` ,"
                   "`is_single_symbol`"
                   ") VALUES ("
                   "%s, %s,  %s, %s, '1'"
                   ");")
            cursor.execute(sql, (symbol, symbol, latex, svg))
            connection.commit()

if __name__ == "__main__":
    with open('symbol.tex') as f:
        content = f.read()

    # Create big letters
    for i in range(ord('A'), ord('Z') + 1):
        with open('tmp.tex', "w") as f:
            tmp = content.replace("{{ content }}", chr(i))
            f.write(tmp)
        upload_new_symbol(chr(i), chr(i))

    # Small big letters
    for i in range(ord('a'), ord('z') + 1):
        with open('tmp.tex', "w") as f:
            tmp = content.replace("{{ content }}", chr(i))
            f.write(tmp)
        upload_new_symbol(chr(i), chr(i))

    # Small big letters
    for i in range(ord('0'), ord('9') + 1):
        with open('tmp.tex', "w") as f:
            tmp = content.replace("{{ content }}", chr(i))
            f.write(tmp)
        upload_new_symbol(chr(i), chr(i))

    for latex in [r"$\rightarrow$", r"$\pi$", r"$\alpha$", r"$\beta$", "$\sum$", "$\sigma$", "$\Sigma$"]:
        with open('tmp.tex', "w") as f:
            tmp = content.replace("{{ content }}", latex)
            f.write(tmp)

        upload_new_symbol(latex, latex)

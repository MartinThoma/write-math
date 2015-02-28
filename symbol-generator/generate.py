#!/usr/bin/env python
# -*- coding: utf-8 -*-

import os
import pymysql
import pymysql.cursors
from dbconfig import mysql  # a dictionary with the connection information
import yaml
from itertools import chain
import sys


def create_svg(name):
    os.system("pdflatex %s.tex -output-format=pdf" % name)
    os.system("pdf2svg %s.pdf %s.svg" % (name, name))


def get_svg(packages, latex, mode):
    with open('symbol.tex') as f:
        tmp = f.read()
    with open('tmp.tex', "w") as f:
        if mode == 'mathmode' or mode == 'bothmodes':
            tmp = tmp.replace("{{ content }}", '$' + latex + '$')
        else:
            tmp = tmp.replace("{{ content }}", latex)

        packagestring = ""
        for package in packages:
            packagestring += r"\usepackage{" + package + "}" + "\n"
        tmp = tmp.replace("{{ packages }}", packagestring)
        f.write(tmp)
    create_svg("tmp")
    new_filename = "tmp.svg"
    os.rename("tmp.svg", new_filename)
    with open(new_filename) as f:
        svg = f.read()
    return svg


def upload_new_symbol(symbol, latex, packages=[], mode='bothmodes'):
    try:
        connection = pymysql.connect(host=mysql['host'], user=mysql['user'],
                                     passwd=mysql['pwd'], db=mysql['dbname'],
                                     cursorclass=pymysql.cursors.DictCursor)
    except pymysql.Error, e:
        logging.error("Could not connect to MySQL-Database.")
        logging.error(e)
        sys.exit(1)

    with connection:
        cursor = connection.cursor()

        # Check if it's already in database
        sql = ("SELECT `id` FROM `wm_formula` WHERE `formula_in_latex` = %s")
        result = cursor.execute(sql, (latex,))
        sys.stdout.write(latex + " ")

        if result == 0:
            svg = get_svg(packages, latex, mode)

            # insert, if not
            sql = ("INSERT INTO `wm_formula` ("
                   "`formula_name`, "
                   "`description`, "
                   "`formula_in_latex`, "
                   "`svg`, "
                   "`is_single_symbol`, "
                   "`mode`, "
                   "`package` "
                   ") VALUES ("
                   "%s, %s,  %s, %s, '1', %s, %s"
                   ");")
            cursor.execute(sql, (symbol, symbol, latex, svg, mode, package))
            connection.commit()
        else:
            formula_id = cursor.fetchone()['id']
            # Is this formula "malformed"?
            sql = ("SELECT `id` FROM `wm_formula_svg_missing` "
                   "WHERE `formula_id` = %s")
            result = cursor.execute(sql, (formula_id,))
            if result != 0:
                svg = get_svg(packages, latex, mode)
                sql = ("UPDATE `wm_formula` SET  `package` =  %s,"
                       "`svg` = %s WHERE  `wm_formula`.`id` = %s;")
                cursor.execute(sql, (";".join(packages), svg, formula_id))
                connection.commit()
                print("\nUPDATED '%s' (ID %s)" % (latex, formula_id))


if __name__ == "__main__":
    with open('symbol.tex') as f:
        content = f.read()

    # Create big letters, small letters and numbers
    for i in chain(range(ord('A'), ord('Z') + 1),
                   range(ord('a'), ord('z') + 1),
                   range(ord('0'), ord('9') + 1)):
        with open('tmp.tex', "w") as f:
            tmp = content.replace("{{ content }}", chr(i))
            f.write(tmp)
        upload_new_symbol(chr(i), chr(i))

    print("\nStart yaml library:")
    stream = open("symbols.yaml", 'r')
    for first in yaml.load(stream):
        if type(first) is dict:
            if 'fontenc' in first:
                continue

            if 'package' in first:
                package = first['package']
            else:
                package = ""

            for mode in ['mathmode', 'textmode', 'bothmodes']:
                if mode in first:
                    for latex in first[mode]:
                        upload_new_symbol(latex, latex, [package], mode)
        else:
            print(first)

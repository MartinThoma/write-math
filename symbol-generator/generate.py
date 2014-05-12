#!/usr/bin/env python
# -*- coding: utf-8 -*-

import os
import MySQLdb
import MySQLdb.cursors
from dbconfig import mysql  # a dictionary with the connection information
import yaml


def create_svg(name):
    os.system("pdflatex %s.tex -output-format=pdf" % name)
    os.system("pdf2svg %s.pdf %s.svg" % (name, name))


def upload_new_symbol(symbol, latex, package='', mode='bothmodes'):
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
            with open('symbol.tex') as f:
                tmp = f.read()
            with open('tmp.tex', "w") as f:
                if mode == 'mathmode':
                    tmp = tmp.replace("{{ content }}", '$' + latex + '$')
                else:
                    tmp = tmp.replace("{{ content }}", '$' + latex + '$')
                tmp = tmp.replace("{{ packages }}", package)
                f.write(tmp)
            create_svg("tmp")
            new_filename = "tmp.svg"
            os.rename("tmp.svg", new_filename)
            with open(new_filename) as f:
                svg = f.read()

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

    counter = 0
    print("Start yaml library:")
    stream = open("symbols.yaml", 'r')
    for first in yaml.load(stream):
        if type(first) is dict:
            if first.has_key('fontenc'):
                continue

            if first.has_key('package'):
                package = first['package']
            else:
                package = ""

            if first.has_key('mathmode'):
                for latex in first['mathmode']:
                    upload_new_symbol(latex, latex, package, 'mathmode')
                    counter += 1
            if first.has_key('textmode'):
                for latex in first['textmode']:
                    upload_new_symbol(latex, latex, package, 'textmode')
                    counter += 1

            if first.has_key('bothmodes'):
                for latex in first['bothmodes']:
                    upload_new_symbol(latex, latex, package, 'bothmodes')
                    counter += 1
        else:
            print(first)

print(counter)

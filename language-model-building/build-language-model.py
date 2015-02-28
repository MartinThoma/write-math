#!/usr/bin/env python
# -*- coding: utf-8 -*-

from __future__ import print_function
import logging
FORMAT = "%(asctime)-15s %(message)s"
logging.basicConfig(filename='example.log',
                    level=logging.INFO,
                    format=FORMAT)
logging.debug("Test")
import re
import pymysql
import pymysql.cursors
from dbconfig import mysql
import os
from argparse import ArgumentParser
import json
import parse_folder
import sys


def get_known_symbols():
    sql = ("SELECT  `id` ,  `formula_in_latex`  FROM  `wm_formula` "
           "WHERE formula_type = 'single symbol';")
    cursor.execute(sql)
    datasets = cursor.fetchall()
    known_symbols = {}
    for el in datasets:
        known_symbols[el['formula_in_latex']] = 0
    return known_symbols


def extract_by_deleting(fn, known_symbols={}):
    basepath = os.path.dirname(fn) + "/"

    with open(fn, "rb") as f:
        content = f.read().strip()

    content_tmp = replace_definitions(content, basepath)
    while content != content_tmp:
        content = content_tmp
        content_tmp = replace_definitions(content, basepath)
    symbollist = []
    for symbol, count in known_symbols.items():
        symbollist.append(symbol)
    # letters, numbers and some special characters can be part of commands and
    # thus they should only be used in a much more sophisticated script
    small_letters = map(chr, range(ord('a'), ord('z')+1))
    big_letters = map(chr, range(ord('A'), ord('Z')+1))
    digits = map(chr, range(ord('0'), ord('9')+1))
    special = ['[', ']', '{', '}', '\\', ',', '.', ';', '.']
    symbollist = sorted(symbollist, key=lambda x: len(x), reverse=True)

    for symbol in symbollist:
        if symbol in (small_letters+big_letters+digits+special):
            continue
        pattern = re.escape(symbol)+"(?=[^A-Za-z]+)"
        symbolreg = re.compile(pattern)
        hits = symbolreg.findall(content)
        if len(hits) > 0:
            known_symbols[symbol] += len(hits)
            content = re.sub(symbolreg,
                             lambda m: "####",
                             content)
    return known_symbols


def replace_definitions(text, basepath):
    # self defined \usepackage
    usepackage = re.compile(r"\\usepackage\{(.*?)\}")
    for filename in usepackage.findall(text):
        filename = basepath + filename + ".sty"
        if os.path.isfile(filename):
            with open(filename) as f:
                c = f.read()
            text = re.sub(usepackage,
                          lambda m: c,
                          text)

    # \input
    inputcode = re.compile(r"\\input\{(.*?)\}")
    text = re.sub(inputcode,
                  lambda m: get_file_content(basepath+str(m.group(1))),
                  text)

    # \newcommand
    newcommand = re.compile(r"\\newcommand\{(.*?)\}\s*\{(.*?)\}")
    for findtext, replacetext in newcommand.findall(text):
        text = text.replace(findtext, replacetext)

    # \def
    curly = "(?:\{(?:.*?)\})"
    defcommand = re.compile(r"\\def(\\[A-Za-z][A-Za-z0-9]*)\{((?:[^\{]*?"
                            + curly + "{0,3})+)\}")
    for findtext, replacetext in defcommand.findall(text):
        text = text.replace(findtext, replacetext)
    # remove the command itself
    text = re.sub(defcommand, lambda m: "", text)
    return text


def extract_math_mode(text, is_wikipedia=False):
    singledollar = re.compile('\$(.*?)\$', re.MULTILINE)
    a = singledollar.findall(text)
    doubledollar = re.compile('\$\$(.*?)\$\$', re.MULTILINE)
    b = doubledollar.findall(text)
    newmath = re.compile('<math>(.*?)</math>')
    c = newmath.findall(text)
    d = extract_environments('equation', text)
    e = extract_environments('align', text)
    return map(lambda x: x.strip(), a + b + c + d + e)


def extract_symbols(text):
    symbol = re.compile(r'(\\[A-Za-z]+)')
    return symbol.findall(text)


def extract_environments(env, text):
    """ Get the content of all environments 'environment' as a list. """
    document = re.compile('\\\\begin{%s}(.*?)\\\\end{%s}' % (env, env),
                          re.MULTILINE | re.DOTALL)
    a = document.findall(text)
    return a


def extract_document_body(text):
    return extract_environments('document', text)


def get_file_content(filename):
    if os.path.isfile(filename):
        with open(filename, "rb") as f:
            content = f.read()
    elif os.path.isfile(filename+".tex"):
        with open(filename+".tex", "rb") as f:
            content = f.read()
    else:
        logging.warning("File '%s' and '%s.tex' does not exist." %
                        (filename, filename))
        content = ""
    return content


if __name__ == "__main__":
    logging.info("Start establishing connection")
    connection = pymysql.connect(host=mysql['host'],
                                 user=mysql['user'],
                                 passwd=mysql['passwd'],
                                 db=mysql['db'],
                                 cursorclass=pymysql.cursors.DictCursor)
    logging.info("Got it. Get cursor.")
    cursor = connection.cursor()
    logging.info("connection established")
    logging.info("Start getting symbols")
    known_symbols = get_known_symbols()
    logging.info("Got symbols")
    parser = ArgumentParser()
    filename = "/home/moose/Downloads/1406.5173v1_FILES/ms.tex"
    parser.add_argument("-f", "--file", dest="filename",
                        default=filename,
                        help="get language stats for this file",
                        metavar="FILE")
    parser.add_argument("-o", "--output", dest="output",
                        default=sys.stdout,
                        help="get language stats for this file",
                        metavar="FILE")
    args = parser.parse_args()
    known_symbols = extract_by_deleting(args.filename, known_symbols)
    if args.output != sys.stdout:
        with open(args.output, "w") as f:
            print(json.dumps(known_symbols), file=f)
    else:
        print(json.dumps(known_symbols))

#!/usr/bin/env python
# -*- coding: utf-8 -*-

import logging
FORMAT = "%(asctime)-15s %(message)s"
logging.basicConfig(filename='example.log',
                    level=logging.DEBUG,
                    format=FORMAT)
logging.debug("Test")
import re
import urllib2
import MySQLdb
import MySQLdb.cursors
from dbconfig import mysql
import os
import glob
import fnmatch


def extract_wikipedia_article(article_name):
    content  = urllib2.urlopen('http://de.wikipedia.org/w/api.php?format=json&action=query&titles=Laplace-Operator&prop=revisions&rvprop=content').read()
    mathexpressions = extract_math_mode(content, is_wikipedia=True)
    for expr in mathexpressions:
        expr = expr.replace("\\\\", "\\")
        symbols = extract_symbols(expr)
        for symbol in symbols:
            print(symbol+" in "+expr)


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
    defcommand = re.compile(r"\\def(\\[A-Za-z][A-Za-z0-9]*)\{((?:[^\{]*?(?:\{(?:.*?)\}){0,3})+)\}")
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


def is_latex_root(filename):
    with open(filename) as f:
        content = f.read()
    return "\\documentclass" in content


if __name__ == "__main__":
    logging.info("Start establishing connection")
    connection = MySQLdb.connect(host=mysql['host'],
                                 user=mysql['user'],
                                 passwd=mysql['passwd'],
                                 db=mysql['db'],
                                 cursorclass=MySQLdb.cursors.DictCursor)
    logging.info("Got it. Get cursor.")
    cursor = connection.cursor()
    logging.info("connection established")
    logging.info("Start getting symbols")
    known_symbols = get_known_symbols()
    logging.info("Got symbols")
    matches = []
    for root, dirnames, filenames in os.walk('/home/moose/Downloads/LaTeX-examples/'):
      for filename in fnmatch.filter(filenames, '*.tex'):
          matches.append(os.path.join(root, filename))
    for filename in matches:
        if is_latex_root(filename):
            print("yes"+filename)
            # filename = "/home/moose/Downloads/LaTeX-examples/documents/GeoTopo/Kapitel1.tex"
            # filename = "/home/moose/Downloads/1406.5173v1_FILES/ms.tex"
            # filename = "/home/moose/Downloads/LaTeX-examples/documents/GeoTopo/GeoTopo.tex"
            known_symbols = extract_by_deleting(filename, known_symbols=known_symbols)
    logging.info("#"*80)
    logging.info("Results:")
    for latex, counter in sorted(known_symbols.items(),
                                 key=lambda x: x[1],
                                 reverse=True):
        if counter > 0:
            logging.info("%s: %i" % (latex, counter))

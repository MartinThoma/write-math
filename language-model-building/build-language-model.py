#!/usr/bin/env python

import re
import urllib2
import MySQLdb
import MySQLdb.cursors
from dbconfig import mysql
import sys


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


def extract_wikipedia_article(article_name):
    content  = urllib2.urlopen('http://de.wikipedia.org/w/api.php?format=json&action=query&titles=Laplace-Operator&prop=revisions&rvprop=content').read()
    mathexpressions = extract_math_mode(content, is_wikipedia=True)
    for expr in mathexpressions:
        expr = expr.replace("\\\\", "\\")
        symbols = extract_symbols(expr)
        for symbol in symbols:
            print(symbol+" in "+expr)


def tokenize(mathexpression, tokens=None):
    if tokens is None:
        tokens = []
    if '{' in mathexpression:
        brakets = re.compile('{}')
    return tokens


def extract_latex_document(fn='/home/moose/Downloads/1406.5173v1_FILES/ms.tex',
                           known_symbols={}):
    with open(fn) as f:
        content = [f.read().strip()]
    c2 = []

    while len(content) > 0 or len(c2) > 0:
        if len(content) == 0:
            content = c2
            c2 = []
        for mathel in content:
            if mathel in known_symbols:
                known_symbols[mathel] += 1
                continue
            for el in extract_math_mode(mathel):
                # Nesting structures
                if r"\frac{" in el:
                    pattern = re.compile(r'(.*)\\frac{(.*?)}{(.*?)}(.*)',
                                         re.MULTILINE | re.DOTALL)
                    matches = pattern.findall(el)
                    for match in matches:
                        for el in match:
                            if el != '':
                                c2.append(el.strip())
                elif "^{" in el:
                    pattern = re.compile('(.*)\^{(.*)}(.*)')
                    matches = pattern.findall(el)
                    for base, head, after in matches:
                        if base+"^{"+head+"}"+after != el:
                            print("Not equal^!"*12)
                            print("El: %s" % el)
                            print("El: %s" % base+"^{"+head+"}"+after)
                            print("base: %s" % base)
                            print("head: %s" % head)
                            print("after: %s" % after)
                            sys.exit(-1)
                        if base != '' and base is not None:
                            c2.append(base.strip())
                        if head != '' and head is not None:
                            c2.append(head.strip())
                        if after != '' and head is not None:
                            c2.append(after.strip())
                elif "_{" in el:
                    pattern = re.compile('(.*)\_{(.*)}(.*)')
                    matches = pattern.findall(el)
                    for base, head, after in matches:
                        if base+"_{"+head+"}"+after != el:
                            print("Not equal_!"*12)
                            print("El: %s" % el)
                            print("El: %s" % base+"^{"+head+"}"+after)
                            print("base: %s" % base)
                            print("head: %s" % head)
                            sys.exit(-1)
                        if base != '' and base is not None:
                            c2.append(base.strip())
                        if head != '' and head is not None:
                            c2.append(head.strip())
                        if after != '' and head is not None:
                            c2.append(after.strip())
                elif "{" in el:
                    print("There is still a '{'. That should not happen.")
                    sys.exit(-1)
                elif "}" in el:
                    print("There is still a '}'. That should not happen.")
                    sys.exit(-1)
                elif "1" in el:
                    pattern = re.compile('(.*?)1(.*)')
                    matches = pattern.findall(el)
                    for base, head in matches:
                        if base+"1"+head != el:
                            print("Not equal_!"*12)
                            print("El: %s" % el)
                            print("El: %s" % base+"1"+head+"")
                            print("base: %s" % base)
                            print("head: %s" % head)
                            sys.exit(-1)
                        if base != '' and base is not None:
                            c2.append(base.strip())
                        if head != '' and head is not None:
                            c2.append(head.strip())
                elif "8" in el:
                    pattern = re.compile('(.*?)8(.*)')
                    matches = pattern.findall(el)
                    for base, head in matches:
                        if base+"8"+head != el:
                            print("Not equal_!"*12)
                            print("El: %s" % el)
                            print("El: %s" % base+"1"+head+"")
                            print("base: %s" % base)
                            print("head: %s" % head)
                            sys.exit(-1)
                        if base != '' and base is not None:
                            c2.append(base.strip())
                        if head != '' and head is not None:
                            c2.append(head.strip())
                elif " " in el:
                    pattern = re.compile('(.*?) (.*)')
                    matches = pattern.findall(el)
                    for base, head in matches:
                        if base + " " + head != el:
                            print("Not equal_!"*12)
                            print("El: %s" % el)
                            print("El: %s" % base+" "+head+"")
                            print("base: %s" % base)
                            print("head: %s" % head)
                            sys.exit(-1)
                        if base != '' and base is not None:
                            c2.append(base.strip())
                        if head != '' and head is not None:
                            c2.append(head.strip())
                elif "-" in el:
                    pattern = re.compile('(.*?)-(.*)')
                    matches = pattern.findall(el)
                    for base, head in matches:
                        if base + "-" + head != el:
                            print("Not equal-!"*12)
                            print("El: %s" % el)
                            print("El: %s" % base+"-"+head+"")
                            print("base: %s" % base)
                            print("head: %s" % head)
                            sys.exit(-1)
                        if base != '' and base is not None:
                            c2.append(base.strip())
                        if head != '' and head is not None:
                            c2.append(head.strip())
                elif el in known_symbols:
                    known_symbols[el] += 1
                else:
                    print("unknown symbol: %s" % el)
                    known_symbols[el] = 1  # TODO: Really?
        content = []
    return known_symbols


def get_known_symbols():
    sql = ("SELECT  `id` ,  `formula_in_latex`  FROM  `wm_formula` "
           "WHERE formula_type = 'single symbol';")
    cursor.execute(sql)
    datasets = cursor.fetchall()
    known_symbols = {}
    for el in datasets:
        known_symbols[el['formula_in_latex']] = 0
    return known_symbols


def main():
    known_symbols = get_known_symbols()
    results = extract_latex_document(known_symbols=known_symbols)
    print("#"*80)
    print("Results:")
    for latex, counter in sorted(results.items(), key=lambda x: x[1], reverse=True):
        if counter > 0:
            print("%s: %i" % (latex, counter))
        if "frac" in latex:
            print latex
            print "#"*200


if __name__ == "__main__":
    connection = MySQLdb.connect(host=mysql['host'],
                                 user=mysql['user'],
                                 passwd=mysql['passwd'],
                                 db=mysql['db'],
                                 cursorclass=MySQLdb.cursors.DictCursor)
    cursor = connection.cursor()
    main()

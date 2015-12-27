#!/usr/bin/env python

"""
Read the unicode.xml
"""

import logging
import sys

logging.basicConfig(format='%(asctime)s %(levelname)s %(message)s',
                    level=logging.DEBUG,
                    stream=sys.stdout)
from xml.dom import minidom
import pymysql
import pymysql.cursors
from dbconfig import mysql
import re


def simplify_latex(latex):
    """
    Simplify LaTeX code, e.g. by removing surrounding "\mbox".

    Parameters
    ----------
    latex : str

    Returns
    -------
    str
        A simplified version of the original LaTeX string.
    """
    latex = latex.strip()
    pattern = re.compile("^\\\mbox\{(.*?)\}$")
    matches = pattern.findall(latex)
    if len(matches) == 1 and len(matches[0]) > 0:
        latex = matches[0]
    return latex


def read():
    """
    Read the unicode.xml

    Returns
    -------
    dict :
        Maps LaTeX to a dictionalry. This dictionary contains the unicode
        decimal code point 'dec' and a description 'desc'.
    """
    latex2unicode_dec = {}

    xmldoc = minidom.parse('unicode.xml')
    itemlist = xmldoc.getElementsByTagName('character')
    logging.info("Read %i characters.", len(itemlist))
    for s in itemlist:
        t = s.getElementsByTagName('mathlatex')
        tn = s.getElementsByTagName('latex')
        desctags = s.getElementsByTagName('description')
        if len(desctags) > 0 and desctags[0].firstChild is not None:
            desc = desctags[0].firstChild.nodeValue.strip()
        if "'" in desc:
            desc = desc.replace("'", "\\'")
        if len(t) >= 1:
            dec = s.attributes['dec'].value
            for el in t:
                latex = simplify_latex(el.firstChild.nodeValue)
                if len(t) > 1:
                    logging.info("multiple (mathmode): '%s'", latex)
                try:
                    latex2unicode_dec[latex] = {'dec': int(dec),
                                                'desc': desc}
                except:
                    logging.debug("%s did not work", dec)
        if len(tn) >= 1:
            dec = s.attributes['dec'].value
            for el in tn:
                latex = simplify_latex(el.firstChild.nodeValue)
                if len(t) > 1:
                    logging.info("multiple (not mathmode): '%s'", latex)
                try:
                    latex2unicode_dec[latex] = {'dec': int(dec),
                                                'desc': desc}
                except:
                    logging.debug("%s did not work", dec)
        # else:
        #     t = s.getElementsByTagName('description')
        # if len(t) > 0 and t[0].firstChild is not None:
        #     desc = t[0].firstChild.nodeValue
        #     if not any([desc.startswith("VARIATION SELECTOR"),
        #                 desc.startswith("CJK COMPATIBILITY IDEOGRAPH")]):
        #         logging.info("'%s' has no latex", desc)
        # else:
        #     char_id = s.attributes['id'].value
        #     logging.info("Charid'%s' has no latex and no desc.", char_id)
    return latex2unicode_dec


def get_formula_datasets():
    """
    Get the mapping from LaTeX to the write-math.com ID.

    Returns
    -------
    dict :
        Maps LaTeX to the ID on write-math.com
    """
    connection = pymysql.connect(host=mysql['host'],
                                 user=mysql['user'],
                                 passwd=mysql['passwd'],
                                 db=mysql['db'],
                                 cursorclass=pymysql.cursors.DictCursor)
    cursor = connection.cursor()
    sql = ("SELECT id, formula_in_latex FROM `wm_formula` "
           "WHERE formula_type = 'single symbol'")
    cursor.execute(sql)
    datasets = cursor.fetchall()
    formula_datasets = {}
    for el in datasets:
        formula_datasets[el['formula_in_latex']] = el['id']
    return formula_datasets


def update(latex2unicode, formula_datasets):
    """
    Add the unicode code point as well as an description on write-math.com.

    Parameters
    ----------
    latex2unicode : dict
        Maps LaTeX to a dictionary which contains the unicode code point 'dec'
        and a description 'desc'.
    formula_datasets : dict
        Maps LaTeX to write-math-ID
    """
    connection = pymysql.connect(host=mysql['host'],
                                 user=mysql['user'],
                                 passwd=mysql['passwd'],
                                 db=mysql['db'],
                                 cursorclass=pymysql.cursors.DictCursor)
    cursor = connection.cursor()
    for latex, mysql_id in formula_datasets.items():
        if latex in latex2unicode:
            unicode_dec = latex2unicode[latex]['dec']
            desc = latex2unicode[latex]['desc']
            sql = ("UPDATE `wm_formula` "
                   "SET `unicode_dec` = '%i', `unicodexml_description` = '%s' "
                   "WHERE `id`= %i LIMIT 1;") % (unicode_dec, desc, mysql_id)
            # Commented out to prevent accidents
            # try:
            #     print(sql)
            #     cursor.execute(sql)
            #     connection.commit()
            # except Exception as e:
            #     print(e)
        else:
            logging.info("%s is not in latex2unicode", latex)


def main():
    """
    Orchestrate the downloading.
    """
    # 1. Download all data (id, latex)
    formula_datasets = get_formula_datasets()
    logging.info("Got %i datasets from server.", len(formula_datasets))

    # 2. Get data from unicode.xml
    latex2unicode = read()
    logging.info("Got %i elements.", len(latex2unicode))

    # 3. update unicode_dec where latex matches
    update(latex2unicode, formula_datasets)

    # 4. Find my datasets where no unicode_dec is specified - later
    # 4. find unicode_dec which don't have an entry in my database

if __name__ == '__main__':
    main()

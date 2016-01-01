#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
Get a list of all single symbols.
"""

import pymysql.cursors
import codecs

from hwrt import utils


def main():
    """
    Get a list of formulas.

    Parameters
    ----------
    cursor : a database cursor
    dataset : string
        Either 'all' or a path to a yaml symbol file.

    Returns
    -------
    list :
        A list of formulas
    """
    cfg = utils.get_database_configuration()
    mysql = cfg['mysql_online']
    connection = pymysql.connect(host=mysql['host'],
                                 user=mysql['user'],
                                 passwd=mysql['passwd'],
                                 db=mysql['db'],
                                 cursorclass=pymysql.cursors.DictCursor,
                                 charset='utf8')
    cursor = connection.cursor()
    sql = ("SELECT `id`, `formula_in_latex` FROM `wm_formula` "
           # "WHERE `formula_type` = 'single symbol' "
           "WHERE `formula_type` = 'nesting symbol' "
           "ORDER BY `formula_in_latex` ASC")
    cursor.execute(sql)
    symbols = cursor.fetchall()
    store_symbols(symbols)


def store_symbols(symbols):
    """
    Parameters
    ----------
    symbols : list
    """
    with codecs.open('vocabulary.txt', 'w', 'utf-8') as f:
        for symbol in symbols:
            f.write("%s\n" % symbol['formula_in_latex'])


def get_parser():
    """Get parser object for script get_vocabulary.py."""
    from argparse import ArgumentParser, ArgumentDefaultsHelpFormatter
    parser = ArgumentParser(description=__doc__,
                            formatter_class=ArgumentDefaultsHelpFormatter)
    parser.add_argument("-s", "--symbol",
                        dest="symbol_filename",
                        type=lambda x: utils.is_valid_file(parser, x),
                        required=True,
                        help="symbol yml file",
                        metavar="FILE")
    return parser


if __name__ == "__main__":
    args = get_parser().parse_args()
    main()

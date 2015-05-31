#!/usr/bin/env python

"""
Add a package tag to each symbol.
"""

import pymysql.cursors
import logging
import sys

import hwrt.utils

logging.basicConfig(format='%(asctime)s %(levelname)s %(message)s',
                    level=logging.DEBUG,
                    stream=sys.stdout)


def get_tags(mysql):
    """
    Parameters
    ----------
    mysql : dict
        Connection information

    Returns
    -------
    dict :
        The key is a tag name and the value is the database id.
    """
    connection = pymysql.connect(host=mysql['host'],
                                 user=mysql['user'],
                                 passwd=mysql['passwd'],
                                 db=mysql['db'],
                                 cursorclass=pymysql.cursors.DictCursor)
    cursor = connection.cursor()

    # Get the data
    sql = ("SELECT `id`, `tag_name` FROM `wm_tags` ORDER BY `id` ASC")
    cursor.execute(sql)
    datasets = cursor.fetchall()

    # Restructure data
    tagname2id = {}
    for d in datasets:
        tagname2id[d['tag_name']] = d['id']
    return tagname2id


def get_symbol_tags(mysql):
    """
    Parameters
    ----------
    mysql : dict
        Connection information

    Returns
    -------
    dict :
        The key is a tag name and the value is the database id.
    """
    connection = pymysql.connect(host=mysql['host'],
                                 user=mysql['user'],
                                 passwd=mysql['passwd'],
                                 db=mysql['db'],
                                 cursorclass=pymysql.cursors.DictCursor)
    cursor = connection.cursor()

    # Get the data
    sql = ("SELECT `wm_formula`.`id`, `package`, `formula_in_latex` "
           "FROM `wm_formula` "
           "ORDER BY `formula_in_latex` ASC")
    cursor.execute(sql)
    datasets = cursor.fetchall()

    return datasets


def adjust_tags(mysql, tags, symbols_to_tags):
    """
    Parameters
    ----------
    mysql : dict
        Connection information
    tags : dict
        Mapping tag names to tag ids
    symbols_to_tags : list of dicts
        Each dict has the keys {u'id': 89, u'tag_id': 6, u'package': ''}
    """
    connection = pymysql.connect(host=mysql['host'],
                                 user=mysql['user'],
                                 passwd=mysql['passwd'],
                                 db=mysql['db'],
                                 cursorclass=pymysql.cursors.DictCursor)
    cursor = connection.cursor()
    for symbol in symbols_to_tags:
        if symbol['package'] != '':
            if symbol['package'] not in tags:
                logging.info("Package '%s' not found (symbol: '%s').",
                             symbol['package'],
                             symbol['formula_in_latex'])
                continue
            sql = ("INSERT INTO `wm_tags2symbols` "
                   "(`tag_id`, `symbol_id`) VALUES (%s, %s)")
            try:
                cursor.execute(sql, (tags[symbol['package']], symbol['id']))
                logging.info("%s (id: %s) gets the tag %s.",
                             symbol['formula_in_latex'],
                             symbol['id'],
                             symbol['package'])
            except pymysql.err.IntegrityError:
                pass
            # connection is not autocommit by default. So you must commit to save
            # your changes.
            connection.commit()


def main():
    cfg = hwrt.utils.get_database_configuration()
    mysql = cfg['mysql_online']
    tags = get_tags(mysql)
    symbols_to_tags = get_symbol_tags(mysql)
    adjust_tags(mysql, tags, symbols_to_tags)


if __name__ == '__main__':
    main()

#!/usr/bin/env python

"""
Import data from Detexify into a MySQL database.
"""

import json
import sys
sys.path.append("/var/www/write-math/website/clients/python")
from hwrt.handwritten_data import HandwrittenData
import pymysql
import pymysql.cursors
from dbconfig import mysql
import os


def process_single_symbol(filename):
    """
    Parameters
    ----------
    filename : str
        Path to a file

    Returns
    -------
    tuple
        (rawdata, symbol) where raw_data is a list and symbol is an id.
    """
    with open(filename) as f:
        content = f.read()
    try:
        f = json.loads(content)
    except Exception as e:
        f = {'doc': content}
        print(e)

    if 'data' in f['doc']:
        rawdata, symbol = f['doc']['data'], f['doc']['id']
        for line in rawdata:
            for point in line:
                point['time'] = point.pop('t')
    else:
        print("filename: %s" % filename)
        print("f['doc'] = %s" % str(f['doc']))
        symbol = "unknown-unknown-unknown"
        rawdata = "[[{'x':0,'y':0,'time':0}]]"
    return (rawdata, symbol)


def parse_detexify_id(detexify_id):
    """Parse an id from Detexify into package, encoding and symbol."""
    splitted = detexify_id.split("-")
    package, encoding, symbol = splitted[0], splitted[1], splitted[2:]
    symbol = "-".join(symbol)
    symbol = symbol.replace("_", "\\")
    return (package, encoding, symbol)


def main(folder):
    """
    Orchestrate the downloading

    Parameters
    ----------
    folder : str
    """
    # Get IDs from server
    connection = pymysql.connect(host=mysql['host'],
                                 user=mysql['user'],
                                 passwd=mysql['passwd'],
                                 db=mysql['db'],
                                 cursorclass=pymysql.cursors.DictCursor)
    cursor = connection.cursor()
    sql = "SELECT id, formula_in_latex, package FROM `wm_formula`"
    cursor.execute(sql)
    datasets = cursor.fetchall()
    print("Got %i datasets." % len(datasets))
    latex2writemathid = {}
    for dataset in datasets:
        latex2writemathid[dataset['formula_in_latex']] = dataset

    # Get files
    from os import listdir
    from os.path import isfile, join
    files = [f for f in listdir(folder) if isfile(join(folder, f))]
    files = filter(lambda n: n.startswith("file"), files)
    files = sorted(files)
    print("Fetched %i files." % len(files))
    # Go through each file
    unknown_symbols = {}
    for i, rawdatafile in enumerate(files):
        if rawdatafile == 'file1':
            continue
        rawdatafile_full = join(folder, rawdatafile)
        raw_data, detexify_id = process_single_symbol(rawdatafile_full)
        package, encoding, symbol = parse_detexify_id(detexify_id)
        # an unkown symbol?
        if symbol not in latex2writemathid:
            if symbol not in unknown_symbols:
                unknown_symbols[symbol] = {'counter': 1,
                                           'package': package,
                                           'encoding': encoding,
                                           'symbol': symbol}
            else:
                unknown_symbols[symbol]['counter'] += 1
        else:
            symbol_id = latex2writemathid[symbol]['id']
            raw_data = pymysql.escape_string(json.dumps(raw_data))
            sql = ("INSERT INTO `wm_raw_draw_data` ("
                   "`user_id` , `data` , `nr_of_symbols`, "
                   "`md5data` , `creation_date` , `user_agent` , "
                   "`accepted_formula_id` "
                   ") VALUES ("
                   "'16925', '%s', '1', MD5('%s'), "
                   "CURRENT_TIMESTAMP , '', '%i'"
                   ");" % (raw_data, raw_data, symbol_id))
            try:
                cursor.execute(sql)
                connection.commit()
                os.rename(rawdatafile_full, "done/"+rawdatafile)
            except Exception as e:
                print("Skip - duplicate content?")
                os.rename(rawdatafile_full, "skipped/"+rawdatafile)
                print(e)
        if i % 200 == 0:
            print(i)
        if i % 50000 == 0:
            exit()

    summe = 0
    for key, value in sorted(unknown_symbols.items(),
                             key=lambda n: (n[1]['encoding'],
                                            -n[1]['counter'],
                                            n[0])):
        print("%ix %s\tPackage: %s;\tEncoding: %s" % (
              value['counter'],
              value['symbol'],
              value['package'],
              value['encoding']))
        summe += value['counter']
    print("Missing symbols: %i" % summe)

if __name__ == '__main__':
    # a = HandwrittenData(json.dumps(raw_data))
    # a.show()
    main('/var/www/write-math/detexify-import/splitted')

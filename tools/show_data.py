#!/usr/bin/env python
"""
Print which symbols are contained in a crossvalidation datasets.pickle file.
"""

from __future__ import print_function
import logging
import sys
import os
logging.basicConfig(format='%(asctime)s %(levelname)s %(message)s',
                    level=logging.DEBUG,
                    stream=sys.stdout)
import cPickle as pickle
sys.path.append("../website/clients/python")
from HandwrittenData import HandwrittenData  # Needed because of pickle
from collections import defaultdict


def main(picklefile):
    logging.info("Read '%s' ..." % picklefile)
    a = pickle.load(open(picklefile))
    logging.info("done")
    s = ""
    symbols = defaultdict(int)
    for el in a['handwriting_datasets']:
        symbols[el['formula_in_latex']] += 1

    for symbol, count in sorted(symbols.items(), key=lambda n: n[0]):
        if symbol in ['a', '0', 'A']:
            s += "\n%s (%i), " % (symbol, count)
        elif symbol in ['z', '9', 'Z']:
            s += "%s (%i) \n" % (symbol, count)
        else:
            s += "%s (%i), " % (symbol, count)
    print("## Data")
    print("Symbols: %i" % len(symbols))
    print("```")
    print(s[:-1])
    print("```")
    if 'preprocessing_queue' in a:
        print("## Preprocessing Queue")
        for preprocessing_el in a['preprocessing_queue']:
            print("* %s" % str(preprocessing_el))
    if 'features' in a:
        print("## Features")
        for feature in a['features']:
            print("* %s" % feature)
    print(a.keys())


def is_valid_file(parser, arg):
    if not os.path.exists(arg):
        parser.error("The file %s does not exist!" % arg)
    else:
        return arg


if __name__ == '__main__':
    from argparse import ArgumentParser
    parser = ArgumentParser(description=__doc__)
    parser.add_argument("-f", "--file", dest="picklefile",
                        default='handwriting.pickle',
                        type=lambda x: is_valid_file(parser, x),
                        help="where is the picklefile", metavar="FILE")
    args = parser.parse_args()
    main(args.picklefile)

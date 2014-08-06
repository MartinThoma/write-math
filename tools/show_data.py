#!/usr/bin/env python
"""
Print which symbols are contained in a datasets .pickle file.
"""

from __future__ import print_function
import logging
import sys
import os
logging.basicConfig(format='%(asctime)s %(levelname)s %(message)s',
                    level=logging.DEBUG,
                    stream=sys.stdout)
import cPickle as pickle
from HandwrittenData import HandwrittenData  # Needed because of pickle
from collections import defaultdict
import utils


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
    print("Recordings: %i" % sum(symbols.values()))
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


if __name__ == '__main__':
    PROJECT_ROOT = utils.get_project_root()

    # Get latest data file file
    models_folder = os.path.join(PROJECT_ROOT, "archive/datasets")
    latest_raw = utils.get_latest_in_folder(models_folder, ".pickle")
    from argparse import ArgumentParser, ArgumentDefaultsHelpFormatter
    parser = ArgumentParser(description=__doc__,
                            formatter_class=ArgumentDefaultsHelpFormatter)
    parser.add_argument("-f", "--file", dest="picklefile",
                        default=latest_raw,
                        type=lambda x: utils.is_valid_file(parser, x),
                        help="where is the picklefile", metavar="FILE")
    args = parser.parse_args()
    main(args.picklefile)

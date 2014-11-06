#!/usr/bin/env python
"""
Print which symbols are contained in a raw datasets .pickle file.
"""

from __future__ import print_function
import logging
import sys
import os
logging.basicConfig(format='%(asctime)s %(levelname)s %(message)s',
                    level=logging.DEBUG,
                    stream=sys.stdout)
try:  # Python 2
    import cPickle as pickle
except ImportError:  # Python 3
    import pickle
from collections import defaultdict

# mine
from hwrt import HandwrittenData  # Needed because of pickle
sys.modules['HandwrittenData'] = HandwrittenData
from hwrt import utils
from hwrt import preprocessing


def main(picklefile):
    logging.info("Read '%s' ..." % picklefile)
    a = pickle.load(open(picklefile))
    logging.info("Reading finished.")

    # Initialize variables
    s = ""
    symbols = defaultdict(int)
    wild_point_recs = 0
    wild_points = 0
    missing_line_recs = 0
    recs_with_errors = 0
    recs_with_single_dot = 0  # except symbols_with_dots
    single_dots = 0
    symbols_with_dots = ['i', 'j', '\cdot', '\div', '\\because', '\\therefore']
    percentages = []
    time_max_threshold = 30*1000  # Max 30 sec pro symbol
    time_max_list = []  # List with symbols that are over the time maximum

    for el in a['handwriting_datasets']:
        symbols[el['formula_in_latex']] += 1
        if el['handwriting'].get_time() > time_max_threshold:
            time_max_list.append(el['handwriting'])
        if el['handwriting'].wild_point_count > 0:
            wild_point_recs += 1
            wild_points += el['handwriting'].wild_point_count
        missing_line_recs += el['handwriting'].missing_line
        if el['handwriting'].wild_point_count > 0 or \
           el['handwriting'].missing_line:
            recs_with_errors += 1
        if el['handwriting'].count_single_dots() > 0 and \
           el['formula_in_latex'] not in symbols_with_dots and \
           "dots" not in el['formula_in_latex']:
            recs_with_single_dot += 1
            old_area = el['handwriting'].get_area()
            tmp = [preprocessing.RemoveDots()]
            el['handwriting'].preprocessing(tmp)
            new_area = el['handwriting'].get_area()
            percentage = float(new_area)/float(old_area)
            if percentage < 1.0:
                percentages.append(percentage)
        single_dots += el['handwriting'].count_single_dots()

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

    # Show errors
    print("Recordings with wild points: %i (%0.2f%%)" %
          (wild_point_recs,
           float(wild_point_recs)/len(a['handwriting_datasets'])*100))
    print("wild points: %i" % wild_points)
    print("Recordings with missing line: %i (%0.2f%%)" %
          (missing_line_recs,
           float(missing_line_recs)/len(a['handwriting_datasets'])*100))
    print("Recordings with errors: %i (%0.2f%%)" %
          (recs_with_errors,
           float(recs_with_errors)/len(a['handwriting_datasets'])*100))
    print("Recordings with dots: %i (%0.2f%%)" %
          (recs_with_single_dot,
           float(recs_with_single_dot)/len(a['handwriting_datasets'])*100))
    print("dots: %i" % single_dots)
    print("size changing removal: %i (%0.2f%%)" %
          (len(percentages),
           float(len(percentages))/len(a['handwriting_datasets'])*100))

    time_max_list = sorted(time_max_list,
                           key=lambda n: n.get_time(),
                           reverse=True)
    print("%i recordings took more than %i ms. That were: " %
          (len(time_max_list), time_max_threshold))
    for el in time_max_list:
        print("* %ims: %s: %s" % (el.get_time(),
                                  utils.get_readable_time(el.get_time()),
                                  el))
    # Show preprocessing queue if possible
    if 'preprocessing_queue' in a:
        print("## Preprocessing Queue")
        for preprocessing_el in a['preprocessing_queue']:
            print("* %s" % str(preprocessing_el))

    # Show features if possible
    if 'features' in a:
        print("## Features")
        for feature in a['features']:
            print("* %s" % feature)


if __name__ == '__main__':
    project_root = utils.get_project_root()

    # Get latest data file
    dataset_folder = os.path.join(project_root, "raw-datasets")
    latest_dataset = utils.get_latest_in_folder(dataset_folder, ".pickle")
    from argparse import ArgumentParser, ArgumentDefaultsHelpFormatter
    parser = ArgumentParser(description=__doc__,
                            formatter_class=ArgumentDefaultsHelpFormatter)
    parser.add_argument("-f", "--file", dest="picklefile",
                        default=latest_dataset,
                        type=lambda x: utils.is_valid_file(parser, x),
                        help="where is the picklefile", metavar="FILE")
    args = parser.parse_args()
    main(args.picklefile)

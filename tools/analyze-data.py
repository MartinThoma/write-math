#!/usr/bin/env python

"""Analyze data in a pickle file by maximum time / width / height and
   similar features.
"""

from __future__ import print_function
import logging
import sys
import os
logging.basicConfig(format='%(asctime)s %(levelname)s %(message)s',
                    level=logging.DEBUG,
                    stream=sys.stdout)
import cPickle as pickle
import time
import datetime
sys.path.append("../website/clients/python")
from HandwrittenData import HandwrittenData  # Needed because of pickle


def get_bounding_box_sizes(raw_datasets):
    bouding_box_sizes = []
    start_time = time.time()
    widthfile = open("widths.txt", "a")
    heightfile = open("height.txt", "a")
    timefile = open("times.txt", "a")
    for i, raw_dataset in enumerate(raw_datasets):
        if i % 100 == 0 and i > 0:
            # Show how much work was done / how much work is remaining
            percentage_done = float(i)/len(raw_datasets)
            current_running_time = time.time() - start_time
            remaining_seconds = current_running_time / percentage_done
            tmp = datetime.timedelta(seconds=remaining_seconds)
            sys.stdout.write("\r%0.2f%% (%s remaining)   " %
                             (percentage_done*100, str(tmp)))
            sys.stdout.flush()
        # Do the work
        b = raw_dataset['handwriting'].get_bounding_box()
        widthfile.write(str(b["maxx"] - b["minx"]) + "\n")
        heightfile.write(str(b["maxy"] - b["miny"]) + "\n")
        timefile.write(str(b["maxt"] - b["mint"]) + "\n")
    widthfile.close()
    heightfile.close()
    timefile.close()
    return bouding_box_sizes


def main(handwriting_datasets_file):
    # Load from pickled file
    logging.info("Start loading data...")
    loaded = pickle.load(open(handwriting_datasets_file))
    raw_datasets = loaded['handwriting_datasets']
    logging.info("Start analyzing")
    get_bounding_box_sizes(raw_datasets)


def is_valid_file(parser, arg):
    if not os.path.exists(arg):
        parser.error("The file %s does not exist!" % arg)
    else:
        return arg


if __name__ == '__main__':
    from argparse import ArgumentParser
    parser = ArgumentParser(description=__doc__)
    parser.add_argument("--handwriting_datasets", dest="handwriting_datasets",
                        help="where are the pickled handwriting_datasets?",
                        metavar="FILE",
                        type=lambda x: is_valid_file(parser, x),
                        default=("../archive/"
                                 "handwriting_datasets-2014-08-03.pickle"))
    args = parser.parse_args()
    main(args.handwriting_datasets)

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
from HandwrittenData import HandwrittenData  # Needed because of pickle
import numpy
import utils


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


def get_time_between_controll_points(raw_datasets):
    average_between_points = open("average_time_between_points.txt", "a")
    average_between_lines = open("average_time_between_lines.txt", "a")
    start_time = time.time()
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
        times_between_points = []
        times_between_lines = []
        last_line_end = None
        for line in raw_dataset['handwriting'].get_pointlist():
            if last_line_end is not None:
                times_between_lines.append(line[-1]['time'] - last_line_end)
            last_line_end = line[-1]['time']
            last_point_end = None
            for point in line:
                if last_point_end is not None:
                    times_between_points.append(point['time'] - last_point_end)
                last_point_end = point['time']
        average_between_points.write("%0.2f\n" %
                                     numpy.average(times_between_points))
        average_between_lines.write("%0.2f\n" %
                                    numpy.average(times_between_lines))

    average_between_points.close()
    average_between_lines.close()


def main(handwriting_datasets_file):
    # Load from pickled file
    logging.info("Start loading data...")
    loaded = pickle.load(open(handwriting_datasets_file))
    raw_datasets = loaded['handwriting_datasets']
    logging.info("Start analyzing")
    get_time_between_controll_points(raw_datasets)


def is_valid_file(parser, arg):
    arg = os.path.abspath(arg)
    if not os.path.exists(arg):
        parser.error("The file %s does not exist!" % arg)
    else:
        return arg


if __name__ == '__main__':
    PROJECT_ROOT = utils.get_project_root()

    # Get latest model description file
    models_folder = os.path.join(PROJECT_ROOT, "archive/datasets")
    latest_dataset = utils.get_latest_in_folder(models_folder, ".pickle")

    from argparse import ArgumentParser, ArgumentDefaultsHelpFormatter
    parser = ArgumentParser(description=__doc__,
                            formatter_class=ArgumentDefaultsHelpFormatter)
    parser.add_argument("-d", "--handwriting_datasets",
                        dest="handwriting_datasets",
                        help="where are the pickled handwriting_datasets?",
                        metavar="FILE",
                        type=lambda x: is_valid_file(parser, x),
                        default=latest_dataset)
    args = parser.parse_args()
    main(args.handwriting_datasets)

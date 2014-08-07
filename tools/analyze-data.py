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
import numpy
from HandwrittenData import HandwrittenData  # Needed because of pickle
import features
import utils


def get_summed_symbol_strok_lengts(raw_datasets):
    """For each symbol: sum up the length of all strokes."""
    strokefile = open("stroke-lengths.txt", "a")
    start_time = time.time()
    calculate_ink = features.Ink()
    for i, raw_dataset in enumerate(raw_datasets):
        if i % 100 == 0 and i > 0:
            utils.print_status(len(raw_datasets), i, start_time)
        ink = calculate_ink(raw_dataset['handwriting'])[0]
        strokefile.write("%0.2f\n" % ink)
    print("\r100%"+"\033[K\n")
    strokefile.close()


def get_bounding_box_sizes(raw_datasets):
    """Get and save the metrics of each recordings bounding box.
       That includes width, height and time.
    """
    bouding_box_sizes = []
    start_time = time.time()
    widthfile = open("widths.txt", "a")
    heightfile = open("height.txt", "a")
    timefile = open("times.txt", "a")
    for i, raw_dataset in enumerate(raw_datasets):
        if i % 100 == 0 and i > 0:
            utils.print_status(len(raw_datasets), i, start_time)
        box = raw_dataset['handwriting'].get_bounding_box()
        widthfile.write(str(box["maxx"] - box["minx"]) + "\n")
        heightfile.write(str(box["maxy"] - box["miny"]) + "\n")
        timefile.write(str(box["maxt"] - box["mint"]) + "\n")
    print("\r100%"+"\033[K\n")
    widthfile.close()
    heightfile.close()
    timefile.close()
    return bouding_box_sizes


def get_time_between_controll_points(raw_datasets):
    """For each recording: Store the average time between controll points of
       one stroke / controll points of two different lines.
    """
    average_between_points = open("average_time_between_points.txt", "a")
    average_between_lines = open("average_time_between_lines.txt", "a")
    start_time = time.time()
    for i, raw_dataset in enumerate(raw_datasets):
        if i % 100 == 0 and i > 0:
            utils.print_status(len(raw_datasets), i, start_time)

        # Do the work
        times_between_points, times_between_lines = [], []
        last_line_end = None
        if len(raw_dataset['handwriting'].get_pointlist()) == 0:
            logging.warning("%i has no content." %
                            raw_dataset['handwriting'].raw_data_id)
            continue
        for line in raw_dataset['handwriting'].get_sorted_pointlist():
            if last_line_end is not None:
                times_between_lines.append(line[-1]['time'] - last_line_end)
            last_line_end = line[-1]['time']
            last_point_end = None
            for point in line:
                if last_point_end is not None:
                    times_between_points.append(point['time'] - last_point_end)
                last_point_end = point['time']
        # The recording might only have one point
        if len(times_between_points) > 0:
            average_between_points.write("%0.2f\n" %
                                         numpy.average(times_between_points))
        # The recording might only have one line
        if len(times_between_lines) > 0:
            average_between_lines.write("%0.2f\n" %
                                        numpy.average(times_between_lines))
    print("\r100%"+"\033[K\n")
    average_between_points.close()
    average_between_lines.close()


def main(handwriting_datasets_file):
    """Start the creation of the wanted metric."""
    # Load from pickled file
    logging.info("Start loading data '%s' ...", handwriting_datasets_file)
    loaded = pickle.load(open(handwriting_datasets_file))
    raw_datasets = loaded['handwriting_datasets']
    logging.info("%i datasets loaded.", len(raw_datasets))
    logging.info("Start analyzing...")
    #get_time_between_controll_points(raw_datasets)
    #get_bounding_box_sizes(raw_datasets)
    get_summed_symbol_strok_lengts(raw_datasets)


if __name__ == '__main__':
    PROJECT_ROOT = utils.get_project_root()

    # Get latest model description file
    MODELS_FOLDER = os.path.join(PROJECT_ROOT, "archive/datasets")
    LATEST_DATASET = utils.get_latest_in_folder(MODELS_FOLDER, "raw.pickle")

    from argparse import ArgumentParser, ArgumentDefaultsHelpFormatter
    parser = ArgumentParser(description=__doc__,
                            formatter_class=ArgumentDefaultsHelpFormatter)
    parser.add_argument("-d", "--handwriting_datasets",
                        dest="handwriting_datasets",
                        help="where are the pickled handwriting_datasets?",
                        metavar="FILE",
                        type=lambda x: utils.is_valid_file(parser, x),
                        default=LATEST_DATASET)
    args = parser.parse_args()
    main(args.handwriting_datasets)

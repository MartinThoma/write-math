#!/usr/bin/env python

"""Create preprocessed dataset."""

from __future__ import print_function
import logging
import sys
import os
logging.basicConfig(format='%(asctime)s %(levelname)s %(message)s',
                    level=logging.DEBUG,
                    stream=sys.stdout)
import cPickle as pickle
import datetime
import time
import preprocessing


def create_preprocessed_dataset(path_to_data, preprocessing_queue):
    # Load from pickled file
    logging.info("Start loading data...")
    loaded = pickle.load(open(path_to_data))
    raw_datasets = loaded['handwriting_datasets']
    logging.info("Start applying preprocessing methods")
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
        raw_dataset['handwriting'].preprocessing(preprocessing_queue)
    print("")
    time_prefix = time.strftime("%Y-%m-%d-%H-%M")
    pickle.dump({'handwriting_datasets': raw_datasets,
                 'formula_id2latex': loaded['formula_id2latex'],
                 'preprocessing_queue': preprocessing_queue
                 },
                open("%s-handwriting_datasets_preprocessed.pickle" %
                     time_prefix, "wb"))


def is_valid_file(parser, arg):
    arg = os.path.abspath(arg)
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
                        default=("../../../archive/datasets/"
                                 "2014-08-03-18-06-"
                                 "handwriting_datasets-raw.pickle"))
    args = parser.parse_args()
    # Define which preprocessing methods will get applied
    preprocessing_queue = []
    preprocessing_queue.append((preprocessing.scale_and_shift, []))
    preprocessing_queue.append((preprocessing.connect_lines,
                                {'minimum_distance': 0.01}))
    preprocessing_queue.append((preprocessing.douglas_peucker,
                               {'EPSILON': 0.01}))
    preprocessing_queue.append((preprocessing.space_evenly,
                                {'number': 100,
                                 'kind': 'cubic'}))
    preprocessing_queue.append((preprocessing.scale_and_shift, []))
    create_preprocessed_dataset(args.handwriting_datasets, preprocessing_queue)

#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
Create pfiles.

Before this script is run, the `download.py` should get executed to generate
a handwriting_datasets.pickle with exactly those symbols that should also
be present in the pfiles and only raw_data that might get used for the
test-, validation- and training set.
"""

from __future__ import print_function
import logging
import sys
logging.basicConfig(format='%(asctime)s %(levelname)s %(message)s',
                    level=logging.DEBUG,
                    stream=sys.stdout)
import os
import cPickle as pickle
from HandwrittenData import HandwrittenData  # Needed because of pickle
import preprocessing  # Needed because of pickle
import features
import time
import datetime
import gc
import natsort


def make_pfile(dataset_name, folder, features, data, time_prefix):
    """ Create the pfile.
    @param filename name of the file that pfile_create will use to create
                    the pfile.
    @param features integer, number of features
    @param data     list of tuples ('feature_string', 'label')
    """
    input_filename = os.path.abspath(os.path.join(folder,
                                                  "%s.raw" % dataset_name))
    output_filename = os.path.abspath(os.path.join(folder,
                                                   "%s-%s.pfile" %
                                                   (time_prefix, dataset_name)
                                                   ))

    # create raw data file for pfile_create
    with open(input_filename, "w") as f:
        for symbolnr, instance in enumerate(data):
            feature_string, label = instance
            assert len(feature_string) == features, \
                "Expected %i features, got %i features" % \
                (features, len(feature_string))
            feature_string = " ".join(map(str, feature_string))
            line = "%i 0 %s %i" % (symbolnr, feature_string, label)
            print(line, file=f)
    command = "pfile_create -i %s -f %i -l 1 -o %s" % \
              (input_filename, features, output_filename)
    logging.info(command)
    os.system(command)
    os.remove(input_filename)


def prepare_dataset(dataset, formula_id2index, feature_list):
    """Transform each instance of dataset to a (Features, Label) tuple."""
    prepared = []
    start_time = time.time()
    for i, data in enumerate(dataset):
        x = []
        handwriting = data['handwriting']
        x = handwriting.feature_extraction(feature_list)  # Feature selection
        y = formula_id2index[data['formula_id']]  # Get label
        prepared.append((x, y))
        if i % 100 == 0 and i > 0:
            # Show how much work was done / how much work is remaining
            percentage_done = float(i)/len(dataset)
            current_running_time = time.time() - start_time
            remaining_seconds = current_running_time / percentage_done
            tmp = datetime.timedelta(seconds=remaining_seconds)
            sys.stdout.write("\r%0.2f%% (%s remaining)   " %
                             (percentage_done*100, str(tmp)))
            sys.stdout.flush()
    sys.stdout.write("\r100%%     \n")
    sys.stdout.flush()
    return prepared


def get_sets(path_to_data):
    """Get a training, validation and a testset as well as a dictionary that
    maps each formula_id to an index (0...nr_of_formulas).

    @param path_to_data a pickle file that contains a list of datasets. """
    loaded = pickle.load(open(path_to_data))
    datasets = loaded['handwriting_datasets']

    training_set, validation_set, test_set = [], [], []

    dataset_by_formula_id = {}
    formula_id2index = {}

    # Group data in dataset_by_formula_id so that 10% can be used for the
    # validation set
    for i, dataset in enumerate(datasets):
        if dataset['formula_id'] in dataset_by_formula_id:
            dataset_by_formula_id[dataset['formula_id']].append(dataset)
        else:
            dataset_by_formula_id[dataset['formula_id']] = [dataset]
        sys.stdout.write("\rGroup data ... %0.2f%%" % (float(i)/len(datasets)*100))
        sys.stdout.flush()
    print("")

    # Create the test-, validation- and training set
    print("Create the test-, validation- and training set")
    for formula_id, dataset in dataset_by_formula_id.items():
        formula_id2index[formula_id] = len(formula_id2index)
        i = 0
        for raw_data in dataset:
            if raw_data['is_in_testset']:
                test_set.append(raw_data)
            else:
                if i % 10 == 0:
                    validation_set.append(raw_data)
                else:
                    training_set.append(raw_data)
                i = (i + 1) % 10
    if 'preprocessing_queue' in loaded:
        preprocessing_queue = loaded['preprocessing_queue']
    else:
        preprocessing_queue = []
    return (training_set, validation_set, test_set, formula_id2index,
            preprocessing_queue)


def create_pfile(handwriting_datasets, folder):
    """Set everything up for the creation of the 3 pfiles (test, validation,
       training).
    """
    logging.info("Get sets...")
    (training_set, validation_set, test_set, formula_id2index,
     preprocessing_queue) = get_sets(handwriting_datasets)

    # Define which features will get extracted
    feature_list = [features.Stroke_Count(),
                    features.Constant_Point_Coordinates(lines=-1,
                                                        points_per_line=81,
                                                        fill_empty_with=0)
                    #features.First_N_Points(81)
                    #features.Bitmap(28)
                    ]

    # Get the dimension of the feature vector
    INPUT_FEATURES = sum(map(lambda n: n.get_dimension(), feature_list))

    # Output data for documentation
    print("Classes (nr of symbols): %i" % len(formula_id2index))

    print("#### Preprocessing")
    print("```")
    for algorithm, options in preprocessing_queue:
        print("* %r with %r" % (algorithm, options))
    print("```")

    print("#### Features (%i)" % INPUT_FEATURES)
    print("```")
    for algorithm in feature_list:
        print("* %s" % str(algorithm))
    print("```")
    logging.info("## Start creating pfiles")

    time_prefix = time.strftime("%Y-%m-%d-%H-%M")

    for dataset_name, dataset in [("testdata", test_set),
                                  ("validdata", validation_set),
                                  ("traindata", training_set)]:
        t0 = time.time()
        prepared = prepare_dataset(dataset,
                                   formula_id2index,
                                   feature_list)
        logging.info("start 'make_pfile' ...")
        make_pfile(dataset_name,
                   folder,
                   INPUT_FEATURES,
                   prepared,
                   time_prefix)
        t1 = time.time() - t0
        logging.info("%s was written. Needed %0.2f seconds" %
                     (dataset_name, t1))
        gc.collect()


def is_valid_file(parser, arg):
    if not os.path.exists(arg):
        parser.error("The file %s does not exist!" % os.path.abspath(arg))
    else:
        return arg

if __name__ == '__main__':
    logging.info("Started creation of pfiles.")

    scriptpath = os.path.dirname(os.path.realpath(__file__))
    joined = os.path.join(scriptpath, "../archive/datasets")
    dataset_dir = os.path.abspath(joined)
    latest_preprocessed_raw = ""
    for my_file in natsort.natsorted(os.listdir(dataset_dir), reverse=True):
        if my_file.endswith("preprocessed.pickle"):
            latest_preprocessed_raw = os.path.join(dataset_dir, my_file)

    from argparse import ArgumentParser, ArgumentDefaultsHelpFormatter
    parser = ArgumentParser(description=__doc__,
                            formatter_class=ArgumentDefaultsHelpFormatter)
    parser.add_argument("-d", "--handwriting_datasets",
                        dest="handwriting_datasets",
                        help="where are the pickled handwriting_datasets?",
                        metavar="FILE",
                        type=lambda x: is_valid_file(parser, x),
                        default=latest_preprocessed_raw)
    parser.add_argument("--folder", dest="folder",
                        help="where should the pfiles be put?",
                        metavar="FOLDER",
                        type=lambda x: is_valid_file(parser, x),
                        default=".")
    args = parser.parse_args()
    create_pfile(args.handwriting_datasets, args.folder)

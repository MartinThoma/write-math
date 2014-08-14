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
import gc
import utils
import yaml


def make_pfile(dataset_name, feature_count, data,
               output_filename):
    """ Create the pfile.
    @param filename name of the file that pfile_create will use to create
                    the pfile.
    @param feature_count integer, number of features
    @param data     list of tuples ('feature_string', 'label')
    """
    input_filename = os.path.abspath("%s.raw" % dataset_name)
    logging.info("Temporary file: '%s'", input_filename)
    # create raw data file for pfile_create
    with open(input_filename, "w") as f:
        for symbolnr, instance in enumerate(data):
            feature_string, label = instance
            assert len(feature_string) == feature_count, \
                "Expected %i features, got %i features" % \
                (feature_count, len(feature_string))
            feature_string = " ".join(map(str, feature_string))
            line = "%i 0 %s %i" % (symbolnr, feature_string, label)
            print(line, file=f)
    command = "pfile_create -i %s -f %i -l 1 -o %s" % \
              (input_filename, feature_count, output_filename)
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
            utils.print_status(len(dataset), i, start_time)
    sys.stdout.write("\r100%" + " "*80 + "\n")
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
        utils.print_status(len(datasets), i)
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


def create_pfile(path_to_data, feature_list, target_paths):
    """Set everything up for the creation of the 3 pfiles (test, validation,
       training).
    """
    logging.info("Start creation of pfiles...")
    logging.info("Get sets from '%s' ..." % path_to_data)
    (training_set, validation_set, test_set, formula_id2index,
     preprocessing_queue) = get_sets(path_to_data)

    # Get the dimension of the feature vector
    INPUT_FEATURES = sum(map(lambda n: n.get_dimension(), feature_list))

    # Output data for documentation
    print("Classes (nr of symbols): %i" % len(formula_id2index))

    print("#### Preprocessing")
    print("```")
    for algorithm in preprocessing_queue:
        print("* " + str(algorithm))
    print("```")

    print("#### Features (%i)" % INPUT_FEATURES)
    print("```")
    for algorithm in feature_list:
        print("* %s" % str(algorithm))
    print("```")
    logging.info("## Start creating pfiles")

    for dataset_name, dataset in [("testdata", test_set),
                                  ("validdata", validation_set),
                                  ("traindata", training_set)]:
        t0 = time.time()
        logging.info("Start preparing '%s' ..." % dataset_name)
        prepared = prepare_dataset(dataset,
                                   formula_id2index,
                                   feature_list)
        logging.info("%s length: %i", dataset_name, len(prepared))
        logging.info("start 'make_pfile' ...")
        make_pfile(dataset_name,
                   INPUT_FEATURES,
                   prepared,
                   target_paths[dataset_name])
        t1 = time.time() - t0
        logging.info("%s was written. Needed %0.2f seconds" %
                     (dataset_name, t1))
        gc.collect()


if __name__ == '__main__':
    PROJECT_ROOT = utils.get_project_root()

    # Get latest model description file
    models_folder = os.path.join(PROJECT_ROOT, "archive/models")
    latest_model = utils.get_latest_in_folder(models_folder, ".yml")

    # Get command line arguments
    from argparse import ArgumentParser, ArgumentDefaultsHelpFormatter
    parser = ArgumentParser(description=__doc__,
                            formatter_class=ArgumentDefaultsHelpFormatter)
    parser.add_argument("-m", "--model_description_file",
                        dest="model_description_file",
                        help="where is the model description YAML file?",
                        metavar="FILE",
                        type=lambda x: utils.is_valid_file(parser, x),
                        default=latest_model)
    args = parser.parse_args()

    # Read the model description file
    with open(args.model_description_file, 'r') as ymlfile:
        model_description = yaml.load(ymlfile)
    # Get preprocessed .pickle file from model description file
    handwriting_datasets = os.path.join(PROJECT_ROOT,
                                        model_description['preprocessed'])
    target_paths = {}
    for key in model_description['data']:
        tmp = os.path.join(PROJECT_ROOT, model_description['data'][key])
        model_description['data'][key] = tmp
        if key == 'training':
            target_paths['traindata'] = model_description['data'][key]
        elif key == 'validating':
            target_paths['validdata'] = model_description['data'][key]
        elif key == 'testing':
            target_paths['testdata'] = model_description['data'][key]

    # Get a list of all used features
    feature_list = features.get_features(model_description['features'])

    # Create pfiles!
    create_pfile(handwriting_datasets, feature_list, target_paths)

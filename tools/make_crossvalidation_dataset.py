#!/usr/bin/env python
# -*- coding: utf-8 -*-

""" Create a crossvalidation (hence: binned) dataset from a dataset.pickle."""

import cPickle as pickle
import utils
import os
import time
import logging
import sys
logging.basicConfig(format='%(asctime)s %(levelname)s %(message)s',
                    level=logging.DEBUG,
                    stream=sys.stdout)


def main(MIN_OCCURENCES=100, K_FOLD=10):
    PROJECT_ROOT = utils.get_project_root()

    # Get latest model description file
    models_folder = os.path.join(PROJECT_ROOT, "archive/datasets")
    latest_dataset_file = utils.get_latest_in_folder(models_folder,
                                                     "raw.pickle")

    logging.info("Load raw datasets ...")
    loaded = pickle.load(open(latest_dataset_file))
    datasets = loaded['handwriting_datasets']
    logging.info("Raw datasets loaded. Create bins ...")

    # Prepare crossvalidation data set
    cv = [[], [], [], [], [], [], [], [], [], []]

    dataset_by_formula_id = {}
    index2formula_id = []
    formula_id2index = {}
    symbols = {}

    for dataset in datasets:
        if dataset['formula_id'] in dataset_by_formula_id:
            dataset_by_formula_id[dataset['formula_id']].append(dataset)
        else:
            dataset_by_formula_id[dataset['formula_id']] = [dataset]

    logging.info("another run ...")
    for formula_id, dataset in dataset_by_formula_id.items():
        formula_id2index[formula_id] = len(index2formula_id)
        index2formula_id.append(formula_id)
        symbols[loaded['formula_id2latex'][formula_id]] = len(dataset)
        i = 0
        for raw_data in dataset:
            cv[i].append(raw_data)
            i = (i + 1) % K_FOLD

    time_prefix = time.strftime("%Y-%m-%d-%H-%M")
    tmp = "archive/cv-datasets/%s.pickle" % time_prefix
    target_filename = os.path.join(PROJECT_ROOT, tmp)
    logging.info("Write '%s' to disk ..." % target_filename)
    pickle.dump({'cv': cv,
                 'formula_id2latex': loaded['formula_id2latex'],
                 'index2formula_id': index2formula_id,
                 'formula_id2index': formula_id2index,
                 'symbols': symbols
                 },
                open(target_filename, "wb"))


if __name__ == '__main__':
    from argparse import ArgumentParser, ArgumentDefaultsHelpFormatter
    parser = ArgumentParser(description=__doc__,
                            formatter_class=ArgumentDefaultsHelpFormatter)
    parser.add_argument("-m", "--min-occurences", dest="MIN_OCCURENCES",
                        type=int, default=100,
                        help="How many training instances should exist at" +
                             "minimum for a symbol to be considered?")
    parser.add_argument("-k", "--kfold", dest="K_FOLD",
                        type=int, default=10,
                        help="How many equal sized bins should be created?")
    args = parser.parse_args()
    main(args.MIN_OCCURENCES, args.K_FOLD)

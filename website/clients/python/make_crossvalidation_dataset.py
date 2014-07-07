#!/usr/bin/env python
# -*- coding: utf-8 -*-

import cPickle as pickle


def main(MIN_OCCURENCES=10, K_FOLD=10):
    loaded = pickle.load(open("handwriting_datasets.pickle"))
    datasets = loaded['handwriting_datasets']

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

    for formula_id, dataset in dataset_by_formula_id.items():
        if len(dataset) >= MIN_OCCURENCES:
            formula_id2index[formula_id] = len(index2formula_id)
            index2formula_id.append(formula_id)
            symbols[loaded['formula_id2latex'][formula_id]] = len(dataset)
            i = 0
            for raw_data in dataset:
                cv[i].append(raw_data)
                i = (i + 1) % K_FOLD
    pickle.dump({'cv': cv,
                 'formula_id2latex': loaded['formula_id2latex'],
                 'index2formula_id': index2formula_id,
                 'formula_id2index': formula_id2index,
                 'symbols': symbols
                 },
                open("cv_datasets.pickle", "wb"))


if __name__ == '__main__':
    from argparse import ArgumentParser, ArgumentDefaultsHelpFormatter

    parser = ArgumentParser(formatter_class=ArgumentDefaultsHelpFormatter)

    # Add more options if you like
    parser.add_argument("-m", "--min-occurences", dest="MIN_OCCURENCES",
                        type=int, default=10,
                        help="How many training instances should exist at" +
                             "minimum for a symbol to be considered?")
    parser.add_argument("-k", "--kfold", dest="K_FOLD",
                        type=int, default=10,
                        help="How many equal sized bins should be created?")

    args = parser.parse_args()

    main(args.MIN_OCCURENCES, args.K_FOLD)

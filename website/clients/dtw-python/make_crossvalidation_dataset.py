#!/usr/bin/env python

import cPickle as pickle


def main():
    MIN_OCCURENCES = 10
    K_FOLD = 10

    datasets = pickle.load(open("handwriting_datasets.pickle"))

    # Prepare crossvalidation data set
    cv = [[], [], [], [], [], [], [], [], [], []]

    dataset_by_formula_id = {}

    for dataset in datasets:
        if dataset['formula_id'] in dataset_by_formula_id:
            dataset_by_formula_id[dataset['formula_id']].append(dataset)
        else:
            dataset_by_formula_id[dataset['formula_id']] = [dataset]

    for formula_id, dataset in dataset_by_formula_id.items():
        if len(dataset) >= MIN_OCCURENCES:
            i = 0
            for raw_data in dataset:
                cv[i].append(raw_data)
                i = (i + 1) % K_FOLD

    pickle.dump(cv, open("cv_datasets.pickle", "wb"))


if __name__ == '__main__':
    main()

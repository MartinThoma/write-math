#!/usr/bin/env python
# -*- coding: utf-8 -*-

import sys
sys.path.append("/var/www/write-math/website/clients/python")
import preprocessing
from dtw_classifier import dtw_classifier
from make_crossvalidation_dataset import main as make_crossvalidation_dataset
from download_dataset import main as download_dataset
import cPickle as pickle
import logging
import time
from argparse import ArgumentParser
logging.basicConfig(filename='test.log',
                    level=logging.DEBUG,
                    format='%(asctime)s %(levelname)s: %(message)s')


def pp_results(results, data, formula_id2latex):
    """Pretty-Print the results of the cross-validation."""
    s = "Raw-Data-ID: %i; Reality: %s\n" % \
        (data['id'], formula_id2latex[data['formula_id']])
    for result in results:
        s += "\t%0.3f for\t%s\n" % \
             (result['p'],
              formula_id2latex[result['formula_id']['formula_id']])
    return s


def main(K_FOLD=10, get_new_dataset=False):
    if get_new_dataset:
        print("Download dataset ...")
        download_dataset()
        print("make_crossvalidation_dataset ...")
        make_crossvalidation_dataset()

    logging.info("Load data")
    tmp = pickle.load(open('cv_datasets.pickle'))
    cv = tmp['cv']
    formula_id2latex = tmp['formula_id2latex']

    # apply preprocessing
    logging.info("Apply Preprocessing")
    for i in range(K_FOLD):
        for data in cv[i]:
            data['handwriting'].preprocessing(
                [(preprocessing.scale_and_shift, []),
                 (preprocessing.douglas_peucker, {'EPSILON': 0.2}),
                 (preprocessing.space_evenly, {'number': 100})])

    # start testing
    logging.info("Start testing")
    ca = []
    i = 0

    for testset in range(K_FOLD):
        logging.info("Start test set: %i" % testset)
        ca.append({'correct': 0, 'wrong': 0, 'c10': 0, 'w10': 0, 'time': 0,
                   'processed_datasets': 0})
        classifier = dtw_classifier()

        learndata = []
        for i in range(K_FOLD):
            if i != testset:
                learndata += cv[i]
        classifier.learn(learndata)
        for data in cv[testset]:
            i += 1
            start = time.time()
            results = classifier.classify(data['handwriting'])
            end = time.time()

            ca[testset]['processed_datasets'] += 1
            ca[testset]['time'] += end - start

            if len(results) > 0:
                if results[0]['formula_id'] == data['formula_id']:
                    ca[testset]['correct'] += 1
                    ca[testset]['c10'] += 1
                else:
                    ca[testset]['wrong'] += 1

                    if data['formula_id'] in [r['formula_id']
                                              for r in results]:
                        ca[testset]['c10'] += 1
                    else:
                        ca[testset]['w10'] += 1
                        logging.info(pp_results(results,
                                                data,
                                                formula_id2latex))
            else:
                logging.debug("No result for Raw-Data-ID: %i; Reality: %s\n" %
                              (data['id'],
                               formula_id2latex[data['formula_id']]))
                ca[testset]['wrong'] += 1
                ca[testset]['w10'] += 1

            if i % 100 == 0:
                logging.info(ca)

if __name__ == '__main__':
    parser = ArgumentParser()

    # Add more options if you like
    parser.add_argument("-k", "--kfold", dest="kfold", type=int, default=10,
                        help="K Fold cross validation")
    parser.add_argument("-r", "--refresh", dest="refresh_dataset",
                        action="store_true", default=False,
                        help="refresh dataset")

    args = parser.parse_args()
    main(args.kfold, args.refresh_dataset)

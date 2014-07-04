#!/usr/bin/env python
# -*- coding: utf-8 -*-

import preprocessing
from dtw_classifier import dtw_classifier
from make_crossvalidation_dataset import main as make_crossvalidation_dataset
from download_dataset import main as download_dataset
import cPickle as pickle
import logging
import time
logging.basicConfig(filename='classificationpy.log',
                    level=logging.DEBUG,
                    format='%(asctime)s %(levelname)s: %(message)s')


def main(K_FOLD=10, get_new_dataset=False):
    if get_new_dataset:
        download_dataset()
        make_crossvalidation_dataset()

    logging.info("Load data")
    cv = pickle.load(open('cv_datasets.pickle'))

    # apply preprocessing
    logging.info("Apply Preprocessing")
    for i in range(K_FOLD):
        for data in cv[i]:
            data['handwriting'].preprocessing([(preprocessing.scale_and_shift, []),
                                               (preprocessing.space_evenly,
                                                {'number': 100}),
                                               (preprocessing.douglas_peucker,
                                                {'EPSILON': 0.2})])

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

            if results[0]['formula_id'] == data['formula_id']:
                ca[testset]['correct'] += 1
                ca[testset]['c10'] += 1
            else:
                ca[testset]['wrong'] += 1

                if data['formula_id'] in [r['formula_id'] for r in results]:
                    ca[testset]['c10'] += 1
                else:
                    ca[testset]['w10'] += 1
                    logging.info("Raw-Data-ID: %i; HYP: %s; Reality: %i" %
                                 (data['id'], str(results), data['formula_id'])
                                 )

            if i % 100 == 0:
                logging.info(ca)

if __name__ == '__main__':
    main()

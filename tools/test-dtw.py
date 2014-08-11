#!/usr/bin/env python
# -*- coding: utf-8 -*-

from __future__ import print_function
import logging
import sys
logging.basicConfig(format='%(asctime)s %(levelname)s %(message)s',
                    level=logging.DEBUG,
                    stream=sys.stdout)
import time
from HandwrittenData import HandwrittenData  # Needed because of pickle
from dtw_classifier import dtw_classifier
from make_crossvalidation_dataset import main as make_crossvalidation_dataset
import cPickle as pickle
import os
import utils


def pp_results(results, data, formula_id2latex):
    """Pretty-Print the results of the cross-validation."""
    s = "Raw-Data-ID: %i; Reality: %s\n" % \
        (data['id'], formula_id2latex[data['formula_id']])
    for result in results:
        s += "\t%0.3f for\t%s (Raw_dataset_id: %i)\n" % \
             (result['p'],
              formula_id2latex[result['formula_id']['formula_id']],
              result['formula_id']['handwriting'].raw_data_id)
    return s


def get_cv_data(PROJECT_ROOT):
    """Get latest cv dataset."""
    cv_folder = os.path.join(PROJECT_ROOT, "archive/cv-datasets")
    latest_cv_dataset = utils.get_latest_in_folder(cv_folder, ".pickle")
    if os.path.isfile(latest_cv_dataset):
        logging.info("Load '%s' ...", latest_cv_dataset)
        tmp = pickle.load(open(latest_cv_dataset))
        cv = tmp['cv']
        formula_id2latex = tmp['formula_id2latex']
        return cv, formula_id2latex
    else:
        sys.exit("No cv-dataset found in archive/cv-datasets. "
                 "You could try make_crossvalidation_dataset.py.")


def store_classification_result_data(ca, results, data, testset,
                                     formula_id2latex, start, LOGFILE):
    """Insert latest classification result into ca."""
    end = time.time()

    # Write hypothesis to logfile
    with open(LOGFILE, "a") as f:
        f.write("%i,%i" % (data['formula_id'], data['id']))
        for i in len(results):
            f.write(",%i,%i" % (
                results[i]['formula_id']['formula_id'],
                results[i]['formula_id']['handwriting'].raw_data_id))
        f.write("\n")

    ca[testset]['processed_datasets'] += 1
    ca[testset]['time'] += end - start
    if len(results) > 0:
        if results[0]['formula_id']['formula_id'] == data['formula_id']:
            ca[testset]['correct'] += 1
            ca[testset]['c10'] += 1
        else:
            ca[testset]['wrong'] += 1

            if data['formula_id'] in [r['formula_id']['formula_id']
                                      for r in results]:
                ca[testset]['c10'] += 1
            else:
                ca[testset]['w10'] += 1
                # logging.info(pp_results(results,
                #                         data,
                #                         formula_id2latex))
    else:
        logging.debug("No result for Raw-Data-ID: %i; Reality: %s\n",
                      data['id'],
                      formula_id2latex[data['formula_id']])
        ca[testset]['wrong'] += 1
        ca[testset]['w10'] += 1
    return ca


def main(K_FOLD=10, get_new_dataset=False):
    """Do a K_FOLD cross-validation on the latest cv-datasets .pickle file.
    """
    if get_new_dataset:
        logging.info("Download dataset ...")
        from download_dataset import main as download_dataset
        download_dataset()
        logging.info("make_crossvalidation_dataset ...")
        make_crossvalidation_dataset()

    PROJECT_ROOT = utils.get_project_root()

    # Get name of logfile
    logging_folder = os.path.join(PROJECT_ROOT, "archive/logs")
    time_prefix = time.strftime("%Y-%m-%d-%H-%M")
    LOGFILE = os.path.join(logging_folder, "%s-DTW.log" % time_prefix)

    open(LOGFILE, 'w').close()  # Truncate the file

    # Write header
    with open(LOGFILE, "a") as f:
        stmp = "Correct_Formula_ID,RAW_DATA_ID"
        for i in range(1, 10+1):
            stmp += ",%i,confused %i" % (i, i)
        f.write(stmp + "\n")

    cv, formula_id2latex = get_cv_data(PROJECT_ROOT)

    # start testing
    logging.info("Start testing")
    ca = []
    i = 0

    for testset in range(K_FOLD):
        logging.info("Start test set: %i", testset)
        ca.append({'correct': 0, 'wrong': 0, 'c10': 0, 'w10': 0, 'time': 0,
                   'processed_datasets': 0})
        classifier = dtw_classifier()

        learndata = []
        for i in range(K_FOLD):
            if i != testset:
                learndata += cv[i]
        classifier.learn(learndata)
        start_time = time.time()
        for i_loop, data in enumerate(cv[testset]):
            if i_loop % 10 == 0 and i_loop > 0:
                utils.print_status(len(cv[testset]), i, start_time)
            i += 1

            # Classify
            start = time.time()
            results = classifier.classify(data['handwriting'])
            # Store results
            ca = store_classification_result_data(ca, results, data, testset,
                                                  formula_id2latex, start,
                                                  LOGFILE)

            if i % 100 == 0:
                logging.info(ca)
        print("\r100%"+"\033[K\n")
    return ca

if __name__ == '__main__':
    from argparse import ArgumentParser, ArgumentDefaultsHelpFormatter
    parser = ArgumentParser(description=__doc__,
                            formatter_class=ArgumentDefaultsHelpFormatter)
    parser.add_argument("-k", "--kfold", dest="kfold", type=int, default=10,
                        help="K Fold cross validation")
    parser.add_argument("-r", "--refresh", dest="refresh_dataset",
                        action="store_true", default=False,
                        help="refresh dataset")

    args = parser.parse_args()
    print(main(args.kfold, args.refresh_dataset))

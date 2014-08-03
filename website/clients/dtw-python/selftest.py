#!/usr/bin/env python

from __future__ import print_function
import logging
import sys
import os
logging.basicConfig(format='%(asctime)s %(levelname)s %(message)s',
                    level=logging.DEBUG,
                    stream=sys.stdout)
import time
import datetime
import yaml
sys.path.append("/var/www/write-math/website/clients/python")
from HandwrittenData import HandwrittenData  # Needed because of pickle
import preprocessing
import dtw_classifier
import cPickle as pickle

CLASSIFIER_NAME = "dtw-python"


def print_experiment_parameters(symbols, symbol_counter, raw_data_counter,
                                EPSILON, CENTER, THRESHOLD,
                                SPACE_EVENLY, SPACE_EVENLY_KIND, POINTS,
                                K_FOLD, t1sum=-1, t10sum=-1,
                                execution_time=[]):
    print("\n" + "-"*80)
    print(str(datetime.date.today()))
    print("")
    print("```")
    print("The following %i symbols were evaluated:" % symbol_counter)
    print(", ".join(symbols))
    print("raw datasets: %i" % raw_data_counter)
    print("Epsilon: %0.2f" % EPSILON)
    print("Center: %r" % CENTER)
    print("Squared quadratic: False")
    print("Threshold: %r" % THRESHOLD)
    if SPACE_EVENLY:
        print("Space evenly: %r (%i points, %s)" % (SPACE_EVENLY, POINTS,
                                                    SPACE_EVENLY_KIND))
    else:
        print("Space evenly: %r" % SPACE_EVENLY)
    print("* Top-1-Classification (%i-fold cross-validated): %0.5f" %
          (K_FOLD, (t1sum/K_FOLD)))
    print("* Top-10-Classification (%i-fold cross-validated): %0.5f" %
          (K_FOLD, t10sum/K_FOLD))
    if len(execution_time) > 0:
        print("Average time: %.5f seconds" %
              (sum(execution_time)/len(execution_time)))
    print("```")


def crossvalidation(path_to_data):
    # Parameters for self-testing
    K_FOLD = 10
    EPSILON = 10
    CENTER = False
    THRESHOLD = 20
    SPACE_EVENLY = True
    SPACE_EVENLY_KIND = 'linear'
    POINTS = 100  # Does only make sense with SPACE_EVENLY=True

    # Prepare crossvalidation data set
    cv = [[], [], [], [], [], [], [], [], [], []]

    symbol_counter = 0
    raw_data_counter = 0
    symbols = []

    # Load from pickled file
    logging.info("Start loading data...")
    loaded = pickle.load(open(path_to_data))
    raw_datasets = loaded['handwriting_datasets']
    formula_id2raw_counter = {}
    logging.info("Start creating crossvalidation sets...")
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
        fid = raw_dataset['handwriting'].formula_id
        to_append = {'handwriting': raw_dataset['handwriting'],
                     'formula_in_latex': raw_dataset['formula_in_latex']}
        if fid not in formula_id2raw_counter:
            cv[0].append(to_append)
            formula_id2raw_counter[fid] = 1
        else:
            cv[formula_id2raw_counter[fid]].append(to_append)
            formula_id2raw_counter[fid] = ((formula_id2raw_counter[fid] + 1) %
                                           K_FOLD)

    print_experiment_parameters(symbols, symbol_counter, raw_data_counter,
                                EPSILON, CENTER, THRESHOLD,
                                SPACE_EVENLY, SPACE_EVENLY_KIND, POINTS,
                                K_FOLD)

    # Start getting validation results
    classification_accuracy = []
    print("\n\n")
    logging.info("Start validation ...")
    execution_time = []

    for testset in range(K_FOLD):
        classification_accuracy.append({'correct': 0,
                                        'wrong': 0,
                                        'c10': 0,
                                        'w10': 0})

        # Prepare datasets the algorithm may use
        trainingset = []
        for key, value in enumerate(cv):
            if key != testset:
                trainingset += value

        # Learn
        classifier = dtw_classifier.dtw_classifier()
        classifier.learn(trainingset)

        start_time = time.time()
        for i, testdata in enumerate(cv[testset]):
            start = time.time()
            A = testdata['handwriting']
            results = classifier.classify(A)
            end = time.time()
            execution_time.append(end - start)

            answer_id = 0
            if len(results) == 0:
                # That should not happen. Threshold of maximum_dtw might be too
                # high.
                logging.debug("Raw_data_id = %i as testdata got no results" %
                              testdata['handwriting'].raw_data_id)
                # Set it to trash class in this case
                answer_id = 1
                results = [{'formula_id': {'formula_id': 1, 'p': 1}}]
            else:
                answer_id = results[0]['formula_id']['formula_id']

            if answer_id == testdata['handwriting'].formula_id:
                classification_accuracy[testset]['correct'] += 1
                classification_accuracy[testset]['c10'] += 1
            else:
                classification_accuracy[testset]['wrong'] += 1
                logging.warning(("Raw-data-ID: %i; "
                                 "Formula-ID: %i; Hypothesis: %i, "
                                 "Percentage: %0.3f") %
                                (testdata['handwriting'].raw_data_id,
                                 testdata['handwriting'].formula_id,
                                 answer_id,
                                 results[0]['p'])) # TODO: that might be wrong
            if testdata['handwriting'].formula_id in \
               [r['formula_id']['formula_id'] for r in results]:
                classification_accuracy[testset]['c10'] += 1
            else:
                classification_accuracy[testset]['w10'] += 1
            if i > 0 and i % 100 == 0:
                # Show how much work was done / how much work is remaining
                percentage_done = float(i)/len(cv[testset])
                current_running_time = time.time() - start_time
                remaining_seconds = current_running_time / percentage_done
                tmp = datetime.timedelta(seconds=remaining_seconds)
                sys.stdout.write("\r%0.2f%% (%s remaining)   " %
                                 (percentage_done*100, str(tmp)))
                sys.stdout.flush()

        classification_accuracy[testset]['accuracy'] = \
            (float(classification_accuracy[testset]['correct']) /
             (classification_accuracy[testset]['correct']
              + classification_accuracy[testset]['wrong']))
        classification_accuracy[testset]['a10'] = \
            (float(classification_accuracy[testset]['c10']) /
             (classification_accuracy[testset]['c10']
              + classification_accuracy[testset]['w10']))
        print(classification_accuracy[testset])
        print("\n")
        logging.info("Average time:")
        logging.info(sum(execution_time)/len(execution_time))

    logging.info(classification_accuracy)

    t1sum = 0
    t10sum = 0

    for testset in range(K_FOLD):
        t1sum += classification_accuracy[testset]['accuracy']
        t10sum += classification_accuracy[testset]['a10']

    print_experiment_parameters(symbols, symbol_counter, raw_data_counter,
                                EPSILON, CENTER, THRESHOLD,
                                SPACE_EVENLY, SPACE_EVENLY_KIND, POINTS,
                                K_FOLD, t1sum, t10sum, execution_time)


def is_valid_file(parser, arg):
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
                        default=("/var/www/write-math/archive/"
                                 "handwriting_datasets-2014-08-01.pickle"))
    args = parser.parse_args()

    yamlconfigfile = "/var/www/write-math/website/clients/python/db.config.yml"
    with open(yamlconfigfile, 'r') as ymlfile:
        cfg = yaml.load(ymlfile)
    logging.info("Started selftest of classifier %s." % CLASSIFIER_NAME)
    crossvalidation(args.handwriting_datasets)

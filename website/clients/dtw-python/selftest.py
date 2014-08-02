#!/usr/bin/env python

from __future__ import print_function
import logging
import MySQLdb
import MySQLdb.cursors
import time
import datetime
import sys
import yaml
sys.path.append("/var/www/write-math/website/clients/python")
from HandwrittenData import HandwrittenData  # Needed because of pickle
import preprocessing
import dtw_classifier

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


def crossvalidation():
    # Parameters for self-testing
    MIN_OCCURENCES = 10
    K_FOLD = 10
    EPSILON = 10
    CENTER = False
    THRESHOLD = 20
    SPACE_EVENLY = True
    SPACE_EVENLY_KIND = 'linear'
    POINTS = 100  # Does only make sense with SPACE_EVENLY=True

    # Prepare crossvalidation data set
    cv = [[], [], [], [], [], [], [], [], [], []]

    sql = ("SELECT id, formula_in_latex FROM `wm_formula` "
           "WHERE is_important = 1 ")
           "AND id < 35")  # TODO: Remove this line as soon as possible
    cursor.execute(sql)
    datasets = cursor.fetchall()

    symbol_counter = 0
    raw_data_counter = 0
    symbols = []

    # Define which preprocessing methods will get applied
    preprocessing_queue = []
    if EPSILON > 0:
        preprocessing_queue.append((preprocessing.douglas_peucker,
                                   {'EPSILON': EPSILON}))
    if SPACE_EVENLY:
        preprocessing_queue.append((preprocessing.space_evenly,
                                   {'number': 100,
                                    'kind': SPACE_EVENLY_KIND}))
    preprocessing_queue.append((preprocessing.scale_and_shift, []))

    for dataset in datasets:
        sql = ("SELECT id, data FROM `wm_raw_draw_data` "
               "WHERE `accepted_formula_id` = %s" % str(dataset['id']))
        cursor.execute(sql)
        raw_datasets = cursor.fetchall()
        if len(raw_datasets) >= MIN_OCCURENCES:
            symbol_counter += 1
            symbols.append("%s (%i)" % (dataset['formula_in_latex'],
                                        len(raw_datasets)))
            print("Get %s (datasets: %i) from server ..." %
                  (dataset['formula_in_latex'], len(raw_datasets)))
            i = 0
            for raw_data in raw_datasets:
                raw_data_counter += 1
                tmp = HandwrittenData(raw_data['data'],
                                      dataset['id'],
                                      raw_data['id'])
                tmp.preprocessing(preprocessing_queue)
                cv[i].append({'handwriting': tmp,
                              'formula_in_latex': dataset['formula_in_latex']
                              })
                i = (i + 1) % K_FOLD

    print_experiment_parameters(symbols, symbol_counter, raw_data_counter,
                                EPSILON, CENTER, THRESHOLD,
                                SPACE_EVENLY, SPACE_EVENLY_KIND, POINTS,
                                K_FOLD)

    # Start getting validation results
    classification_accuracy = []
    print("\n\n")
    print("Start validation ...")
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

        for testdata in cv[testset]:
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
                              testdata['id'])
            else:
                answer_id = results[0]['formula_id']['formula_id']

            if answer_id == testdata['handwriting'].formula_id:
                classification_accuracy[testset]['correct'] += 1
                classification_accuracy[testset]['c10'] += 1
            else:
                classification_accuracy[testset]['wrong'] += 1
                logging.warning(("Raw-data-ID: %i; "
                                 "Formula-ID: %i; Hypothesis: %i, Percentage: %0.3f") %
                                (testdata['handwriting'].raw_data_id,
                                 testdata['handwriting'].formula_id,
                                 answer_id,
                                 results[0]['p'])) # TODO: that might be wrong
            if testdata['handwriting'].formula_id in [r['formula_id']['formula_id'] for r in results]:
                classification_accuracy[testset]['c10'] += 1
            else:
                classification_accuracy[testset]['w10'] += 1

            print('|', end="")
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
        print("Average time:")
        print(sum(execution_time)/len(execution_time))

    print(classification_accuracy)

    t1sum = 0
    t10sum = 0

    for testset in range(K_FOLD):
        t1sum += classification_accuracy[testset]['accuracy']
        t10sum += classification_accuracy[testset]['a10']

    print_experiment_parameters(symbols, symbol_counter, raw_data_counter,
                                EPSILON, CENTER, THRESHOLD,
                                SPACE_EVENLY, SPACE_EVENLY_KIND, POINTS,
                                K_FOLD, t1sum, t10sum, execution_time)

if __name__ == '__main__':
    logging.basicConfig(filename='selftest.log',
                        level=logging.DEBUG,
                        format='%(asctime)s %(levelname)s: %(message)s')

    yamlconfigfile = "/var/www/write-math/website/clients/python/db.config.yml"
    with open(yamlconfigfile, 'r') as ymlfile:
        cfg = yaml.load(ymlfile)

    logging.info("Started selftest of classifier %s." % CLASSIFIER_NAME)
    logging.info("start establishing connection")
    connection = MySQLdb.connect(host=cfg['mysql_online']['host'],
                                 user=cfg['mysql_online']['user'],
                                 passwd=cfg['mysql_online']['passwd'],
                                 db=cfg['mysql_online']['db'],
                                 cursorclass=MySQLdb.cursors.DictCursor)
    cursor = connection.cursor()
    logging.info("end establishing connection")
    crossvalidation()

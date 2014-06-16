#!/usr/bin/env python

from __future__ import print_function
import logging
import MySQLdb
import MySQLdb.cursors
from classification import *
from dbconfig import mysql
import time
import datetime
import sys


def crossvalidation():
    # Parameters for self-testing
    MIN_OCCURENCES = 10
    K_FOLD = 10
    EPSILON = 10
    CENTER = False
    FLATTEN = False
    THRESHOLD = 20
    SPACE_EVENLY = True
    SPACE_EVENLY_KIND = 'cubic'
    POINTS = 100  # Does only make sense with SPACE_EVENLY=True

    # Prepare crossvalidation data set
    cv = [[], [], [], [], [], [], [], [], [], []]

    sql = "SELECT id, formula_in_latex FROM `wm_formula`"
    cursor.execute(sql)
    datasets = cursor.fetchall()

    symbol_counter = 0
    raw_data_counter = 0
    symbols = []

    for dataset in datasets:
        sql = ("SELECT id, data FROM `wm_raw_draw_data` "
               "WHERE `accepted_formula_id` = %s" % str(dataset['id']))
        cursor.execute(sql)
        raw_datasets = cursor.fetchall()
        if len(raw_datasets) >= MIN_OCCURENCES:
            symbol_counter += 1
            symbols.append(dataset['formula_in_latex'])
            print("%s (%i)" % (dataset['formula_in_latex'], len(raw_datasets)))
            i = 0
            for raw_data in raw_datasets:
                raw_data_counter += 1
                cv[i].append({'data': raw_data['data'],
                              'id': raw_data['id'],
                              'formula_id': dataset['id'],
                              'accepted_formula_id': dataset['id'],
                              'formula_in_latex': dataset['formula_in_latex']
                              })
                i = (i + 1) % K_FOLD

    ###
    print("\n" + "-"*80)
    print(str(datetime.date.today()))
    print("The following %i symbols were evaluated:" % symbol_counter)
    print(", ".join(symbols))
    print("raw datasets: %i" % raw_data_counter)
    print("Epsilon: %0.2f" % EPSILON)
    print("Center: %r" % CENTER)
    print("Squared quadratic: False")
    print("Flatten: %r" % FLATTEN)
    print("Threshold: %r" % THRESHOLD)
    if SPACE_EVENLY:
        print("Space evenly: %r (%i points, %s)" % (SPACE_EVENLY, POINTS, SPACE_EVENLY_KIND))
    else:
        print("Space evenly: %r" % SPACE_EVENLY)
    ###

    # Start getting validation results
    classification_accuracy = []
    print("\n\n")
    execution_time = []

    for testset in range(K_FOLD):
        classification_accuracy.append({'correct': 0,
                                        'wrong': 0,
                                        'c10': 0,
                                        'w10': 0})
        for testdata in cv[testset]:
            start = time.time()
            raw_draw_data = testdata['data']
            A = pointLineList(raw_draw_data)
            if EPSILON > 0:
                A = douglas_peucker(A, EPSILON)

            if SPACE_EVENLY:
                Anew = []
                for line in A:
                    Anew.append(space_evenly(line, POINTS, SPACE_EVENLY_KIND))
                A = Anew

            A = scale_and_center(A, CENTER)

            if FLATTEN:
                A = list_of_pointlists2pointlist(A)

            # Prepare datasets the algorithm may use
            datasets = []
            for key, value in enumerate(cv):
                if key != testset:
                    datasets += value
            results = classify(datasets, A, EPSILON, THRESHOLD, FLATTEN,
                               SPACE_EVENLY, POINTS)
            end = time.time()
            execution_time.append(end - start)

            answer_id = 0
            if len(results) == 0:
                # That should not happen. Threshold of maximum_dtw might be too
                # high.
                logging.debug("Raw_data_id = %i as testdata got no results" %
                              testdata['id'])
            else:
                answer_id = results[0]['formula_id']

            if answer_id == testdata['formula_id']:
                classification_accuracy[testset]['correct'] += 1
            else:
                classification_accuracy[testset]['wrong'] += 1
                logging.warning(("Got raw_data_id %i wrong. "
                                 "It is %i, but I thought it would be %i.") %
                                (testdata['id'],
                                 testdata['formula_id'],
                                 answer_id))

            if testdata['formula_id'] in [r['formula_id'] for r in results]:
                classification_accuracy[testset]['c10'] += 1
            else:
                classification_accuracy[testset]['w10'] += 1

            print('|', end="")
            sys.stdout.flush()

        classification_accuracy[testset]['accuracy'] = (float(classification_accuracy[testset]['correct']) / (classification_accuracy[testset]['correct'] + classification_accuracy[testset]['wrong']))
        classification_accuracy[testset]['a10'] = float(classification_accuracy[testset]['c10']) / (classification_accuracy[testset]['c10'] + classification_accuracy[testset]['w10'])
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

    print("\n" + "-"*80)
    print(str(datetime.date.today()))
    print("The following %i symbols were evaluated:" % symbol_counter)
    print(", ".join(symbols))
    print("raw datasets: %i" % raw_data_counter)
    print("Epsilon: %0.2f" % EPSILON)
    print("Center: %r" % CENTER)
    print("Squared quadratic: False")
    print("Flatten: %r" % FLATTEN)
    print("Threshold: %r" % THRESHOLD)
    if SPACE_EVENLY:
        print("Space evenly: %r (%i points, %s)" % (SPACE_EVENLY, POINTS, SPACE_EVENLY_KIND))
    else:
        print("Space evenly: %r" % SPACE_EVENLY)
    print("* Top-1-Classification (%i-fold cross-validated): %0.5f" % (K_FOLD, (t1sum/K_FOLD)))
    print("* Top-10-Classification (%i-fold cross-validated): %0.5f" % (K_FOLD, t10sum/K_FOLD))
    print("Average time: %.5f seconds" % (sum(execution_time)/len(execution_time)))

if __name__ == '__main__':
    logging.basicConfig(filename='selftest.log',
                        level=logging.DEBUG,
                        format='%(asctime)s %(levelname)s: %(message)s')

    logging.info("Started selftest of classifier %s." % CLASSIFIER_NAME)
    logging.info("start establishing connection")
    connection = MySQLdb.connect(host=mysql['host'],
                                 user=mysql['user'],
                                 passwd=mysql['passwd'],
                                 db=mysql['db'],
                                 cursorclass=MySQLdb.cursors.DictCursor)
    cursor = connection.cursor()
    logging.info("end establishing connection")
    crossvalidation()

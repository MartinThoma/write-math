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


def print_experiment_parameters(symbols, symbol_counter, raw_data_counter,
                                EPSILON, CENTER, FLATTEN, THRESHOLD,
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
    print("Flatten: %r" % FLATTEN)
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
            symbols.append("%s (%i)" % (dataset['formula_in_latex'],
                                        len(raw_datasets)))
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

    print_experiment_parameters(symbols, symbol_counter, raw_data_counter,
                                EPSILON, CENTER, FLATTEN, THRESHOLD,
                                SPACE_EVENLY, SPACE_EVENLY_KIND, POINTS,
                                K_FOLD)

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
            raw_draw_data = testdata['data']
            A = pointLineList(raw_draw_data)
            if EPSILON > 0:
                A = douglas_peucker(A, EPSILON)

            print("lines: %i, points: %i" % (len(A),
                                             sum([len(line) for line in A])
                                             )
                  )

            print('|', end="")
            sys.stdout.flush()

        print("\n")

    print(classification_accuracy)

    t1sum = 0
    t10sum = 0

    for testset in range(K_FOLD):
        t1sum += classification_accuracy[testset]['accuracy']
        t10sum += classification_accuracy[testset]['a10']

    print_experiment_parameters(symbols, symbol_counter, raw_data_counter,
                                EPSILON, CENTER, FLATTEN, THRESHOLD,
                                SPACE_EVENLY, SPACE_EVENLY_KIND, POINTS,
                                K_FOLD, t1sum, t10sum, execution_time)

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

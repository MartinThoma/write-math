#!/usr/bin/env python
# -*- coding: utf-8 -*-

from __future__ import print_function

# Other
import logging
import MySQLdb
import MySQLdb.cursors
from classification import pointLineList, douglas_peucker, space_evenly, \
    scale_and_center
from dbconfig import mysql
import datetime
from collections import defaultdict

import os
import cPickle as pickle

logging.basicConfig(filename='selftest.log',
                    level=logging.INFO,
                    format='%(asctime)s %(levelname)s: %(message)s')


def make_pfile(filename, features, data):
    input_filename = os.path.abspath("%s.raw" % filename)
    output_filename = os.path.abspath(filename)
    with open(input_filename, "w") as f:
        for symbolnr, instance in enumerate(data):
            feature_string, label = instance
            feature_string = " ".join(map(str, feature_string))
            line = "%i 0 %s %i" % (symbolnr, feature_string, label)
            print(line, file=f)
    os.system("pfile_create -i %s -f %i -l 1 -o %s.pfile" % (input_filename,
                                                             features,
                                                             output_filename))
    os.remove(input_filename)


def get_features(raw_draw_data, EPSILON, SPACE_EVENLY, POINTS_PER_LINE,
                 SPACE_EVENLY_KIND, CENTER):
    """
    Get a list of real-numbered values. Those values will be used for training
    and evaluating.
    """
    A = pointLineList(raw_draw_data)
    if EPSILON > 0:
        A = douglas_peucker(A, EPSILON)

    if SPACE_EVENLY:
        Anew = []
        for line in A:
            Anew.append(space_evenly(line, POINTS_PER_LINE, SPACE_EVENLY_KIND))
        A = Anew

    A = scale_and_center(A, CENTER)

    features = [len(A)]
    for line in range(4):
        for point in range(POINTS_PER_LINE):
            if line >= len(A):
                features.append(0)
                features.append(0)
            else:
                if point >= len(A[line]):
                    features.append(0)
                    features.append(0)
                else:
                    features.append(A[line][point]['x'])
                    features.append(A[line][point]['y'])

    return features


def print_parameters(symbol_counter, raw_data_counter, EPSILON, CENTER,
                     FLATTEN, THRESHOLD, SPACE_EVENLY, POINTS_PER_LINE,
                     SPACE_EVENLY_KIND, K_FOLD, symbols):
    print("\n" + "-"*80)
    print(str(datetime.date.today()))
    print("\n```")
    print("### Dataset information ###")
    print("The following %i symbols were evaluated:" % symbol_counter)
    for symbol, counter in sorted(symbols.items()):
        if symbol in ['A', '0', 'a']:
            print("")
        print("%s (%i)" % (symbol, counter), end=", ")
        if symbol in ['Z', '9', 'z']:
            print("")
    print("")
    print("raw datasets: %i" % raw_data_counter)
    print("### Preprocessing Parameters ###")
    print("Epsilon: %0.2f" % EPSILON)
    print("Center: %r" % CENTER)
    print("Squared quadratic: False")
    print("Flatten: %r" % FLATTEN)
    print("Threshold: %r" % THRESHOLD)
    if SPACE_EVENLY:
        print("Space evenly: %r (%i points, %s)" %
              (SPACE_EVENLY, POINTS_PER_LINE, SPACE_EVENLY_KIND))
    else:
        print("Space evenly: %r" % SPACE_EVENLY)
    print("```")


def get_binned_data(EPSILON, SPACE_EVENLY, POINTS_PER_LINE, SPACE_EVENLY_KIND,
                    CENTER, K_FOLD=10, MIN_OCCURENCES=10):
    """
    Get ten bins of labeled training data. Those bins are guaranteed to have a
    similar number of training instances per symbol.

    Each bin is a list of (input_features, class_name) tuples, where class_name
    is an integer starting at 0.
    """

    if os.path.isfile('databins.pickle'):
        data = pickle.load(open('databins.pickle'))
    else:
        # Prepare 10-fold crossvalidation data set
        cv = []
        for i in range(K_FOLD):
            cv.append([])

        # Get datasets from database
        sql = "SELECT id, formula_in_latex FROM `wm_formula`"
        cursor.execute(sql)
        datasets = cursor.fetchall()

        symbol_counter = 0
        raw_data_counter = 0
        symbols = defaultdict(int)
        index2symbol = []
        symbol2index = {}

        for dataset in datasets:
            sql = ("SELECT id, data FROM `wm_raw_draw_data` "
                   "WHERE `accepted_formula_id` = %s" % str(dataset['id']))
            cursor.execute(sql)
            raw_datasets = cursor.fetchall()
            if len(raw_datasets) >= MIN_OCCURENCES:
                index2symbol.append(dataset['id'])
                symbol2index[dataset['id']] = len(index2symbol) - 1
                symbol_counter += 1
                print("%s (%i)" % (dataset['formula_in_latex'],
                                   len(raw_datasets)))
                i = 0
                for raw_data in raw_datasets:
                    raw_data_counter += 1
                    symbols[dataset['formula_in_latex']] += 1
                    x = get_features(raw_data['data'], EPSILON, SPACE_EVENLY,
                                     POINTS_PER_LINE, SPACE_EVENLY_KIND,
                                     CENTER)
                    y = symbol2index[dataset['id']]
                    cv[i].append((x, y))
                    i = (i + 1) % K_FOLD
        data = {'cv': cv,
                'symbol_counter': symbol_counter,
                'raw_data_counter': raw_data_counter,
                'symbols': symbols}
        pickle.dump(data, open("databins.pickle", "wb"))
    return data


def create_pfile(POINTS_PER_LINE=20,
                 MIN_OCCURENCES=10, K_FOLD=10, EPSILON=10,
                 CENTER=False, THRESHOLD=20,
                 SPACE_EVENLY_KIND='cubic', LEARNING_RATE=0.01,
                 LEARNING_RATE_DECAY=1.0, EPOCHS=20):
    # Parameters for self-testing
    FLATTEN = False
    SPACE_EVENLY = True

    tmp = get_binned_data(EPSILON, SPACE_EVENLY, POINTS_PER_LINE,
                          SPACE_EVENLY_KIND, CENTER, K_FOLD,
                          MIN_OCCURENCES)
    cv = tmp['cv']
    symbol_counter = tmp['symbol_counter']
    raw_data_counter = tmp['raw_data_counter']
    symbols = tmp['symbols']

    print_parameters(symbol_counter, raw_data_counter, EPSILON, CENTER,
                     FLATTEN, THRESHOLD, SPACE_EVENLY, POINTS_PER_LINE,
                     SPACE_EVENLY_KIND, K_FOLD, symbols)

    # Start getting validation results
    c_acc = []
    print("\n\n")

    # Maximum of 4 lines and 2 coordinates (x and y) per line
    INPUT_FEATURES = 4*POINTS_PER_LINE*2 + 1

    for testset in range(K_FOLD):
        c_acc.append({'correct': 0,
                      'wrong': 0,
                      'c10': 0,
                      'w10': 0})
        # Prepare datasets the algorithm may use
        datasets = []
        for key, data_bin in enumerate(cv):
            if key != testset:
                datasets += data_bin

        print("Start training dataset generation")
        trndata = []
        for x, y in datasets:
            trndata.append((x, y))
        make_pfile("trndata-%i" % testset, INPUT_FEATURES, trndata)
        print("end training dataset generation")
        print("testdata")
        tstdata = []
        for x, y in cv[testset]:
            tstdata.append((x, y))
        make_pfile("tstdata-%i" % testset, INPUT_FEATURES, tstdata)
        print("end testdata")

    print_parameters(symbol_counter, raw_data_counter, EPSILON, CENTER,
                     FLATTEN, THRESHOLD, SPACE_EVENLY, POINTS_PER_LINE,
                     SPACE_EVENLY_KIND, K_FOLD, symbols)

if __name__ == '__main__':
    logging.info("Started creation of pfiles.")
    logging.info("start establishing connection")
    connection = MySQLdb.connect(host=mysql['host'],
                                 user=mysql['user'],
                                 passwd=mysql['passwd'],
                                 db=mysql['db'],
                                 cursorclass=MySQLdb.cursors.DictCursor)
    cursor = connection.cursor()
    logging.info("end establishing connection")

    from argparse import ArgumentParser, ArgumentDefaultsHelpFormatter

    parser = ArgumentParser(formatter_class=ArgumentDefaultsHelpFormatter)

    parser.add_argument("-P", metavar="POINTS", type=int,
                        dest="points_per_line", default=20,
                        help="number of points per stroke")
    args = parser.parse_args()

    MIN_OCCURENCES = 10
    K_FOLD = 10
    EPSILON = 10
    CENTER = False
    THRESHOLD = 20
    create_pfile(args.points_per_line, MIN_OCCURENCES, K_FOLD, EPSILON,
                 CENTER, THRESHOLD, 'cubic')

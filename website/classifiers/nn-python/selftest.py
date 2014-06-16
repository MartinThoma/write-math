#!/usr/bin/env python
# -*- coding: utf-8 -*-

from __future__ import print_function

# Source: http://pybrain.org/docs/tutorial/fnn.html
from pybrain.datasets import ClassificationDataSet
from pybrain.utilities import percentError
from pybrain.tools.shortcuts import buildNetwork
from pybrain.supervised.trainers import BackpropTrainer
from pybrain.structure.modules import SoftmaxLayer

# Other
import logging
import MySQLdb
import MySQLdb.cursors
from classification import pointLineList, douglas_peucker, space_evenly, \
    scale_and_center
from dbconfig import mysql
import time
import datetime
import sys
from collections import defaultdict


logging.basicConfig(filename='selftest.log',
                    level=logging.INFO,
                    format='%(asctime)s %(levelname)s: %(message)s')

CLASSIFIER_NAME = 'python-nn'


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


def get_binned_data(EPSILON, SPACE_EVENLY, POINTS_PER_LINE, SPACE_EVENLY_KIND,
                    CENTER, K_FOLD=10, MIN_OCCURENCES=10):
    """
    Get ten bins of labeled training data. Those bins are guaranteed to have a
    similar number of training instances per symbol.

    Each bin is a list of (input_features, class_name) tuples, where class_name
    is an integer starting at 0.
    """

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
            symbols[dataset['formula_in_latex']] += 1
            print("%s (%i)" % (dataset['formula_in_latex'], len(raw_datasets)))
            i = 0
            for raw_data in raw_datasets:
                raw_data_counter += 1
                # cv[i].append({'data': raw_data['data'],
                #               'id': raw_data['id'],
                #               'formula_id': dataset['id'],
                #               'accepted_formula_id': dataset['id'],
                #               'formula_in_latex': dataset['formula_in_latex']
                #               })
                x = get_features(raw_data['data'], EPSILON, SPACE_EVENLY,
                                 POINTS_PER_LINE, SPACE_EVENLY_KIND,
                                 CENTER)
                y = symbol2index[dataset['id']]
                cv[i].append((x, y))
                i = (i + 1) % K_FOLD
    return {'cv': cv,
            'symbol_counter': symbol_counter,
            'raw_data_counter': raw_data_counter,
            'symbols': symbols}


def crossvalidation(hidden_neurons, weightdecay, momentum):
    """ Start a 10-fold cross-validation. """
    # Parameters for self-testing
    MIN_OCCURENCES = 10
    K_FOLD = 10
    EPSILON = 10
    CENTER = False
    FLATTEN = False
    THRESHOLD = 20
    SPACE_EVENLY = True
    SPACE_EVENLY_KIND = 'cubic'
    POINTS_PER_LINE = 20  # Does only make sense with SPACE_EVENLY=True

    tmp = get_binned_data(EPSILON, SPACE_EVENLY, POINTS_PER_LINE,
                          SPACE_EVENLY_KIND, CENTER, K_FOLD,
                          MIN_OCCURENCES)
    cv = tmp['cv']
    symbol_counter = tmp['symbol_counter']
    raw_data_counter = tmp['raw_data_counter']
    symbols = tmp['symbols']

    ###
    print("\n" + "-" * 80)
    print(str(datetime.date.today()))
    print("The following %i symbols were evaluated:" % symbol_counter)
    symbolstring = ""
    for el, counter in symbols.items():
        symbolstring += ("%s (%i)" % (el, counter))
    print("raw datasets: %i" % raw_data_counter)
    print("Epsilon: %0.2f" % EPSILON)
    print("Center: %r" % CENTER)
    print("Squared quadratic: False")
    print("Flatten: %r" % FLATTEN)
    print("Threshold: %r" % THRESHOLD)
    if SPACE_EVENLY:
        print("Space evenly: %r (%i points, %s)" % (SPACE_EVENLY,
                                                    POINTS_PER_LINE,
                                                    SPACE_EVENLY_KIND))
    else:
        print("Space evenly: %r" % SPACE_EVENLY)

    # Start getting validation results
    c_acc = []
    print("\n\n")
    execution_time = []

    INPUT_FEATURES = 4*POINTS_PER_LINE*2 + 1
    CLASSES = symbol_counter
    HIDDEN_NEURONS = hidden_neurons
    WEIGHTDECAY = weightdecay
    MOMENTUM = momentum

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
        trndata = ClassificationDataSet(INPUT_FEATURES, 1,
                                        nb_classes=CLASSES)
        for x, y in datasets:
            trndata.addSample(x, [y])
        print("end training dataset generation")
        print("testdata")
        tstdata = ClassificationDataSet(INPUT_FEATURES, 1,
                                        nb_classes=CLASSES)
        for x, y in cv[testset]:
            tstdata.addSample(x, [y])
        print("end testdata")

        # This is necessary, but I don't know why
        # See http://stackoverflow.com/q/8154674/562769
        trndata._convertToOneOfMany()
        tstdata._convertToOneOfMany()

        fnn = buildNetwork(trndata.indim, HIDDEN_NEURONS, trndata.outdim,
                           outclass=SoftmaxLayer)

        trainer = BackpropTrainer(fnn, dataset=trndata, momentum=MOMENTUM,
                                  verbose=True, weightdecay=WEIGHTDECAY)

        print("start traing")
        for i in range(20):
            trainer.trainEpochs(1)
            trnresult = percentError(trainer.testOnClassData(),
                                     trndata['class'])
            tstresult = percentError(trainer.testOnClassData(
                                     dataset=tstdata), tstdata['class'])

            print("epoch: %4d" % trainer.totalepochs,
                  "  train error: %5.2f%%" % trnresult,
                  "  test error: %5.2f%%" % tstresult)
        print("end training")

        for x, y in cv[testset]:
            start = time.time()
            # Classify
            results = fnn.activate(x)
            topIndices = (-results).argsort()
            indexTop1 = topIndices[0]
            indexTop10 = topIndices[:10]
            end = time.time()
            execution_time.append(end - start)

            if indexTop1 == y:
                c_acc[testset]['correct'] += 1
            else:
                c_acc[testset]['wrong'] += 1

            if y in indexTop10:
                c_acc[testset]['c10'] += 1
            else:
                c_acc[testset]['w10'] += 1

            print('|', end="")
            sys.stdout.flush()

        c_acc[testset]['accuracy'] = (float(c_acc[testset]['correct']) /
                                     (c_acc[testset]['correct']
                                      + c_acc[testset]['wrong']))
        c_acc[testset]['a10'] = (float(c_acc[testset]['c10']) /
                                 (c_acc[testset]['c10']
                                  + c_acc[testset]['w10']))
        print(c_acc[testset])
        print("\n")
        print("Average time:")
        print(sum(execution_time)/len(execution_time))

    print(c_acc)

    t1sum = 0
    t10sum = 0

    for testset in range(K_FOLD):
        t1sum += c_acc[testset]['accuracy']
        t10sum += c_acc[testset]['a10']

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
        print("Space evenly: %r (%i points, %s)" %
              (SPACE_EVENLY, POINTS_PER_LINE, SPACE_EVENLY_KIND))
    else:
        print("Space evenly: %r" % SPACE_EVENLY)
    print("* Top-1-Classification (%i-fold cross-validated): %0.5f" %
          (K_FOLD, (t1sum/K_FOLD)))
    print("* Top-10-Classification (%i-fold cross-validated): %0.5f" %
          (K_FOLD, t10sum/K_FOLD))
    print("Hidden neurons: %i" % HIDDEN_NEURONS)
    print("Momentum: %.5f" % MOMENTUM)
    print("weightdecay: %.5f" % WEIGHTDECAY)
    print("Average time: %.5f seconds" % (sum(execution_time) /
                                          len(execution_time)))

if __name__ == '__main__':
    logging.info("Started selftest of classifier %s." % CLASSIFIER_NAME)
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

    # Add more options if you like
    parser.add_argument("-H", metavar="H", type=int, dest="hidden_neurons",
                        default=5,
                        help="number of neurons in the hidden layer")
    parser.add_argument("-d", metavar="W", type=float, dest="weightdecay",
                        default=0.01,
                        help="weightdecay")
    parser.add_argument("-m", metavar="M", type=float, dest="momentum",
                        default=0.1,
                        help="momentum")
    args = parser.parse_args()

    crossvalidation(args.hidden_neurons, args.weightdecay, args.momentum)

#!/usr/bin/env python
# -*- coding: utf-8 -*-

from __future__ import print_function

# Source: http://pybrain.org/docs/tutorial/fnn.html
from pybrain.datasets import ClassificationDataSet
from pybrain.utilities import percentError
from pybrain.tools.shortcuts import buildNetwork
from pybrain.supervised.trainers import BackpropTrainer
from pybrain.structure.modules import SoftmaxLayer

# Only needed for data generation and graphical output
from pylab import ion, ioff, figure, draw, contourf, clf, show, plot
from scipy import diag, arange, meshgrid, where
from numpy.random import multivariate_normal
from random import normalvariate

# Other
import logging
import MySQLdb
import MySQLdb.cursors
from classification import pointLineList, douglas_peucker, space_evenly, \
    scale_and_center, list_of_pointlists2pointlist
from dbconfig import mysql
import time
import datetime
import sys

CLASSIFIER_NAME = 'python-nn'

def get_features(raw_draw_data, EPSILON, SPACE_EVENLY, POINTS_PER_LINE,
                 SPACE_EVENLY_KIND, CENTER):
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


def crossvalidation(hidden_neurons, weightdecay, momentum):
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

    # Prepare crossvalidation data set
    cv = [[], [], [], [], [], [], [], [], [], []]

    sql = "SELECT id, formula_in_latex FROM `wm_formula`"
    cursor.execute(sql)
    datasets = cursor.fetchall()

    symbol_counter = 0
    raw_data_counter = 0
    symbols = []
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
        print("Space evenly: %r (%i points, %s)" % (SPACE_EVENLY, POINTS_PER_LINE, SPACE_EVENLY_KIND))
    else:
        print("Space evenly: %r" % SPACE_EVENLY)
    ###

    # Start getting validation results
    classification_accuracy = []
    print("\n\n")
    execution_time = []

    INPUT_FEATURES = 4*POINTS_PER_LINE*2 + 1
    CLASSES = symbol_counter
    HIDDEN_NEURONS = hidden_neurons
    WEIGHTDECAY = weightdecay
    MOMENTUM = momentum

    for testset in range(K_FOLD):
        classification_accuracy.append({'correct': 0,
                                        'wrong': 0,
                                        'c10': 0,
                                        'w10': 0})
        # Prepare datasets the algorithm may use
        datasets = []
        for key, value in enumerate(cv):
            if key != testset:
                datasets += value

        print("Start training dataset generation")
        trndata = ClassificationDataSet(INPUT_FEATURES, 1,
                                        nb_classes=CLASSES)
        for data in datasets:
            klass = symbol2index[data['formula_id']]
            features = get_features(data['data'], EPSILON, SPACE_EVENLY,
                                    POINTS_PER_LINE, SPACE_EVENLY_KIND,
                                    CENTER)
            trndata.addSample(features, [klass])
        print("end training dataset generation")
        print("testdata")
        tstdata = ClassificationDataSet(INPUT_FEATURES, 1,
                                        nb_classes=CLASSES)
        for data in cv[testset]:
            klass = symbol2index[data['formula_id']]
            features = get_features(data['data'], EPSILON, SPACE_EVENLY,
                                    POINTS_PER_LINE, SPACE_EVENLY_KIND,
                                    CENTER)
            tstdata.addSample(features, [klass])
        print("end testdata")

        trndata._convertToOneOfMany()  # This is necessary, but I don't know why
        tstdata._convertToOneOfMany()  # http://stackoverflow.com/q/8154674/562769

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

        for testdata in cv[testset]:
            start = time.time()
            x = get_features(testdata['data'], EPSILON, SPACE_EVENLY,
                                    POINTS_PER_LINE, SPACE_EVENLY_KIND,
                                    CENTER)
            # Classify
            results = fnn.activate(x)
            topIndices = (-results).argsort()
            indexTop1 = topIndices[0]
            indexTop10 = topIndices[:10]

            print("Number of training patterns: %i" % len(trndata))
            print("Input and output dimensions: %i, %i" % (trndata.indim,
                                                           trndata.outdim))
            print("Hidden neurons: %i" % HIDDEN_NEURONS)
            print("First sample (input, target, class):")

            end = time.time()
            execution_time.append(end - start)

            answer_id = -1
            if len(results) == 0:
                # That should not happen. Threshold of maximum_dtw might be too
                # high.
                logging.debug("Raw_data_id = %i as testdata got no results" %
                              testdata['id'])
            else:
                answer_id = index2symbol[indexTop1]

            if answer_id == testdata['formula_id']:
                classification_accuracy[testset]['correct'] += 1
            else:
                classification_accuracy[testset]['wrong'] += 1
                logging.warning(("Got raw_data_id %i wrong. "
                                 "It is %i, but I thought it would be %i.") %
                                (testdata['id'],
                                 testdata['formula_id'],
                                 answer_id))

            if testdata['formula_id'] in [index2symbol[r] for r in topIndices]:
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
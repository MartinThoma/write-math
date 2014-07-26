#!/usr/bin/env python
# -*- coding: utf-8 -*-

from __future__ import print_function

# Other
import logging
import os
import cPickle as pickle
import sys
sys.path.append("/var/www/write-math/website/clients/python")
from HandwrittenData import HandwrittenData  # Needed because of pickle
import preprocessing


def make_pfile(filename, features, data):
    """ Create the pfile.
    @param filename name of the file that pfile_create will use to create
                    the pfile.
    @param features integer, number of features
    @param data     list of tuples ('feature_string', 'label')
    """
    input_filename = os.path.abspath("%s.raw" % filename)
    output_filename = os.path.abspath(filename)

    # create raw data file for pfile_create
    with open(input_filename, "w") as f:
        for symbolnr, instance in enumerate(data):
            feature_string, label = instance
            assert len(feature_string) == features, \
                "Expected %i features, got %i features" % \
                (features, len(feature_string))
            feature_string = " ".join(map(str, feature_string))
            line = "%i 0 %s %i" % (symbolnr, feature_string, label)
            print(line, file=f)
    os.system("pfile_create -i %s -f %i -l 1 -o %s.pfile" % (input_filename,
                                                             features,
                                                             output_filename))
    os.remove(input_filename)


def prepare_dataset(dataset, formula_id2index, preprocessing_queue):
    prepared = []

    for data in dataset:
        x = []
        # Prepare features
        handwriting = data['handwriting']

        # Preprocessing
        handwriting.preprocessing(preprocessing_queue)

        # Feature selection
        x.append(len(handwriting.get_pointlist()))  # Number of lines
        # Append points (20 points per line, 4 lines)
        pointlist = handwriting.get_pointlist()
        fill_empty_with = 0
        for line_nr in range(4):
            if line_nr < len(pointlist):
                # if len(pointlist[line_nr]) >= 20:
                #     print("More than 20 points in this list! (%i)" %
                #           len(pointlist[line_nr]))
                #     print("Raw-Data-ID: %r" % data['id'])
                for point_nr in range(20):
                    if point_nr < len(pointlist[line_nr]):
                        x.append(pointlist[line_nr][point_nr]['x'])
                        x.append(pointlist[line_nr][point_nr]['y'])
                    else:
                        x.append(fill_empty_with)
                        x.append(fill_empty_with)
            else:
                for i in range(20):
                    x.append(fill_empty_with)
                    x.append(fill_empty_with)
        # Add label
        y = formula_id2index[data['formula_id']]
        prepared.append((x, y))
    return prepared


def create_pfile():
    path_to_data = '../python/cv_datasets.pickle'
    tmp = pickle.load(open(path_to_data))
    cv = tmp['cv']
    formula_id2index = tmp['formula_id2index']

    test_set = cv[0]
    validation_set = cv[1]
    training_set = []
    for i in range(2, len(cv)):
        training_set += cv[i]

    preprocessing_queue = [(preprocessing.scale_and_shift, []),
                           (preprocessing.connect_lines, []),
                           (preprocessing.douglas_peucker,
                            {'EPSILON': 0.2}),
                           (preprocessing.space_evenly,
                            {'number': 100,
                             'KIND': 'cubic'})
                           ]

    print("Classes (nr of symbols): %i" % len(formula_id2index))

    print("#### Preprocessing")
    print("```")
    for algorithm, options in preprocessing_queue:
        print("* %r with %r" % (algorithm, options))
    print("```")


    prepared = prepare_dataset(test_set,
                               formula_id2index,
                               preprocessing_queue)
    INPUT_FEATURES = len(prepared[0][0])

    print("#### Features (%i)" % INPUT_FEATURES)
    print("* Number of lines")
    print("* Points of symbol (maximum of 20 per line, maximum of 4 lines)")
    print("  Empty slots get filled with -1")
    print("## done")

    make_pfile("testdata", INPUT_FEATURES, prepared)
    print("Testdata was written")
    prepared = prepare_dataset(validation_set,
                               formula_id2index,
                               preprocessing_queue)
    make_pfile("validdata", INPUT_FEATURES, prepared)
    print("validdata was written")
    prepared = prepare_dataset(training_set,
                               formula_id2index,
                               preprocessing_queue)
    make_pfile("traindata", INPUT_FEATURES, prepared)
    print("traindata was written")
if __name__ == '__main__':
    logging.info("Started creation of pfiles.")
    create_pfile()

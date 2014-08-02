#!/usr/bin/env python

import yaml
import os
import logging
import sys
sys.path.append("/var/www/write-math/website/clients/python")
import preprocessing
import features

logging.basicConfig(format='%(asctime)s %(levelname)s %(message)s',
                    level=logging.DEBUG,
                    stream=sys.stdout)

"""
Steps include:

1. Get data (.pickle)
2. Split data in train-, validation- and test set (.pfile)
    1. Split data from .pickle file
    2. Run preprocessing
    3. Run feature selection
3. Run Training (d)
"""


def parse_model_yaml(filename):
    with open(filename, 'r') as ymlfile:
        cfg = yaml.load(ymlfile)

    sections = ["data-source", "data", "preprocessing", "features", "model"]

    # Make sure every section in the yaml file is known
    for section in cfg:
        if section not in sections:
            logging.info(("%s in the file %s is not known. "
                          "Please correct the file.") % (section, filename))
            return
        sections.remove(section)

    # Make sure no section is missing
    if len(sections) > 0:
        logging.info(("The following sections were "
                      "not found: %s") % str(sections))
        return

    # Check if data source exists
    if os.path.isfile(cfg['data-source']):
        logging.info("Data file ... exists")
    else:
        logging.error("Data file ... does not exist")

    # Check if training data exists
    if os.path.isfile(cfg['data']['training']):
        logging.info("Training data file ... exists")
    else:
        logging.error("Training data file ... does not exist")

    # Check if training data exists
    if os.path.isfile(cfg['data']['validating']):
        logging.info("Validation data file ... exists")
    else:
        logging.error("Validation data file ... does not exist")

    # Check if testing data exists
    if os.path.isfile(cfg['data']['testing']):
        logging.info("Testing data file ... exists")
    else:
        logging.error("Testing data file ... does not exist")

    # Go through preprocessing algorithms
    preprocessing_queue = []
    for algorithm_name, parameters in cfg['preprocessing'].items():
        algorithm = preprocessing.get_algorithm(algorithm_name)
        if algorithm is None:
            logging.error("Algorithm %s not found." % algorithm_name)
            return
        preprocessing_queue.append((algorithm, parameters))

    # Go through features
    feature_list = []
    for algorithm_name, parameters in cfg['features'].items():
        algorithm = features.get_class(algorithm_name)
        if algorithm is None:
            logging.error("Algorithm %s not found." % algorithm_name)
            return
        if parameters is None:
            feature_list.append(algorithm())
        else:
            parameter_dict = {}
            for el in parameters:
                parameter_dict = dict(parameter_dict.items() + el.items())
            feature_list.append(algorithm(**parameter_dict))

    # Check if testing data exists
    if os.path.isfile(cfg['model']['file']):
        logging.info("model file '%s' ... exists" % cfg['model']['file'])
    else:
        logging.error("model file '%s' ... does not exist" %
                      cfg['model']['file'])

if __name__ == '__main__':
    parse_model_yaml("mlp-370.yml")

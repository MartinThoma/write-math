#!/usr/bin/env python

"""Create preprocessed dataset."""

from __future__ import print_function
import logging
import sys
import os
logging.basicConfig(format='%(asctime)s %(levelname)s %(message)s',
                    level=logging.DEBUG,
                    stream=sys.stdout)
import cPickle as pickle
import time
import preprocessing
import yaml
import utils


def create_preprocessed_dataset(path_to_data, outputpath, preprocessing_queue):
    # Log everything
    logging.info("Data soure %s" % path_to_data)
    logging.info("Output will be stored in %s" % outputpath)
    logging.info("Preprocessing Queue:")
    for el in preprocessing_queue:
        logging.info(el)
    # Load from pickled file
    logging.info("Start loading data...")
    loaded = pickle.load(open(path_to_data))
    raw_datasets = loaded['handwriting_datasets']
    logging.info("Start applying preprocessing methods")
    start_time = time.time()
    for i, raw_dataset in enumerate(raw_datasets):
        if i % 10 == 0 and i > 0:
            utils.print_status(len(raw_datasets), i, start_time)
        # Do the work
        raw_dataset['handwriting'].preprocessing(preprocessing_queue)
    sys.stdout.write("\r%0.2f%% (done)   \n" % (100))
    print("")
    pickle.dump({'handwriting_datasets': raw_datasets,
                 'formula_id2latex': loaded['formula_id2latex'],
                 'preprocessing_queue': preprocessing_queue
                 },
                open(outputpath, "wb"),
                2)


if __name__ == '__main__':
    PROJECT_ROOT = utils.get_project_root()

    # Get latest model description file
    models_folder = os.path.join(PROJECT_ROOT, "archive/models")
    latest_model = utils.get_latest_in_folder(models_folder, ".yml")

    # Get command line arguments
    from argparse import ArgumentParser, ArgumentDefaultsHelpFormatter
    parser = ArgumentParser(description=__doc__,
                            formatter_class=ArgumentDefaultsHelpFormatter)
    parser.add_argument("-m", "--model_description_file",
                        dest="model_description_file",
                        help="where is the model description YAML file?",
                        metavar="FILE",
                        type=lambda x: utils.is_valid_file(parser, x),
                        default=latest_model)
    args = parser.parse_args()

    # Read the model description file
    with open(args.model_description_file, 'r') as ymlfile:
        model_description = yaml.load(ymlfile)
    # Get the path of the raw data
    raw_datapath = os.path.join(PROJECT_ROOT,
                                model_description['data-source'])
    # Get the path were the preprocessed file should be put
    outputpath = os.path.join(PROJECT_ROOT,
                              model_description['preprocessed'])
    # Get the preprocessing queue
    tmp = model_description['preprocessing']
    preprocessing_queue = preprocessing.get_preprocessing_queue(tmp)

    # Do it! Preprcess the data!
    create_preprocessed_dataset(raw_datapath, outputpath, preprocessing_queue)

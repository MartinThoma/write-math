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
import datetime
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
        raw_dataset['handwriting'].preprocessing(preprocessing_queue)
    sys.stdout.write("\r%0.2f%% (done)   \n" % (100))
    print("")
    pickle.dump({'handwriting_datasets': raw_datasets,
                 'formula_id2latex': loaded['formula_id2latex'],
                 'preprocessing_queue': preprocessing_queue
                 },
                open(outputpath, "wb"))


def is_valid_file(parser, arg):
    arg = os.path.abspath(arg)
    if not os.path.exists(arg):
        parser.error("The file %s does not exist!" % arg)
    else:
        return arg


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
                        type=lambda x: is_valid_file(parser, x),
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
    preprocessing_queue = []
    print(model_description['preprocessing'])
    for el in model_description['preprocessing']:
        parameters = {}
        algorithms = el.keys()
        for algorithm in algorithms:
            parameters = {}
            if el[algorithm] is not None:
                for param in el[algorithm]:
                    for key in param.keys():
                        print(key)
                        parameters[key] = param[key]
            algorithm = preprocessing.get_algorithm(algorithm)
            preprocessing_queue.append((algorithm, parameters))
    # Do it! Preprcess the data!
    create_preprocessed_dataset(raw_datapath, outputpath, preprocessing_queue)

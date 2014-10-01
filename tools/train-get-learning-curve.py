#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""Create a learning curve for a given model. The pfiles have to exist before
   this is started (create_pfiles_learning_curve.py).
"""

import os
import yaml
import logging
import sys
logging.basicConfig(format='%(asctime)s %(levelname)s %(message)s',
                    level=logging.DEBUG,
                    stream=sys.stdout)
# mine
import utils


def generate_training_command(model_folder):
    utils.update_if_outdated(model_folder)
    model_description_file = os.path.join(model_folder, "info.yml")
    # Read the model description file
    with open(model_description_file, 'r') as ymlfile:
        model_description = yaml.load(ymlfile)

    # Get the data paths (pfiles)
    PROJECT_ROOT = utils.get_project_root()
    data = {}
    data['training'] = os.path.join(PROJECT_ROOT,
                                    model_description["data-source"],
                                    "traindata.pfile")
    data['testing'] = os.path.join(PROJECT_ROOT,
                                   model_description["data-source"],
                                   "testdata.pfile")
    data['validating'] = os.path.join(PROJECT_ROOT,
                                      model_description["data-source"],
                                      "validdata.pfile")

    # Get latest model file
    model_src = os.path.join(model_folder, "%s-%i.json" % ("model", 0))
    model_target = os.path.join(model_folder, "target.json")

    # generate the training command
    training = model_description['training']
    training = training.replace("{{testing}}", data['testing'])
    training = training.replace("{{training}}", data['training'])
    training = training.replace("{{validation}}", data['validating'])
    training = training.replace("{{src_model}}", model_src)
    training = training.replace("{{target_model}}", model_target)
    training = training.replace("{{nntoolkit}}", utils.get_nntoolkit())
    return training


def train_model(model_folder, model_description, data):
    os.chdir(model_folder)
    training = generate_training_command(model_folder)
    if training is None:
        return -1
    os.chdir(model_folder)
    steps = 5
    for i in range(1, 50, steps):
        # Adjustmenst for learning curve
        folder = "%i-recording" % i
        if not os.path.exists(folder):
            os.makedirs(folder)
            newcommand = training.replace("traindata.pfile",
                                          "traindata-%i-examples.pfile" % i)
            newcommand = newcommand.replace("testresult_%e.txt",
                                            "%s/testresult_%%e.txt" % folder)
            newcommand = newcommand.replace("target.json",
                                            "%s/model-1.json" % folder)
            logging.info(newcommand)
            os.system(newcommand)


def main(model_folder):
    model_description_file = os.path.join(model_folder, "info.yml")

    # Read the model description file
    with open(model_description_file, 'r') as ymlfile:
        model_description = yaml.load(ymlfile)

    # Analyze model
    logging.info(model_description['model'])
    data = {}
    data['training'] = os.path.join(model_folder, "traindata.pfile")
    data['testing'] = os.path.join(model_folder, "testdata.pfile")
    data['validating'] = os.path.join(model_folder, "validdata.pfile")
    train_model(model_folder, model_description, data)

if __name__ == "__main__":
    PROJECT_ROOT = utils.get_project_root()

    # Get latest model description file
    models_folder = os.path.join(PROJECT_ROOT, "archive/models")
    latest_model = utils.get_latest_folder(models_folder)

    # Get command line arguments
    from argparse import ArgumentParser, ArgumentDefaultsHelpFormatter
    parser = ArgumentParser(description=__doc__,
                            formatter_class=ArgumentDefaultsHelpFormatter)
    parser.add_argument("-m", "--model",
                        dest="model",
                        help="where is the model folder (with a info.yml)?",
                        metavar="FOLDER",
                        type=lambda x: utils.is_valid_folder(parser, x),
                        default=latest_model)
    args = parser.parse_args()
    main(args.model)

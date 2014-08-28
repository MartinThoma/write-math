#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""Create and train a given model."""

import os
import yaml
import logging
import sys
logging.basicConfig(format='%(asctime)s %(levelname)s %(message)s',
                    level=logging.DEBUG,
                    stream=sys.stdout)
# mine
import utils


def train_model(model_folder, model_description, data):
    os.chdir(model_folder)
    basename = "model"
    training = model_description['training']
    latest_model = utils.get_latest_working_model(model_folder)

    if latest_model == "":
        logging.error("There is no model with basename '%s'.", basename)
        sys.exit(1)
    else:
        logging.info("Model '%s' found.", latest_model)
        i = int(latest_model.split("-")[-1].split(".")[0])
        model_src = os.path.join(model_folder, "%s-%i.json" % (basename, i))
        model_target = os.path.join(model_folder,
                                    "%s-%i.json" % (basename, i+1))

    # train the model
    training = training.replace("{{testing}}", data['testing'])
    training = training.replace("{{training}}", data['training'])
    training = training.replace("{{validation}}", data['validating'])
    training = training.replace("{{src_model}}", model_src)
    training = training.replace("{{target_model}}", model_target)
    logging.info(training)
    os.system(training)


def main(model_folder):
    model_description_file = os.path.join(model_folder, "model.yml")

    # Read the model description file
    with open(model_description_file, 'r') as ymlfile:
        model_description = yaml.load(ymlfile)

    # Analyze model
    logging.info(model_description['model'])
    modelfile = utils.get_latest_in_folder(model_folder, ".json")
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
                        help="where is the model folder (with a model.yml)?",
                        metavar="FOLDER",
                        type=lambda x: utils.is_valid_folder(parser, x),
                        default=latest_model)
    args = parser.parse_args()
    main(args.model)

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
import natsort
# mine
import utils


def create_model(model_folder, basename, model_type, topology, training,
                 data):
    models = filter(lambda n: n.endswith(".json"), os.listdir(model_folder))
    models = filter(lambda n: n.startswith(basename), models)
    models = natsort.natsorted(models, reverse=True)
    if len(models) == 0:
        logging.info("No base model. Create it...")
        model_src = os.path.join(model_folder, "%s-0.json" % basename)
        command = "nntoolkit make %s %s > %s" % (model_type,
                                                 topology,
                                                 model_src)
        model_target = os.path.join(model_folder, "%s-1.json" % basename)
        logging.info(command)
        os.system(command)
    else:
        latest_model = models[0]
        i = int(latest_model.split("-")[-1])
        model_src = os.path.json(model_folder, "%s-%i.json" % (basename, i))
        model_target = os.path.json(model_folder,
                                    "%s-%i.json" % (basename, i+1))

    # train the model
    training = training.replace("{{training}}", data['training'])
    training = training.replace("{{validation}}", data['validating'])
    training = training.replace("{{src_model}}", model_src)
    training = training.replace("{{target_model}}", model_target)
    logging.info(training)
    os.system(training)

if __name__ == "__main__":
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
    # Analyze model
    print(model_description['model'])
    modelfile = os.path.join(PROJECT_ROOT,
                             model_description['model']['folder'])
    create_model(modelfile,
                 model_description['model']['basename'],
                 model_description['model']['type'],
                 model_description['model']['topology'],
                 model_description['training'],
                 model_description['data'])

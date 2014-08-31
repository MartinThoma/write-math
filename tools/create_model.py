#!/usr/bin/env python

import os
import yaml
import natsort
import logging
import sys
logging.basicConfig(format='%(asctime)s %(levelname)s %(message)s',
                    level=logging.DEBUG,
                    stream=sys.stdout)
# mine
import utils


def create_model(model_folder, model_type, topology, override):
    latest_model = utils.get_latest_in_folder(model_folder, ".json")
    if (latest_model == "") or override:
        logging.info("Create a base model...")
        model_src = os.path.join(model_folder, "model-0.json")
        command = "nntoolkit make %s %s > %s" % (model_type,
                                                 topology,
                                                 model_src)
        logging.info(command)
        os.system(command)
    else:
        logging.info("Model file already existed.")


def main(model_folder, override=False):
    model_description_file = os.path.join(model_folder, "info.yml")
    # Read the model description file
    with open(model_description_file, 'r') as ymlfile:
        model_description = yaml.load(ymlfile)
    # Analyze model
    logging.info(model_description['model'])
    create_model(model_folder,
                 model_description['model']['type'],
                 model_description['model']['topology'],
                 override)
    utils.create_run_logfile(model_folder)


if __name__ == "__main__":
    PROJECT_ROOT = utils.get_project_root()

    # Get latest model folder
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
    parser.add_argument("-o", "--override",
                        action="store_true", dest="override",
                        default=False,
                        help=("should the model be overridden "
                              "if it already exists?"))
    args = parser.parse_args()
    main(args.model, args.override)

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


def create_model(model_folder, basename, model_type, topology, override):
    models = filter(lambda n: n.endswith(".json"), os.listdir(model_folder))
    models = filter(lambda n: n.startswith(basename), models)
    models = natsort.natsorted(models, reverse=True)
    if (len(models) == 0) or override:
        logging.info("No base model. Create it...")
        model_src = os.path.join(model_folder, "%s-0.json" % basename)
        command = "nntoolkit make %s %s > %s" % (model_type,
                                                 topology,
                                                 model_src)
        logging.info(command)
        os.system(command)


def main(model_description_file, override):
    PROJECT_ROOT = utils.get_project_root()
    # Read the model description file
    with open(model_description_file, 'r') as ymlfile:
        model_description = yaml.load(ymlfile)
    # Analyze model
    print(model_description['model'])
    modelfile = os.path.join(PROJECT_ROOT,
                             model_description['model']['folder'])
    create_model(modelfile,
                 model_description['model']['basename'],
                 model_description['model']['type'],
                 model_description['model']['topology'],
                 override)


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
    parser.add_argument("-o", "--override",
                        action="store_true", dest="override",
                        default=False,
                        help=("should the model be overridden "
                              "if it already exists?"))
    args = parser.parse_args()
    main(args.model_description_file, args.override)

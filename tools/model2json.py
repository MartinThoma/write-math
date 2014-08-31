#!/usr/bin/env python

"""Convert a model.json file with numpy arrays to a normal json file."""

import logging
import sys
import os
logging.basicConfig(format='%(asctime)s %(levelname)s %(message)s',
                    level=logging.DEBUG,
                    stream=sys.stdout)
import simplejson as json
from StringIO import StringIO
import numpy
from base64 import b64decode
# mine
import utils


def main(model_folder, model_target="modelparams.json"):
    os.chdir(model_folder)

    # Get model as string
    model_file = utils.get_latest_working_model(model_folder)
    with open(model_file) as f:
        content = f.read()
    parsed_model = json.loads(content)

    # Build model representation by layers
    layers = []

    for i, layer in enumerate(parsed_model["layers"]):
        logging.info("## Layer %i" % i)
        logging.info("Props: %s" % str(layer['_props']))
        if '_mtype' in layer:
            logging.info("mtype: %s" % str(layer['_mtype']))
        else:
            logging.info(layer.keys())
        logging.info("param keys: %s" % str(layer['params'].keys()))
        key = '__numpy.cndarray__'
        W = numpy.load(StringIO(b64decode(layer["params"]["W"][key]))).tolist()
        b = numpy.load(StringIO(b64decode(layer["params"]["b"][key]))).tolist()
        layers.append({'W': W, 'b': b})

    with open(model_target, "w") as f:
        f.write(json.dumps(layers))

if __name__ == "__main__":
    PROJECT_ROOT = utils.get_project_root()

    # Get latest model folder
    models_folder = os.path.join(PROJECT_ROOT, "archive/models")
    latest_model = utils.get_latest_folder(models_folder)

    from argparse import ArgumentParser, ArgumentDefaultsHelpFormatter
    parser = ArgumentParser(description=__doc__,
                            formatter_class=ArgumentDefaultsHelpFormatter)
    parser.add_argument("-m", "--model",
                        dest="model",
                        help="where is the model folder (with the info.yml)?",
                        metavar="FILE",
                        type=lambda x: utils.is_valid_folder(parser, x),
                        default=latest_model)
    parser.add_argument("-t", "--target",
                        dest="target",
                        help="what name should the new parameter file have?",
                        metavar="FILE",
                        default="modelparams.json")
    args = parser.parse_args()
    main(args.model, args.target)

#!/usr/bin/env python

import os
import yaml
import natsort
import logging
import sys
logging.basicConfig(format='%(asctime)s %(levelname)s %(message)s',
                    level=logging.DEBUG,
                    stream=sys.stdout)
import subprocess
import time
import re
# mine
import utils


def test_model(model_folder, basename, test_file):
    model_src = utils.get_latest_model(model_folder, basename)
    if model_src is None:
        logging.error("No model with basename '%s' found in '%s'.",
                      basename,
                      model_folder)
    else:
        PROJECT_ROOT = utils.get_project_root()
        time_prefix = time.strftime("%Y-%m-%d-%H-%M")
        logging.info("Evaluate '%s'...", model_src)
        logfile = os.path.join(PROJECT_ROOT,
                               "archive/logs/%s-testing.log" %
                               time_prefix)
        with open(logfile, "w") as log, open(model_src, "r") as model_src_p:
            p = subprocess.Popen(['nntoolkit', 'test', '--batch-size', '1',
                                  test_file],
                                 stdin=model_src_p,
                                 stderr=log)
            ret = p.wait()
            if ret != 0:
                logging.error("nntoolkit finished with ret code %s", str(ret))
                sys.exit()

        # Get the error
        with open(logfile) as f:
            log_content = f.read()
        pattern = re.compile("errors = (\d\.\d+)")
        error = float(pattern.findall(log_content)[-1])
        return error


def main(model_description_file, run_native=False):
    PROJECT_ROOT = utils.get_project_root()
    # Read the model description file
    with open(model_description_file, 'r') as ymlfile:
        model_description = yaml.load(ymlfile)
    model_folder = os.path.join(PROJECT_ROOT,
                                model_description['model']['folder'])
    test_data_path = os.path.join(PROJECT_ROOT,
                                  model_description['data']['testing'])
    error = test_model(model_folder,
                       model_description['model']['basename'],
                       test_data_path)
    if run_native:
        logging.info("Error: %0.4f", error)
    return error


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
    main(args.model_description_file, run_native=True)

#!/usr/bin/env python

import os
import logging
import sys
logging.basicConfig(format='%(asctime)s %(levelname)s %(message)s',
                    level=logging.DEBUG,
                    stream=sys.stdout)
import yaml
#mine
import utils
import refresh_model


def choose_dataset(model_folder):
    # Get the currently used raw dataset
    model_description_file = os.path.join(model_folder, "model.yml")
    # Read the model description file
    with open(model_description_file, 'r') as ymlfile:
        md = yaml.load(ymlfile)

    # Get the preprocessing information
    PROJECT_ROOT = utils.get_project_root()
    preprocessed = os.path.join(PROJECT_ROOT, md['preprocessed'],
                                "info.yml")

    # Read the preprocessing info file
    with open(preprocessed, 'r') as ymlfile:
        pd = yaml.load(ymlfile)
    currently = pd['data-source']

    # Get all other datasets
    folder = os.path.join(utils.get_project_root(), "archive/raw-datasets")
    files = [os.path.join(folder, name) for name in os.listdir(folder)
             if name.endswith(".pickle")]
    default = -1
    for i, filename in enumerate(files):
        if os.path.basename(currently) == os.path.basename(filename):
            default = i
        if i != default:
            print("[%i]\t%s" % (i, os.path.basename(filename)))
        else:
            print("\033[1m[%i]\033[0m\t%s" % (i, os.path.basename(filename)))
    i = utils.input_int_default("Choose a dataset by number: ", default)
    return files[i]


def main():
    """Go through each model folder and refresh them."""
    folder = os.path.join(utils.get_project_root(), "archive/models")
    folders = [os.path.join(folder, name) for name in os.listdir(folder)
               if os.path.isdir(os.path.join(folder, name))]
    for model_folder in folders:
        logging.info("Update model '%s' ...", model_folder)
        dataset = choose_dataset(model_folder)
        refresh_model.main(model_folder, dataset)
        print("")  # Newline to show that this is done
    logging.info("done")


if __name__ == '__main__':
    main()

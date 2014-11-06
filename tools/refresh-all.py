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
    model_description_file = os.path.join(model_folder, "info.yml")
    # Read the model description file
    with open(model_description_file, 'r') as ymlfile:
        md = yaml.load(ymlfile)

    # Get the preprocessing information
    project_root = utils.get_project_root()
    preprocessed = os.path.join(project_root, md['preprocessed'],
                                "info.yml")

    # Read the preprocessing info file
    with open(preprocessed, 'r') as ymlfile:
        pd = yaml.load(ymlfile)
    currently = pd['data-source']
    return utils.choose_raw_dataset(currently)


def main():
    """Go through each model folder and refresh them."""
    folder = os.path.join(utils.get_project_root(), "models")
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

#!/usr/bin/env python

import os
import logging
import sys
logging.basicConfig(format='%(asctime)s %(levelname)s %(message)s',
                    level=logging.DEBUG,
                    stream=sys.stdout)
#mine
import train
import utils


def clean_model_folder(model_folder):
    """Remove all `DO.` files from a model folder."""
    # remove all files that begin with "DO."
    for my_file in os.listdir(model_folder):
        if my_file.startswith("DO."):
            dofile = os.path.join(model_folder, my_file)
            os.remove(dofile)


def add_do_files(model_folder):
    """Add all DO files to model folder."""

    # Get all template DO files
    template_folder = os.path.join(utils.get_project_root(),
                                   "tools/slurm-files")
    for my_file in os.listdir(template_folder):
        if my_file.startswith("DO."):
            # Get template as string
            template_file = os.path.join(template_folder, my_file)
            with open(template_file) as f:
                template = f.read()
            # Replace all template variables
            training_command = train.generate_training_command(model_folder)
            if training_command is not None:
                template = template.replace("{{ training }}", training_command)
            # Write template file to model folder
            filename = os.path.join(model_folder, my_file)
            with open(filename, "w") as f:
                f.write(template)


def main():
    """Go through each model folder and update them."""
    folder = os.path.join(utils.get_project_root(), "archive/models")
    folders = [os.path.join(folder, name) for name in os.listdir(folder)
               if os.path.isdir(os.path.join(folder, name))]
    for model_folder in folders:
        logging.info("Update folder '%s' ...", model_folder)
        clean_model_folder(model_folder)
        add_do_files(model_folder)
    logging.info("done")


if __name__ == '__main__':
    main()

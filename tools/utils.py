#!/usr/bin/env python

import os
import yaml
import natsort


def get_project_root():
    """Get the project root folder as a string."""
    home = os.path.expanduser("~")
    rcfile = os.path.join(home, ".writemathrc")
    with open(rcfile, 'r') as ymlfile:
        cfg = yaml.load(ymlfile)
    return cfg['root']


def get_latest_in_folder(folder, ending="", default=""):
    latest = ""
    for my_file in natsort.natsorted(os.listdir(folder), reverse=True):
        if my_file.endswith(ending):
            latest = os.path.join(folder, my_file)
    return latest


def get_database_config_file():
    PROJECT_ROOT = get_project_root()
    return os.path.join(PROJECT_ROOT, "tools/db.config.yml")


def get_database_configuration():
    with open(get_database_config_file(), 'r') as ymlfile:
        cfg = yaml.load(ymlfile)
    return cfg

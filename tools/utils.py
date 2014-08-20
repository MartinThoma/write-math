#!/usr/bin/env python

"""Utility functions that can be used in multiple scripts."""

import sys
import os
import yaml
import natsort
import time
import datetime


def print_status(total, current, start_time=None):
    """Show how much work was done / how much work is remaining"""
    percentage_done = float(current)/total
    sys.stdout.write("\r%0.2f%% " % (percentage_done*100))
    if start_time is not None:
        current_running_time = time.time() - start_time
        remaining_seconds = current_running_time / percentage_done
        tmp = datetime.timedelta(seconds=remaining_seconds)
        sys.stdout.write("(%s remaining)   " % str(tmp))
    sys.stdout.flush()


def is_valid_file(parser, arg):
    """Check if arg is a valid file that already exists on the file system."""
    arg = os.path.abspath(arg)
    if not os.path.exists(arg):
        parser.error("The file %s does not exist!" % arg)
    else:
        return arg


def get_project_configuration():
    """Get project configuration as dictionary."""
    home = os.path.expanduser("~")
    rcfile = os.path.join(home, ".writemathrc")
    with open(rcfile, 'r') as ymlfile:
        cfg = yaml.load(ymlfile)
    return cfg


def get_project_root():
    """Get the project root folder as a string."""
    cfg = get_project_configuration()
    return cfg['root']


def get_latest_in_folder(folder, ending="", default=""):
    """Get the file that comes last with natural sorting in folder and has
       file ending 'ending'.
    """
    latest = default
    for my_file in natsort.natsorted(os.listdir(folder), reverse=True):
        if my_file.endswith(ending):
            latest = os.path.join(folder, my_file)
    return latest


def get_database_config_file():
    """Get the absolute path to the database configuration file."""
    return os.path.join(get_project_root(), "tools/db.config.yml")


def get_database_configuration():
    """Get database configuration as dictionary."""
    with open(get_database_config_file(), 'r') as ymlfile:
        cfg = yaml.load(ymlfile)
    return cfg


def sizeof_fmt(num):
    """Takes the a filesize in bytes and returns a nicely formatted string. """
    for x in ['bytes', 'KB', 'MB', 'GB', 'TB']:
        if num < 1024.0:
            return "%3.1f %s" % (num, x)
        num /= 1024.0

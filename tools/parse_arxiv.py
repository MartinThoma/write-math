#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""Go through arXiv data.

You can download arXiv data by s3cmd:

1. pip install s3cmd
2. s3cmd --configure
3. s3cmd get --recursive --skip-existing s3://arxiv/src/ --requester-pays
"""

import os
from os import listdir
from os.path import isfile, join
import tarfile
import logging
import sys

from find_mathmode import get_math_mode

logging.basicConfig(format='%(asctime)s %(levelname)s %(message)s',
                    level=logging.DEBUG,
                    stream=sys.stdout)


def main(directory):
    onlyfiles = [f for f in listdir(directory) if isfile(join(directory, f))]
    tarfiles = sorted([os.path.join(directory, f)
                       for f in onlyfiles if f.endswith('.tar')])
    for tar_filename in tarfiles:
        files_by_project = get_data(directory, tar_filename)
        for project in files_by_project:
            for filename in project:
                if filename.endswith('.eps') or filename.endswith('.sty'):
                    continue
                elif not filename.endswith('.tex'):
                    logging.info("Found %s. Skip.", filename)
                    continue
                mathmode_contents = get_math_mode(filename)
                print(mathmode_contents)
            sys.exit()


def get_data(directory, tar_filename):
    """
    Extract data and return filenames, grouped by paper.

    Parameters
    ----------
    directory : string
        The path to a directory which contains .gz files of the arXiv.

    Returns
    -------
    list of lists
        Each sublist belongs to a publication and contains paths to files.
    """
    extracted_by_project = []

    working_directory = os.path.join(directory, '.cache')
    if not os.path.exists(working_directory):
        os.makedirs(working_directory)
    logging.info(tar_filename)

    # Extract all .gz files in .tar file
    extracted = []
    with tarfile.open(tar_filename) as tar:
        extracted = tar.getnames()
        tar.extractall(path=working_directory)
    extracted = [os.path.join(working_directory, f)
                 for f in extracted if f.endswith('.gz')]

    # Extract all files within .gz files
    for gz_file in extracted:
        try:
            extracted_by_project.append([])
            with tarfile.open(gz_file, 'r:gz') as tar:
                sub_workdir = gz_file[:-3]
                if not os.path.exists(sub_workdir):
                    os.makedirs(sub_workdir)
                ext = tar.getnames()
                tar.extractall(path=sub_workdir)
            for filename in ext:
                full_path_filename = os.path.join(sub_workdir, filename)
                extracted_by_project[-1].append(full_path_filename)
            logging.warning("%s done.", gz_file)
        except:
            logging.warning("Didn't work for %s", gz_file)
    return extracted_by_project


def get_parser():
    from argparse import ArgumentParser, ArgumentDefaultsHelpFormatter
    parser = ArgumentParser(description=__doc__,
                            formatter_class=ArgumentDefaultsHelpFormatter)
    parser.add_argument("-d", "--directory",
                        dest="directory",
                        help="look in this DIR for arXiv .tar files",
                        metavar="DIR",
                        required=True)
    return parser


if __name__ == "__main__":
    args = get_parser().parse_args()
    main(args.directory)

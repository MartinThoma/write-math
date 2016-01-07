#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
Check single symbol recordings for multiple symbols.

This tool tries to find recordings which have a segmentation online which
says the most likely hypothesis is only one symbol, but actually - with the
current model - the most likely hypothesis has multiple symbols.
"""

from hwrt import segmentation as se
from hwrt import utils

# import json
import pickle
import natsort

import logging
import sys
import os

logging.basicConfig(format='%(asctime)s %(levelname)s %(message)s',
                    level=logging.DEBUG,
                    stream=sys.stdout)


def main(raw_pickle):
    """
    Parameters
    ----------
    raw_pickle : str
        Path to a pickle file
    """
    logging.info('Start loading raw datasets...')
    raw_datasets = load_raw(raw_pickle)
    logging.info('Start analyzing...')
    wrongs = []
    for i, raw_dataset in enumerate(raw_datasets):
        if i % 100 == 0:
            print(i)
        ret = check_single(raw_dataset)
        if ret != -1:
            wrongs.append(ret)
    logging.info("Wrongs: %i", len(wrongs))


def check_single(raw_dataset):
    """
    Parameters
    ----------
    raw_dataset : dict
        with key 'handwriting'

    Returns
    -------
    tuple or int
        (raw_dataset, seg_predict) or -1 to be exact (TODO)
    """
    strokelist = raw_dataset['handwriting'].get_sorted_pointlist()
    if len(strokelist) > 8:
        logging.warning('%i strokes in %s',
                        len(strokelist),
                        raw_dataset['handwriting'])
    beam = se.Beam()
    for stroke in strokelist:
        beam.add_stroke({'data': [stroke], 'id': 42})  # TODO
    seg_predict = beam.get_results()
    if seg_predict[0]['symbol count'] != 1:
        logging.info(('http://write-math.com/view/?raw_data_id=%i : '
                      '%s symbols (%s)'),
                     raw_dataset['handwriting'].raw_data_id,
                     seg_predict[0]['symbol count'],
                     seg_predict[0]['semantics'].split(';')[1])
        return (raw_dataset, seg_predict)
    return -1


def load_raw(path_to_data):
    """
    Parameters
    ----------
    path_to_data : str

    Returns
    -------
    list
        HandwrittenData objects
    """
    with open(path_to_data, "rb") as f:
        loaded = pickle.load(f)
    raw_datasets = loaded['handwriting_datasets']
    return raw_datasets


def is_valid_file(parser, arg):
    """
    Check if arg is a valid file that already exists on the file system.

    Parameters
    ----------
    parser : argparse object
    arg : str

    Returns
    -------
    arg
    """
    arg = os.path.abspath(arg)
    if not os.path.exists(arg):
        parser.error("The file %s does not exist!" % arg)
    else:
        return arg


def _get_default_pickle():
    """
    Get a raw dataset.

    Returns
    -------
    None or str
        Path to a model.pickle file.
    """
    project_root = utils.get_project_root()
    raw_dir = os.path.join(project_root, "raw-datasets")
    models = filter(lambda n: n.endswith(".pickle"), os.listdir(raw_dir))
    models = natsort.natsorted(models, reverse=True)
    if len(models) == 0:
        return None
    else:
        return os.path.join(raw_dir, models[0])


def get_parser():
    """Get parser object for find_wrong_segmentation.py."""
    from argparse import ArgumentParser, ArgumentDefaultsHelpFormatter
    parser = ArgumentParser(description=__doc__,
                            formatter_class=ArgumentDefaultsHelpFormatter)
    parser.add_argument("-r", "--raw",
                        dest="raw_pickle",
                        default=_get_default_pickle(),
                        type=lambda x: is_valid_file(parser, x),
                        help="load data from RAW_PICKLE_FILE",
                        metavar="RAW_PICKLE_FILE")
    return parser


if __name__ == '__main__':
    args = get_parser().parse_args()
    main(args.raw_pickle)

#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""Check single symbol recordings for multiple symbols."""

from hwrt import segmentation
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

nn = segmentation.get_nn_classifier(None, None)
stroke_segmented_classifier = lambda X: nn(X)[0][1]
single_stroke_clf = None  # single_symbol_stroke_classifier()
single_clf = segmentation.single_classifier()


def main(raw_pickle):
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
    pointlist = raw_dataset['handwriting'].get_pointlist()
    if len(pointlist) > 8:
        logging.warning('%i strokes in %s',
                        len(pointlist),
                        raw_dataset['handwriting'])
    seg_predict = segmentation.get_segmentation(pointlist,
                                                single_clf,
                                                single_stroke_clf,
                                                stroke_segmented_classifier)
    if len(seg_predict[0][0]) != 1:
        logging.info('http://write-math.com/view/?raw_data_id=%i : %s',
                     raw_dataset['handwriting'].raw_data_id,
                     seg_predict[0][0])
        return (raw_dataset, seg_predict)
    return -1


def load_raw(path_to_data):
    loaded = pickle.load(open(path_to_data, "rb"))
    raw_datasets = loaded['handwriting_datasets']
    return raw_datasets


def is_valid_file(parser, arg):
    """Check if arg is a valid file that already exists on the file
       system.
    """
    arg = os.path.abspath(arg)
    if not os.path.exists(arg):
        parser.error("The file %s does not exist!" % arg)
    else:
        return arg


def _get_default_pickle():
    project_root = utils.get_project_root()
    raw_dir = os.path.join(project_root, "raw-datasets")
    models = filter(lambda n: n.endswith(".pickle"), os.listdir(raw_dir))
    models = natsort.natsorted(models, reverse=True)
    if len(models) == 0:
        return None
    else:
        return os.path.join(raw_dir, models[0])


def get_parser():
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

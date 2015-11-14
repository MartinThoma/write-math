#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
Given a symbol s, what is the probability P(n|s) of a stroke count of n?

Download data for each symbol.
"""

import logging
import sys
logging.basicConfig(format='%(asctime)s %(levelname)s %(message)s',
                    level=logging.INFO,
                    stream=sys.stdout)
import pymysql.cursors
import numpy
from collections import Counter
import yaml

# My packages
from hwrt.handwritten_data import HandwrittenData
from hwrt import utils

from write_math_utils import get_formulas


def main(dataset='all'):
    """
    Parameters
    ----------
    dataset : string
        Either 'all' or a path to a yaml symbol file.
    """
    cfg = utils.get_database_configuration()
    mysql = cfg['mysql_online']
    connection = pymysql.connect(host=mysql['host'],
                                 user=mysql['user'],
                                 passwd=mysql['passwd'],
                                 db=mysql['db'],
                                 cursorclass=pymysql.cursors.DictCursor)
    cursor = connection.cursor()

    # TODO: no formulas, only single-symbol ones.
    formulas = get_formulas(cursor, dataset)
    prob = {}

    # Go through each formula and download every raw_data instance
    for formula in formulas:
        stroke_counts = []
        recordings = []
        sql = (("SELECT `wm_raw_draw_data`.`id`, `data`, `is_in_testset`, "
                "`wild_point_count`, `missing_line`, `user_id`, "
                "`display_name` "
                "FROM `wm_raw_draw_data` "
                "JOIN `wm_users` ON "
                "(`wm_users`.`id` = `wm_raw_draw_data`.`user_id`) "
                "WHERE `accepted_formula_id` = %s "
                "AND wild_point_count=0 "
                "AND has_correction=0 "
                # "AND `display_name` LIKE 'MfrDB::%%'"
                ) %
               str(formula['id']))
        cursor.execute(sql)
        raw_datasets = cursor.fetchall()
        logging.info("%s (%i)", formula['formula_in_latex'], len(raw_datasets))
        for raw_data in raw_datasets:
            try:
                handwriting = HandwrittenData(raw_data['data'],
                                              formula['id'],
                                              raw_data['id'],
                                              formula['formula_in_latex'],
                                              raw_data['wild_point_count'],
                                              raw_data['missing_line'],
                                              raw_data['user_id'])
                stroke_counts.append(len(handwriting.get_pointlist()))
                recordings.append(handwriting)
            except Exception as e:
                logging.info("Raw data id: %s", raw_data['id'])
                logging.info(e)
        if len(stroke_counts) > 0:
            logging.info("\t[%i - %i]", min(stroke_counts), max(stroke_counts))
            median = numpy.median(stroke_counts)
            logging.info("\tMedian: %0.2f\tMean: %0.2f\tstd: %0.2f",
                         median,
                         numpy.mean(stroke_counts),
                         numpy.std(stroke_counts))

            # Make prob
            s = sorted(Counter(stroke_counts).items(),
                       key=lambda n: n[1],
                       reverse=True)
            key = formula['formula_in_latex']
            prob[key] = {}
            for stroke_nr, count in s:
                prob[key][stroke_nr] = count

            # Outliers
            modes = get_modes(stroke_counts)
            logging.info("\tModes: %s", modes)
            exceptions = []
            for rec in recordings:
                if len(rec.get_pointlist()) not in modes:
                    url = (("http://www.martin-thoma.de/"
                            "write-math/view/?raw_data_id=%i - "
                            "%i strokes") % (rec.raw_data_id,
                                             len(rec.get_pointlist())))
                    dist = get_dist(len(rec.get_pointlist()), modes)
                    exceptions.append((url, len(rec.get_pointlist()), dist))
            print_exceptions(exceptions, max_print=10)
        else:
            logging.debug("No recordings for symbol "
                          "'http://www.martin-thoma.de/"
                          "write-math/symbol/?id=%s'.",
                          formula['id'])
    write_prob(prob, "prob_stroke_count_by_symbol.yml")


def print_exceptions(exceptions, max_print=10):
    """
    Print the exceptions, but not too many.

    Parameters
    ----------
    exceptions : list
        Triplets (url, stroke_count, dist to closest mode)
    max_print : int
        Print not more then max_print lines
    """
    exceptions = sorted(exceptions,
                        key=lambda n: (n[2], n[1]),
                        reverse=True)[:max_print]
    for url, stroke_count, _ in exceptions:
        logging.info("\t%s - %i strokes", url, stroke_count)


def get_dist(stroke_count, modes):
    """
    Get the distance to the closest mode.

    Parameters
    ----------
    stroke_count : int
    modes : list of int
    """
    dist = float('inf')
    for mode in modes:
        dist = min(dist, abs(mode - stroke_count))
    return dist


def get_modes(empiric_distribution, at_least_total=10, at_least_rel=0.1):
    """
    Get all values which make at least a relative number of at_least_rel of
    the data given in empiric_distribution, but also at least at_least_total
    times in the data.

    The most common value does not have to have at_least_total apearences in
    the data.

    Parameters
    ----------
    empiric_distribution : list
        List of integers
    at_least_total : int
    at_least_rel : float
        Value in (0.0, 1.0)
    """
    modes = []
    s = sorted(Counter(empiric_distribution).items(),
               key=lambda n: n[1],
               reverse=True)
    total = float(len(s))
    for stroke_count, appearences in s:
        constrain1 = (stroke_count >= at_least_total and
                      appearences/total >= at_least_total)
        if constrain1 or len(modes) == 0:
            modes.append(stroke_count)
    return modes


def write_prob(counts, filename):
    """
    Parameters
    ----------
    prob : dict
        Mapping symbols to dicts of stroke counts with total count
    filename : str
    """

    probs = {}

    # Get probabilities with smoothing
    for symbol_id, value in counts.items():
        probs[symbol_id] = {}
        total_count = 0
        for i in range(1, 10):
            probs[symbol_id][i] = 1
            if i in value:
                probs[symbol_id][i] += value[i]
            total_count += probs[symbol_id][i]
        for i in range(1, 10):
            probs[symbol_id][i] = probs[symbol_id][i] / float(total_count)

    # Write it
    with open(filename, 'w') as outfile:
        outfile.write(yaml.dump(probs, default_flow_style=False))


def get_parser():
    from argparse import ArgumentParser, ArgumentDefaultsHelpFormatter
    parser = ArgumentParser(description=__doc__,
                            formatter_class=ArgumentDefaultsHelpFormatter)
    parser.add_argument("-f", "--file",
                        dest="filename",
                        default='all',
                        help="Get symbols from this file.",
                        metavar="FILE")
    return parser


if __name__ == "__main__":
    args = get_parser().parse_args()
    main(args.filename)

#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
Find outliers in the data of a given class.

This script was written to detect misclassified recordings.
"""

import logging
import sys
import pymysql
import pkg_resources
import os
import numpy
from distance_metric import handwritten_data_greedy_matching_distance as dtw

import hwrt.utils
from hwrt.handwritten_data import HandwrittenData

logging.basicConfig(format='%(asctime)s %(levelname)s %(message)s',
                    level=logging.DEBUG,
                    stream=sys.stdout)


def main(symbol_id=None):
    """
    Parameters
    ----------
    symbol_id : int, optional
        If this is set, all recordings of this single symbol will be checked
        for outliers. Otherwise, all symbols will be checked.
    """
    cfg = hwrt.utils.get_database_configuration()
    mysql = cfg['mysql_online']

    model_path = pkg_resources.resource_filename('hwrt', 'misc/')
    model_file = os.path.join(model_path, "model.tar")
    logging.info("Model: %s", model_file)
    (preprocessing_queue, feature_list, model,
     output_semantics) = hwrt.utils.load_model(model_file)

    if symbol_id is None:
        symbols = get_symbols(mysql)
    else:
        symbols = [(symbol_id, 'WHATEVER')]

    for symbol_id, formula_name in symbols:
        logging.info("Start fetching recordings for symbol ID %i (%s)...",
                     symbol_id,
                     formula_name)
        recordings = get_recordings(mysql, symbol_id)
        logging.info("Got %i recordings.", len(recordings))
        # logging.info("Start calculating features...")
        recordings = get_features(recordings, preprocessing_queue)
        recordings = append_dtw(recordings)
        # logging.info("Start finding outliers...")
        outliers = get_outliers(recordings)
        min_dtw = numpy.percentile([el['score'] for el in outliers], 90)
        if numpy.percentile([el['score'] for el in outliers], 70)*2 < min_dtw:
            for i, outlier in enumerate(outliers, start=1):
                if i > 20:
                    break
                if outlier['score'] > min_dtw:
                    print(("%i: %0.4f:\thttp://write-math.com/view/"
                           "?raw_data_id=%s") %
                          (i,
                           outlier['score'],
                           outlier['HandwrittenData'].raw_data_id))
                    if i % 5 == 0:
                        print("")
                else:
                    break


def get_symbols(mysql):
    """
    Parameters
    ----------
    mysql : dict
        Connection information

    Returns
    -------
    list :
        A list of (symbol ids, formula name)
    """
    connection = pymysql.connect(host=mysql['host'],
                                 user=mysql['user'],
                                 passwd=mysql['passwd'],
                                 db=mysql['db'],
                                 cursorclass=pymysql.cursors.DictCursor)
    cursor = connection.cursor()
    sql = ("SELECT `wm_formula`.`id`, `formula_in_latex`, "
           "COUNT(`wm_formula`.`id`) AS `counter` "
           "FROM `wm_raw_draw_data` "
           "JOIN `wm_formula` ON `wm_formula`.`id` = `accepted_formula_id` "
           "WHERE (`formula_type` = 'single symbol' OR "
           "`formula_type` = 'drawing' OR "
           "`formula_type` = 'nesting symbol') AND "
           "GROUP BY  `accepted_formula_id` "
           "ORDER BY counter DESC")
    cursor.execute(sql)
    symbols = cursor.fetchall()
    symbol_ids = []
    for symbol in symbols:
        if 10 <= symbol['counter'] <= 100:
            symbol_ids.append((symbol['id'], symbol['formula_in_latex']))
    return symbol_ids


def get_recordings(mysql, symbol_id):
    """
    Parameters
    ----------
    mysql : dict
        Connection information
    symbol_id : int
        ID of a symbol on write-math.com

    Returns
    -------
    list :
        A list of HandwrittenData objects
    """
    connection = pymysql.connect(host=mysql['host'],
                                 user=mysql['user'],
                                 passwd=mysql['passwd'],
                                 db=mysql['db'],
                                 cursorclass=pymysql.cursors.DictCursor)
    cursor = connection.cursor()

    # Get the data
    recordings = []
    sql = ("SELECT `id`, `data`, `is_in_testset`, `wild_point_count`, "
           "`missing_line`, `user_id` "
           "FROM `wm_raw_draw_data` "
           "WHERE `accepted_formula_id` = %s" % str(symbol_id))
    cursor.execute(sql)
    raw_datasets = cursor.fetchall()
    for raw_data in raw_datasets:
        try:
            handwriting = HandwrittenData(raw_data['data'],
                                          symbol_id,
                                          raw_data['id'],
                                          "no formula in latex",
                                          raw_data['wild_point_count'],
                                          raw_data['missing_line'],
                                          raw_data['user_id'])
            recordings.append(handwriting)
        except Exception as e:
            logging.info("Raw data id: %s", raw_data['id'])
            logging.info(e)
    return recordings


def get_features(recordings, preprocessing_queue):
    """
    Calculate features for each recording.

    Parameters
    ----------
    recordings : list
        A list of HandwrittenData objects
    preprocessing_queue : list of preprocessing algorithms


    Returns
    -------
    list of dicts :
        A list of dictionaries with the keys 'features' and 'HandwrittenData'
    """
    feature_dataset = []

    for recording in recordings:
        recording.preprocessing(preprocessing_queue)
        # import nntoolkit.evaluate
        # model_output = nntoolkit.evaluate.get_model_output(model, [features])
        # results = nntoolkit.evaluate.get_results(model_output,
        #                                          output_semantics)
        # results = sorted(results, key=lambda n: n['symbolnr'])
        # features = [el['probability'] for el in results]
        feature_dataset.append({'features': [],
                                'HandwrittenData': recording})

    return feature_dataset


def append_dtw(recordings):
    """
    Parameters
    ----------
    recordings : list
    """
    n = len(recordings)
    dtw_matrix = numpy.zeros((n, n))
    max_dist_noninf = 0
    for i, rec_a in enumerate(recordings):
        for j, rec_b in enumerate(recordings):
            dtw_matrix[i][j] = dtw(rec_a['HandwrittenData'],
                                   rec_b['HandwrittenData'])
            if dtw_matrix[i][j] < float('inf'):
                max_dist_noninf = max(max_dist_noninf, dtw_matrix[i][j])
    for i in range(n):
        for j in range(n):
            dtw_matrix[i][j] = min(dtw_matrix[i][j], 2*max_dist_noninf)
    for i in range(n):
        recordings[i]['dtw_median'] = numpy.median(sorted(dtw_matrix[i])[:10])
    return recordings


def get_outliers(recordings):
    """Find outliers, given a list of data with already calculated features.

    Parameters
    ----------
    recordings : list of dicts
        Each dict has the keys 'features' and 'HandwrittenData'

    Returns
    -------
    List of dicts :
        Each dict has the keys 'score' and 'HandwrittenData'. The higher the
        score, the more likely it is that the given symbol is an outlier.
    """

    # Idee:
    # Jedes Symbol hat max. 3 varianten (magic number)
    # 1. Definiere 3 zufällige, unterschiedliche recordings als cluster center
    # 2. Berechne den DTW-Abstand zu diesen 3 recordings von jedem recording
    #    Ordne jedes recording dem jeweils nächstem zu
    # 3. ???

    scored = []
    mean = numpy.array(recordings[0]['features'])
    for recording in recordings:
        mean += numpy.array(recording['features'])
    mean /= len(recordings)
    for recording in recordings:
        # score = sum((mean - recording['features'])**2
        scored.append({'score': recording['dtw_median'],
                       'HandwrittenData': recording['HandwrittenData']})
    scored = sorted(scored, key=lambda n: n['score'], reverse=True)

    # Normalization
    # max_score = float(max([el['score'] for el in scored]))
    # for i, _ in enumerate(scored):
    #     scored[i]['score'] = scored[i]['score'] / max_score
    return scored


def get_parser():
    """Get parser object for find_outliers.py."""
    from argparse import ArgumentParser, ArgumentDefaultsHelpFormatter
    parser = ArgumentParser(description=__doc__,
                            formatter_class=ArgumentDefaultsHelpFormatter)
    parser.add_argument("--id",
                        dest="symbol_id",
                        default=799,
                        type=int,
                        help="id of the symbol on write-math.com")
    return parser


if __name__ == "__main__":
    args = get_parser().parse_args()
    main(args.symbol_id)

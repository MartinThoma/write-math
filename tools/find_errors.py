#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
Find raw_datasets which are not accepted by the administrator and look
different than other known datasets with the same accepted_formula_id.

(So: Find outliers)
"""
import sys
import logging
logging.basicConfig(level=logging.INFO,
                    stream=sys.stdout,
                    format='%(asctime)s %(levelname)s: %(message)s')
logger = logging.getLogger(__name__)

# Database stuff
import pymysql
import pymysql.cursors
# Other
import webbrowser

# My modules
from distance_metric import handwritten_data_greedy_matching_distance as dtw
from hwrt import preprocessing
from hwrt import utils
from misc import HandwrittenDataM


def update_data(cfg, a, unaccept=False):
    """
    Parameters
    ----------
    cfg : dict
        Configuration
    a : HandwrittenData object
    unaccept : bool, optional
        Reset the accepted formula (default is False)
    """
    mysql = cfg['mysql_online']
    connection_local = pymysql.connect(host=mysql['host'],
                                       user=mysql['user'],
                                       passwd=mysql['passwd'],
                                       db=mysql['db'],
                                       cursorclass=pymysql.cursors.DictCursor)
    cursor_local = connection_local.cursor()
    if unaccept:
        sql = ("UPDATE `wm_raw_draw_data` "
               "SET  `administrator_edit` = now(), "
               "`missing_line` = %i, "
               "`has_hook` = %i, "
               "`has_too_long_line` = %i, "
               "`is_image` = %i, "
               "`other_problem` = %i, "
               "`has_interrupted_line` = %i, "
               "`accepted_formula_id` = NULL "
               "WHERE  `wm_raw_draw_data`.`id` =%i "
               "LIMIT 1;") % \
              (int(a.missing_line),
               int(a.has_hook),
               int(a.has_too_long_line),
               int(a.is_image),
               int(a.other_problem),
               int(a.has_interrupted_line),
               a.raw_data_id)
    elif a.istrash:
        sql = ("UPDATE `wm_raw_draw_data` "
               "SET  `administrator_edit` = now(), "
               "`missing_line` = %i, "
               "`has_hook` = %i, "
               "`has_too_long_line` = %i, "
               "`is_image` = %i, "
               "`other_problem` = %i, "
               "`has_interrupted_line` = %i, "
               "`accepted_formula_id` = 1 "
               "WHERE  `wm_raw_draw_data`.`id` =%i "
               "LIMIT 1;") % \
              (int(a.missing_line),
               int(a.has_hook),
               int(a.has_too_long_line),
               int(a.is_image),
               int(a.other_problem),
               int(a.has_interrupted_line),
               a.raw_data_id)
    else:
        sql = ("UPDATE `wm_raw_draw_data` "
               "SET  `administrator_edit` = now(), "
               "`missing_line` = %i, "
               "`has_hook` = %i, "
               "`has_too_long_line` = %i, "
               "`is_image` = %i, "
               "`other_problem` = %i, "
               "`has_interrupted_line` = %i "
               "WHERE  `wm_raw_draw_data`.`id` =%i "
               "LIMIT 1;") % \
              (int(a.missing_line),
               int(a.has_hook),
               int(a.has_too_long_line),
               int(a.is_image),
               int(a.other_problem),
               int(a.has_interrupted_line),
               a.raw_data_id)
    cursor_local.execute(sql)
    connection_local.commit()
    cursor_local.close()
    connection_local.close()
    connection_online = pymysql.connect(host=mysql['host'],
                                        user=mysql['user'],
                                        passwd=mysql['passwd'],
                                        db=mysql['db'],
                                        cursorclass=pymysql.cursors.DictCursor)
    cursor_online = connection_online.cursor()
    cursor_online.execute(sql)
    connection_online.commit()
    cursor_online.close()
    connection_online.close()


def main(cfg, raw_data_start_id):
    """
    Parameters
    ----------
    cfg : dict
        Configuration
    raw_data_start_id : int
    """
    mysql = cfg['mysql_online']
    connection = pymysql.connect(host=mysql['host'],
                                 user=mysql['user'],
                                 passwd=mysql['passwd'],
                                 db=mysql['db'],
                                 cursorclass=pymysql.cursors.DictCursor)
    cursor = connection.cursor()

    # Get formulas
    logger.info("Get formulas")
    print("get formulas")
    sql = ("SELECT `id`, `formula_in_latex` FROM `wm_formula` "
           "WHERE `id` > %s ORDER BY `id`")
    cursor.execute(sql, (raw_data_start_id, ))
    formulas = cursor.fetchall()
    formulaid2latex = {}
    for el in formulas:
        formulaid2latex[el['id']] = el['formula_in_latex']

    preprocessing_queue = [preprocessing.ScaleAndShift(),
                           # preprocessing.Douglas_peucker(EPSILON=0.2),
                           # preprocessing.Space_evenly(number=100,
                           #                            kind='cubic')
                           ]

    checked_formulas = 0
    checked_raw_data_instances = 0

    for formula_id in formulaid2latex.keys():
        alread_shown_in_browser = False
        if formula_id == 1:
            # This formula id is for trash. No need to look at it.
            continue
        # Get data
        logger.info("Get data for formula_id %i (%s)" %
                    (formula_id, formulaid2latex[formula_id]))
        sql = ("SELECT `id`, `data`, `accepted_formula_id`, "
               "`wild_point_count`, `missing_line`, `has_hook`, "
               "`has_too_long_line`, `is_image`, `administrator_edit`, "
               "`other_problem`, `has_interrupted_line` "
               "FROM  `wm_raw_draw_data` "
               "WHERE `accepted_formula_id` = %i "
               "ORDER BY `administrator_edit` DESC, "
               "`creation_date` ASC;") % formula_id
        cursor.execute(sql)
        raw_datasets = cursor.fetchall()
        logger.info("Raw datasets: %i" % len(raw_datasets))
        checked_raw_data_instances += len(raw_datasets)
        checked_formulas += 1
        if len(raw_datasets) < 100:
            continue
        as_ = []
        for i, data in enumerate(raw_datasets):
            if data['data'] == "[]":
                continue
            b = HandwrittenDataM(data['data'],
                                 data['accepted_formula_id'],
                                 data['wild_point_count'],
                                 data['missing_line'],
                                 data['has_hook'],
                                 data['has_too_long_line'],
                                 data['is_image'],
                                 data['other_problem'],
                                 data['has_interrupted_line'],
                                 data['id'],
                                 formulaid2latex[formula_id])
            b.preprocessing(preprocessing_queue)
            b_pll = b.get_pointlist()
            distance = float('inf')
            for A_pll in as_:
                distance = min(distance, dtw(A_pll, b_pll))
            if distance > 100:
                if data['administrator_edit'] is not None:
                    as_.append(b.get_pointlist())
                else:
                    if not alread_shown_in_browser:
                        alread_shown_in_browser = True
                        webbrowser.open("http://www.martin-thoma.de/"
                                        "write-math/view/?"
                                        "raw_data_id=%i" % data['id'], 2)
                    b.show()
                    if b.ok:
                        as_.append(b.get_pointlist())
                        update_data(cfg, b)
                    else:
                        update_data(cfg, b, True)
        logger.info("[Status] Checked formulas: %i of %i" %
                    (checked_formulas, len(formulaid2latex)))
        logger.info("[Status] Checked raw_data_instances: %i" %
                    checked_raw_data_instances)
    logger.info("done")

if __name__ == '__main__':
    from argparse import ArgumentParser

    parser = ArgumentParser(description=__doc__)

    # Add more options if you like
    parser.add_argument("-i", dest="i",
                        help="at which raw_data_id should it start?",
                        metavar="RAW_DATA_ID")
    args = parser.parse_args()
    cfg = utils.get_database_configuration()
    main(cfg, args.i)

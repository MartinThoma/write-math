#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""Sync the `wm_raw_draw_data`.`user_answers_count` and
   `wm_raw_draw_data`.`automated_answers_count` with the actual counts.
"""

import pymysql.cursors
import logging
import sys
from collections import defaultdict

import hwrt.utils

logging.basicConfig(format='%(asctime)s %(levelname)s %(message)s',
                    level=logging.DEBUG,
                    stream=sys.stdout)


def main(chunk_size=100):
    cfg = hwrt.utils.get_database_configuration()
    mysql = cfg['mysql_online']

    total_recordings = get_total_recordings(mysql)
    logging.info("Total recordings: %i", total_recordings)

    for offset in range(0, total_recordings, chunk_size):
        logging.info("Chunk %i/%i", offset, total_recordings)
        raw_data_ids = get_raw_data_ids(mysql, offset, chunk_size)
        min_id = min(raw_data_ids)
        max_id = max(raw_data_ids)
        logging.info("\t%i - %i", min_id, max_id)
        user_answers = get_user_answers(mysql, min_id, max_id)
        worker_answers = get_worker_answers(mysql, min_id, max_id)
        update(mysql, raw_data_ids, user_answers, worker_answers)


def get_total_recordings(mysql):
    """
    Parameters
    ----------
    mysql : dict
        Connection information
    """
    connection = pymysql.connect(host=mysql['host'],
                                 user=mysql['user'],
                                 passwd=mysql['passwd'],
                                 db=mysql['db'],
                                 charset='utf8mb4',
                                 cursorclass=pymysql.cursors.DictCursor)

    try:
        cursor = connection.cursor()
        sql = "SELECT COUNT(*) as `count` FROM `wm_raw_draw_data`"
        cursor.execute(sql)
        result = cursor.fetchone()
        return result['count']
    finally:
        connection.close()


def get_raw_data_ids(mysql, offset, chunk_size):
    """
    Parameters
    ----------
    mysql : dict
        Connection information
    offset : int
    chunk_size : int

    Returns
    -------
    list of integers :
        IDs within `wm_raw_draw_data`
    """
    connection = pymysql.connect(host=mysql['host'],
                                 user=mysql['user'],
                                 passwd=mysql['passwd'],
                                 db=mysql['db'],
                                 charset='utf8mb4',
                                 cursorclass=pymysql.cursors.DictCursor)

    try:
        cursor = connection.cursor()
        sql = "SELECT `id` FROM `wm_raw_draw_data` ORDER BY `id` LIMIT %s, %s"
        cursor.execute(sql, (offset, chunk_size))
        result = cursor.fetchall()
        return [r['id'] for r in result]
    finally:
        connection.close()


def get_user_answers(mysql, min_recording_id, max_recording_id):
    """
    Parameters
    ----------
    mysql : dict
        Connection information
    min_recording_id : int
    max_recording_id : int

    Returns
    -------
    list of dicts :
        IDs within `wm_raw_draw_data`
    """
    connection = pymysql.connect(host=mysql['host'],
                                 user=mysql['user'],
                                 passwd=mysql['passwd'],
                                 db=mysql['db'],
                                 charset='utf8mb4',
                                 cursorclass=pymysql.cursors.DictCursor)

    try:
        cursor = connection.cursor()
        sql = ("SELECT `recording_id`, COUNT(`recording_id`) as `count` "
               "FROM  `wm_partial_answer` "
               "WHERE %s <= `recording_id`  AND `recording_id` <= %s "
               "GROUP BY `recording_id` ")
        cursor.execute(sql, (min_recording_id, max_recording_id))
        result = cursor.fetchall()
        answer = defaultdict(int)
        for r in result:
            answer[int(r['recording_id'])] = r['count']
        return answer
    finally:
        connection.close()


def get_worker_answers(mysql, min_recording_id, max_recording_id):
    """
    Parameters
    ----------
    mysql : dict
        Connection information
    min_recording_id : int
    max_recording_id : int

    Returns
    -------
    list of dicts :
        IDs within `wm_raw_draw_data`
    """
    connection = pymysql.connect(host=mysql['host'],
                                 user=mysql['user'],
                                 passwd=mysql['passwd'],
                                 db=mysql['db'],
                                 charset='utf8mb4',
                                 cursorclass=pymysql.cursors.DictCursor)

    try:
        cursor = connection.cursor()
        sql = ("SELECT `raw_data_id`, COUNT(`raw_data_id`) as `count` "
               "FROM  `wm_worker_answers` "
               "WHERE %s <= `raw_data_id`  AND `raw_data_id` <= %s "
               "GROUP BY `raw_data_id` ")
        cursor.execute(sql, (min_recording_id, max_recording_id))
        result = cursor.fetchall()
        answer = defaultdict(int)
        for r in result:
            answer[int(r['raw_data_id'])] = r['count']
        return answer
    finally:
        connection.close()


def update(mysql, raw_data_ids, user_answers, worker_answers):
    """Update `wm_raw_draw_data`.`user_answers_count` and
   `wm_raw_draw_data`.`automated_answers_count` with the actual counts

    Parameters
    ----------
    mysql : dict
        Connection information
    raw_data_ids : IDs to update
    user_answers : actual counts
    worker_answers : actual counts
    """
    connection = pymysql.connect(host=mysql['host'],
                                 user=mysql['user'],
                                 passwd=mysql['passwd'],
                                 db=mysql['db'],
                                 charset='utf8mb4',
                                 cursorclass=pymysql.cursors.DictCursor)

    try:
        cursor = connection.cursor()
        for raw_data_id in raw_data_ids:
            sql = ("UPDATE `wm_raw_draw_data` "
                   "SET  `user_answers_count` = %s, "
                   "`automated_answers_count` = %s WHERE `id` = %s LIMIT 1;")
            data = (user_answers[raw_data_id],
                    worker_answers[raw_data_id],
                    raw_data_id)
            cursor.execute(sql, data)
        connection.commit()
    finally:
        connection.close()


def get_parser():
    from argparse import ArgumentParser, ArgumentDefaultsHelpFormatter
    parser = ArgumentParser(description=__doc__,
                            formatter_class=ArgumentDefaultsHelpFormatter)
    return parser


if __name__ == "__main__":
    args = get_parser().parse_args()
    main()

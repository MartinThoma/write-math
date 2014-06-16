#!/usr/bin/env python
# -*- coding: utf-8 -*-

import logging
import MySQLdb
import MySQLdb.cursors
from classification import *
from flask import Flask, request
from dbconfig import mysql

CLASSIFIER_NAME = "DTW-Python"

app = Flask(__name__)


def classifyD(raw_data_id, raw_draw_data, epsilon):
    global cursor

    if epsilon > 0:
        result_path = apply_douglas_peucker(pointLineList(raw_draw_data),
                                            epsilon)
    else:
        result_path = pointLineList(raw_draw_data)
    A = scale_and_center(list_of_pointlists2pointlist(result_path))

    # Get the first 4000 known formulas
    sql = ("SELECT `wm_raw_draw_data`.`id`, `data`, `accepted_formula_id`, "
           "`formula_in_latex`, `accepted_formula_id` as `formula_id`"
           "FROM `wm_raw_draw_data` "
           "JOIN  `wm_formula` ON  `wm_formula`.`id` =  `accepted_formula_id` "
           "LIMIT 4000")
    cursor.execute(sql)
    datasets = cursor.fetchall()
    print(datasets)

    results = classify(datasets, A)
    return json_encode(results)


@app.route('/', methods=['GET', 'POST'])
def index():
    if 'heartbeat' in request.args:
        return request.args['heartbeat']
    elif 'classify' in request.form:
        epsilon = 0
        if 'epsilon' in request.form:
            epsilon = request.form['epsilon']
        return classifyD(request.form['raw_data_id'],
                         request.form['classify'],
                         epsilon)
    return 'No action given'

if __name__ == '__main__':
    logging.basicConfig(filename='classifier.log',
                        level=logging.DEBUG,
                        format='%(asctime)s %(levelname)s: %(message)s')

    logging.info("Started classifier %s." % CLASSIFIER_NAME)
    logging.info("start establishing connection")
    connection = MySQLdb.connect(host=mysql['host'],
                                 user=mysql['user'],
                                 passwd=mysql['passwd'],
                                 db=mysql['db'],
                                 cursorclass=MySQLdb.cursors.DictCursor)
    cursor = connection.cursor()
    logging.info("end establishing connection")
    app.run(port=80)
    # set the secret key.  keep this really secret:
    app.secret_key = 'A0Zr98j/3yX R~XHH!jmN]LWX/,?RT'

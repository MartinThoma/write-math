#!/usr/bin/env python
# -*- coding: utf-8 -*-

from math import sqrt, exp
import logging
import sys
sys.path.append("/var/www/write-math/website/clients/python")
from HandwrittenData import HandwrittenData
# Database stuff
import MySQLdb
import MySQLdb.cursors
from dbconfig import mysql_local as mysql
sys.path.append("/var/www/write-math/website/clients/dtw-python")
from classification import dtw, pointLineList

import sys
import preprocessing


def modified_show():
    import numpy as np
    import matplotlib.pyplot as plt
    from matplotlib.widgets import Button
    freqs = np.arange(2, 20, 3)

    fig, ax = plt.subplots()
    plt.subplots_adjust(bottom=0.2)
    t = np.arange(0.0, 1.0, 0.001)
    s = np.sin(2*np.pi*freqs[0]*t)
    l, = plt.plot(t, s, lw=2)


    class Index:
        ind = 0
        def next(self, event):
            self.ind += 1
            i = self.ind % len(freqs)
            ydata = np.sin(2*np.pi*freqs[i]*t)
            l.set_ydata(ydata)
            plt.draw()

        def prev(self, event):
            self.ind -= 1
            i = self.ind % len(freqs)
            ydata = np.sin(2*np.pi*freqs[i]*t)
            l.set_ydata(ydata)
            plt.draw()

    callback = Index()
    axprev = plt.axes([0.7, 0.05, 0.1, 0.075])
    axnext = plt.axes([0.81, 0.05, 0.1, 0.075])
    bnext = Button(axnext, 'Next')
    bnext.on_clicked(callback.next)
    bprev = Button(axprev, 'Previous')
    bprev.on_clicked(callback.prev)

    plt.show()


def query_yes_no(question, default="yes"):
    """Ask a yes/no question via raw_input() and return their answer.

    "question" is a string that is presented to the user.
    "default" is the presumed answer if the user just hits <Enter>.
        It must be "yes" (the default), "no" or None (meaning
        an answer is required of the user).

    The "answer" return value is one of "yes" or "no".
    """
    valid = {"yes":True,   "y":True,  "ye":True,
             "no":False,     "n":False}
    if default == None:
        prompt = " [y/n] "
    elif default == "yes":
        prompt = " [Y/n] "
    elif default == "no":
        prompt = " [y/N] "
    else:
        raise ValueError("invalid default answer: '%s'" % default)

    while True:
        sys.stdout.write(question + prompt)
        choice = raw_input().lower()
        if default is not None and choice == '':
            return valid[default]
        elif choice in valid:
            return valid[choice]
        else:
            sys.stdout.write("Please respond with 'yes' or 'no' "\
                             "(or 'y' or 'n').\n")


def main(raw_data_start_id):
    connection = MySQLdb.connect(host=mysql['host'],
                                 user=mysql['user'],
                                 passwd=mysql['passwd'],
                                 db=mysql['db'],
                                 cursorclass=MySQLdb.cursors.DictCursor)
    cursor = connection.cursor()

    # Get formulas
    print("Get formulas")
    sql = ("SELECT `id`, `formula_in_latex` FROM `wm_formula`")
    cursor.execute(sql)
    formulas = cursor.fetchall()
    formulaid2latex = {}
    for el in formulas:
        formulaid2latex[el['id']] = el['formula_in_latex']

    preprocessing_queue = [(preprocessing.scale_and_shift, []),
                           # (preprocessing.douglas_peucker,
                           #  {'EPSILON': 0.2}),
                           # (preprocessing.space_evenly,
                           #  {'number': 100,
                           #   'KIND': 'cubic'})
                           ]

    for formula_id in formulaid2latex.keys():
        if formula_id == 1:
            # This formula id is for trash. No need to look at it.
            continue
        # Get data
        print("Get data for formula_id %i (%s)" % (formula_id,
                                                   formulaid2latex[formula_id]))
        sql = ("SELECT `id`, `data`, `accepted_formula_id`, "
               "`wild_point_count`, `missing_line`, `has_hook`, "
               "`has_too_long_line` "
               "FROM  `wm_raw_draw_data` "
               "WHERE `accepted_formula_id` = %i;" % formula_id)
        cursor.execute(sql)
        raw_datasets = cursor.fetchall()
        print("Raw datasets: %i" % len(raw_datasets))
        As = []
        for i, data in enumerate(raw_datasets):
            if len(As) == 0:
                A = HandwrittenData(data['data'])
                A.preprocessing(preprocessing_queue)
                A.show()
                answer = query_yes_no("Is raw_data_id %i a %s?" %
                                      (data['id'],
                                       formulaid2latex[formula_id]))
                if answer:
                    As.append(A.get_pointlist())
            else:
                B = HandwrittenData(data['data'])
                B.preprocessing(preprocessing_queue)
                B_pll = B.get_pointlist()
                distance = float('inf')
                for A_pll in As:
                    distance = min(distance, dtw(A_pll, B_pll))
                if distance > 100:
                    B.show()
                    answer = query_yes_no("Is raw_data_id %i a %s? (distance was %0.2f)" %
                                          (data['id'],
                                           formulaid2latex[formula_id],
                                           distance))
                    if answer:
                        As.append(pointLineList(data['data']))
                else:
                    print("worked")

    print("done")

if __name__ == '__main__':
    from argparse import ArgumentParser

    parser = ArgumentParser()

    # Add more options if you like
    parser.add_argument("-i", dest="i",
                        help="at which raw_data_id should it start?",
                        metavar="RAW_DATA_ID")
    args = parser.parse_args()
    main(args.i)

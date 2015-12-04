#!/usr/bin/env python

import sys
if sys.version_info < (3, 0):
    # If it is Python 2, then I want the Python 3 open function
    from future.builtins import open

import csv
id_counter = {}

with open('complete.csv', 'rt', newline='') as csvfile:
    csvreader = csv.reader(csvfile, delimiter=';', quotechar="'")
    next(csvreader, None)  # skip the headers
    for row in csvreader:
        # print(row)
        # print(len(row))
        symbol_id, user_id, data, user_agent = row
        if symbol_id in id_counter:
            id_counter[symbol_id] += 1
        else:
            id_counter[symbol_id] = 1

    for symbol_id, counter in sorted(id_counter.items(),
                                     key=lambda n: n[1],
                                     reverse=True):
        # print("%s: %i" % (symbol_id, counter))
        print(counter)

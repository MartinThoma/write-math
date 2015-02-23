#!/usr/bin/env python

try:
    from future.builtins import open
except:
    pass

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
        #print("%s: %i" % (symbol_id, counter))
        print(counter)

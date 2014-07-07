#!/usr/bin/env python

import cPickle as pickle

a = pickle.load(open('cv_datasets.pickle'))
s = ""
for symbol, count in sorted(a['symbols'].items(), key=lambda n: n[0]):
    if symbol in ['a', '0', 'A']:
        s += "\n%s (%i), " % (symbol, count)
    elif symbol in ['z', '9', 'Z']:
        s += "%s (%i) \n" % (symbol, count)
    else:
        s += "%s (%i), " % (symbol, count)
print("```")
print(s)
print("```")
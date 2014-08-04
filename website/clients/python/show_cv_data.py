#!/usr/bin/env python
"""
Print which symbols are contained in a crossvalidation datasets.pickle file.
"""

import cPickle as pickle


def main(picklefile):
    a = pickle.load(open(picklefile))
    print(a.keys())
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

if __name__ == '__main__':
    from argparse import ArgumentParser
    parser = ArgumentParser(description=__doc__)
    parser.add_argument("-f", "--file", dest="picklefile",
                        default='cv_datasets.pickle',
                        help="where is the picklefile", metavar="FILE")
    args = parser.parse_args()
    main(args.picklefile)

#!/usr/bin/env python

import imp

required_modules = ['argparse', 'matplotlib']
all_ok = True

for required_module in required_modules:
    try:
        imp.find_module(required_module)
        check = "module '%s' ... found" % required_module
        if hasattr(required_module, '__version__'):
            check += " (version: %s)" % str(required_module.__version__)
        print(check)

    except ImportError:
        print("module '%s' ... NOT found" % required_module)
        all_ok = False

if all_ok:
    import argparse
    print("argparse version: %s (1.1 tested)" % argparse.__version__)
    import matplotlib
    print("matplotlib version: %s (1.2.1 tested)" % matplotlib.__version__)

#!/usr/bin/env python

import imp


def which(program):
    import os

    def is_exe(fpath):
        return os.path.isfile(fpath) and os.access(fpath, os.X_OK)

    fpath, fname = os.path.split(program)
    if fpath:
        if is_exe(program):
            return program
    else:
        for path in os.environ["PATH"].split(os.pathsep):
            path = path.strip('"')
            exe_file = os.path.join(path, program)
            if is_exe(exe_file):
                return exe_file

    return None


def check_python_modules():
    print("## Check modules")
    required_modules = ['argparse', 'matplotlib', 'natsort', 'MySQLdb',
                        'cPickle', 'detl', 'theano', 'dropbox',
                        'webbrowser', 'hashlib', 'shapely']
    found = []
    for required_module in required_modules:
        try:
            imp.find_module(required_module)
            check = "module '%s' ... found" % required_module
            print(check)
            found.append(required_module)
        except ImportError:
            print("module '%s' ... NOT found" % required_module)

    if "argparse" in found:
        import argparse
        print("argparse version: %s (1.1 tested)" % argparse.__version__)
    if "matplotlib" in found:
        import matplotlib
        print("matplotlib version: %s (1.2.1 tested)" % matplotlib.__version__)
    if "natsort" in found:
        import natsort
        print("natsort version: %s (3.4.0 tested, 3.4.0 > required)" %
              natsort.__version__)
    if "MySQLdb" in found:
        import MySQLdb
        print("MySQLdb version: %s (1.2.3 tested)" %
              MySQLdb.__version__)
    if "theano" in found:
        import theano
        print("theano version: %s (0.6.0 tested)" %
              theano.__version__)
    if "shapely" in found:
        import shapely
        print("shapely version: %s (1.2.14 tested)" %
              shapely.__version__)
    if "cPickle" in found:
        import cPickle
        print("cPickle version: %s (1.71 tested)" %
              cPickle.__version__)
        print("cPickle HIGHEST_PROTOCOL: %s (2 required)" %
              cPickle.HIGHEST_PROTOCOL)


def check_executables():
    print("## Check executables")
    required_executables = ["pfile_create"]
    for executable in required_executables:
        path = which(executable)
        if path is None:
            print("%s ... NOT found" % executable)
        else:
            print("%s ... found at %s" % (executable, path))


def main():
    check_python_modules()
    check_executables()

if __name__ == '__main__':
    main()

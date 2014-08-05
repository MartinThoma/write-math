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
    required_modules = ['argparse', 'matplotlib', 'natsort', 'detl']
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
        import natsort
        print("natsort version: %s (3.4.0 tested, 3.4.0 > required)" %
              natsort.__version__)


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

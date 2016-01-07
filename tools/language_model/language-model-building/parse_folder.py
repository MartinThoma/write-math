#!/usr/bin/env python

import fnmatch
import os
from argparse import ArgumentParser
import json
import subprocess


def combine_known_symbols(kn1, kn2):
    """
    Add all values of one dictionary to another dictionary.

    Parameters
    ----------
    kn1 : dict
    kn2 : dict

    Returns
    -------
    dict
        Combined dictionary
    """
    for key, value in kn2.items():
        if key not in kn1:
            kn1[key] = value
        else:
            kn1[key] += value
    return kn1


def parse_folder(folder):
    """
    Parse all LaTeX root files for symbols.

    Parameters
    ----------
    folder : str

    Returns
    -------
    dict :
        Symbols
    """
    matches = []
    for root, dirnames, filenames in os.walk(folder):
        for filename in fnmatch.filter(filenames, '*.tex'):
            matches.append(os.path.join(root, filename))
    known_symbols = {}
    for filename in matches:
        if is_latex_root(filename):
            print(filename)
            # TODO: Fix this!
            proc = subprocess.Popen(["./build-language-model.py", "-f %s" %
                                     filename,
                                     "-o out.txt"],
                                    stdout=subprocess.PIPE, shell=True)
            (out, err) = proc.communicate()
            with open("out.txt") as f:
                out = f.read()
            kn2 = json.loads(out)
            known_symbols = combine_known_symbols(known_symbols, kn2)
    return known_symbols


def is_latex_root(filename):
    """
    Check if a file is a LaTeX root file.

    Parameters
    ----------
    filename : str
        Path to a text file which could be a LaTeX file

    Returns
    -------
    bool :
        True, iff it is a LaTeX root file.
    """
    with open(filename) as f:
        content = f.read()
    return "\\documentclass" in content


def print_known_symbols(known_symbols):
    """
    Print which symbols were found and how often they were found.

    Parameters
    ----------
    known_symbols : dict
    """
    for latex, counter in sorted(known_symbols.items(),
                                 key=lambda x: x[1],
                                 reverse=True):
        if counter > 0:
            print("%s: %i" % (latex, counter))


if __name__ == '__main__':
    parser = ArgumentParser()
    folder = '/home/moose/Downloads/LaTeX-examples/'
    parser.add_argument("-f", "--folder", dest="folder",
                        default=folder,
                        help="folder with multiple LaTeX files",
                        metavar="FOLDER")
    args = parser.parse_args()
    known_symbols = parse_folder(args.folder)
    print_known_symbols(known_symbols)

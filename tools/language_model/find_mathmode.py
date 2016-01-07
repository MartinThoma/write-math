#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""Get math mode environments from text file."""

import os
import re
import codecs
import logging


def main(filename):
    """
    Get all mathmode environments within a file and print them.

    Parameters
    ----------
    filename : str
        Path to a LaTeX file.
    """
    math_mode = get_math_mode(filename)
    for i, el in enumerate(math_mode):
        print("%i.\t%s" % (i, el.replace('\n', '\\n')))


def get_math_mode(filename):
    """
    Read `filename` and get all math mode contents from it.

    Parameters
    ----------
    filename : str
        Path to a TeX file

    Returns
    -------
    list of math mode contents
    """
    with codecs.open(filename, 'r', 'utf-8') as f:
        lines = f.read()

    lines = extract_document_body(lines)
    if len(lines) == 0:
        return []
    elif len(lines) > 1:
        logging.debug("File '%s' has %i document environments" %
                      (filename, len(lines)))
    else:
        lines = lines[0]

    # strip comment lines
    lines = lines.split("\n")
    new_lines = []
    for line in lines:
        if not line.strip().startswith("%"):
            new_lines.append(line)
    lines = "\n".join(new_lines)

    # match mathmode
    p1 = re.compile('\$(.*?)\$', re.DOTALL)
    p2 = re.compile('\\[(.+?)\\\]')
    matches = p1.findall(lines)
    matches += p2.findall(lines)
    return matches


def extract_environments(env, text):
    """
    Get the content of all environments 'environment' as a list.

    Parameters
    ----------
    env : string
        Name of the environment
    text : string
        Text to parse for environment

    Returns
    -------
    list
        List of matches
    """
    document = re.compile('\\\\begin{%s}(.*?)\\\\end{%s}' % (env, env),
                          re.MULTILINE | re.DOTALL)
    a = document.findall(text)
    return a


def extract_document_body(text):
    """
    Parameters
    ----------
    text : str
        Where to get the body from

    Returns
    -------
    str
    """
    return extract_environments('document', text)


def unfold_math(expression):  # TODO
    tree = {}
    return tree


def is_valid_file(parser, arg):
    """
    Check if arg is a valid file that already exists on the file system.

    Parameters
    ----------
    parser : argparse object
    arg : str

    Returns
    -------
    arg
    """
    arg = os.path.abspath(arg)
    if not os.path.exists(arg):
        parser.error("The file %s does not exist!" % arg)
    else:
        return arg


def get_parser():
    """Get parser object for script find_mathmode.py."""
    from argparse import ArgumentParser, ArgumentDefaultsHelpFormatter
    parser = ArgumentParser(description=__doc__,
                            formatter_class=ArgumentDefaultsHelpFormatter)
    parser.add_argument("-f", "--file",
                        dest="filename",
                        required=True,
                        type=lambda x: is_valid_file(parser, x),
                        help="write report to FILE",
                        metavar="FILE")
    return parser


if __name__ == "__main__":
    args = get_parser().parse_args()
    main(args.filename)

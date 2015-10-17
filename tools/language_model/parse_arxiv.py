#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""Go through arXiv data.

You can download arXiv data by s3cmd:

1. pip install s3cmd
2. s3cmd --configure
3. s3cmd get --recursive --skip-existing s3://arxiv/src/ --requester-pays
"""

import os
from os import listdir
from os.path import isfile, join
import tarfile
import logging
import sys
import pkg_resources
import codecs
import gzip
import string

from find_mathmode import get_math_mode
import parse_mathmode

logging.basicConfig(format='%(asctime)s %(levelname)s %(message)s',
                    level=logging.DEBUG,
                    stream=sys.stdout)

import struct
from gzip import FEXTRA, FNAME


def read_gzip_info(gzipfile):
    gf = gzipfile.fileobj
    pos = gf.tell()

    # Read archive size
    gf.seek(-4, 2)
    size = struct.unpack('<I', gf.read())[0]

    gf.seek(0)
    magic = gf.read(2)
    if magic != '\037\213':
        raise IOError('Not a gzipped file')

    method, flag, mtime = struct.unpack("<BBIxx", gf.read(8))

    if not flag & FNAME:
        # Not stored in the header, use the filename sans .gz
        gf.seek(pos)
        fname = gzipfile.name
        if fname.endswith('.gz'):
            fname = fname[:-3]
        return fname, size

    if flag & FEXTRA:
        # Read & discard the extra field, if present
        gf.read(struct.unpack("<H", gf.read(2)))

    # Read a null-terminated string containing the filename
    fname = []
    while True:
        s = gf.read(1)
        if not s or s == '\000':
            break
        fname.append(s)

    gf.seek(pos)
    return ''.join(fname), size


def main(directory):
    vocabulary = get_vocabulary()
    unknown = {}
    unknown_extensions = {}
    unigrams = {}
    for word in vocabulary:
        unigrams[word] = 0

    onlyfiles = [f for f in listdir(directory) if isfile(join(directory, f))]
    tarfiles = sorted([os.path.join(directory, f)
                       for f in onlyfiles if f.endswith('.tar')])
    for tar_filename in tarfiles:
        files_by_project = get_data(directory, tar_filename)
        for project in files_by_project:
            for filename in project:
                extensions = ['.eps', '.epsf', '.epsi', '.epsfrag',
                              '.ps', '.postscript', '.pstex', '.pstex_t',
                              '.sty', '.cls', '.bbl', '.bst', '.clo', '.log',
                              '.mp',
                              '.gif', '.jpg', '.png', '.jpeg', '.pdf',
                              '.html', '.htm', '.doc']
                digits = string.digits
                if any([filename.lower().endswith(e) for e in extensions]):
                    continue
                elif any([filename.lower().endswith(e) for e in digits]):
                    continue
                elif not filename.lower().endswith('.tex'):
                    _, file_extension = os.path.splitext(filename)
                    file_extension = file_extension.lower()
                    if file_extension in unknown_extensions:
                        unknown_extensions[file_extension].append(filename)
                    else:
                        unknown_extensions[file_extension] = [filename]
                try:
                    mathmode_contents = get_math_mode(filename)
                except:
                    logging.debug("get_math_mode error with %s.", filename)
                for mcontent in mathmode_contents:
                    tokens = parse_mathmode.tokenize(mcontent,
                                                     filename=filename)
                    # logging.debug(tokens)
                    for token in tokens:
                        if not isinstance(token, basestring):
                            # parse_mathmode.Environment
                            # parse_mathmode.Block
                            pass
                        elif token in unigrams:
                            unigrams[token] += 1
                        elif token in ["{", "}", "_", "^"]:
                            pass
                        elif token in [r"\left", r"\right"]:
                            pass
                        elif token in [r"\,", r"~"]:
                            pass
                        elif token in [r"\cal", r"\mathcal", r"\mathbb",
                                       r"\mathbf",
                                       r"\bf", r"\mathrm", r"\over",
                                       r"\rm", r"\sqrt",
                                       r"\bar", r"\vec", r"\overline",
                                       r"\tilde", r"\frac", r"\label"]:
                            pass
                        elif token in [r"\to", r"\mit"]:
                            pass
                        else:
                            if token in unknown:
                                unknown[token].append(filename)
                            else:
                                unknown[token] = [filename]

        print("\n## Unigrams (Total: %i)" %
              sum([el[1] for el in unigrams.items()]))
        for k, v in sorted(unigrams.items(), key=lambda n: n[1], reverse=True):
            if v > 0:
                print("%i:\t%s" % (v, k))
        print("\n## Unknown Tokens")
        for k, v in sorted(unknown.items(),
                           key=lambda n: len(n[1]),
                           reverse=True)[:50]:
            if len(v) > 2:
                print("%i:\t%s" % (len(v), k))

        print("\n## Unknown Extensions")
        for k, v in sorted(unknown_extensions.items(),
                           key=lambda n: len(n[1]),
                           reverse=True)[:50]:
            if len(v) > 2:
                print("%i:\t%s" % (len(v), k))
        sys.exit()


def get_vocabulary():
    vocabulary_file = pkg_resources.resource_filename('hwrt',
                                                      'misc/vocabulary.txt')
    with codecs.open(vocabulary_file, 'r', 'utf-8') as f:
        vocabulary = f.read()
    return vocabulary.split(u"\n")[:-1]


def get_data(directory, tar_filename):
    """
    Extract data and return filenames, grouped by paper.

    Parameters
    ----------
    directory : string
        The path to a directory which contains .gz files of the arXiv.

    Returns
    -------
    list of lists
        Each sublist belongs to a publication and contains paths to files.
    """
    extracted_by_project = []

    working_directory = os.path.join(directory, '.cache')
    if not os.path.exists(working_directory):
        os.makedirs(working_directory)
    logging.info(tar_filename)

    # Extract all .gz files in .tar file
    extracted = []
    with tarfile.open(tar_filename) as tar:
        extracted = tar.getnames()
        tar.extractall(path=working_directory)
    extracted = [os.path.join(working_directory, f)
                 for f in extracted if f.endswith('.gz')]

    # Extract all files within .gz files
    for gz_file in extracted:
        try:
            extracted_by_project.append([])
            with tarfile.open(gz_file, 'r:gz') as tar:
                sub_workdir = gz_file[:-3]
                if not os.path.exists(sub_workdir):
                    os.makedirs(sub_workdir)
                ext = tar.getnames()
                tar.extractall(path=sub_workdir)
            for filename in ext:
                full_path_filename = os.path.join(sub_workdir, filename)
                extracted_by_project[-1].append(full_path_filename)
            # logging.info("%s done.", gz_file)
        except:
            try:
                extracted_by_project.append([])
                with gzip.open(gz_file, 'rb') as f:
                    file_content = f.read()
                    sub_workdir = gz_file[:-3]
                    if not os.path.exists(sub_workdir):
                        os.makedirs(sub_workdir)
                    ext, _ = read_gzip_info(f)
                    with open(os.path.join(sub_workdir, ext), 'wb') as f2:
                        f2.write(file_content)
            except Exception as inst2:
                logging.warning("Didn't work for %s", gz_file)
                logging.warning(inst2)
    return extracted_by_project


def get_parser():
    from argparse import ArgumentParser, ArgumentDefaultsHelpFormatter
    parser = ArgumentParser(description=__doc__,
                            formatter_class=ArgumentDefaultsHelpFormatter)
    parser.add_argument("-d", "--directory",
                        dest="directory",
                        help="look in this DIR for arXiv .tar files",
                        metavar="DIR",
                        required=True)
    return parser


if __name__ == "__main__":
    args = get_parser().parse_args()
    main(args.directory)

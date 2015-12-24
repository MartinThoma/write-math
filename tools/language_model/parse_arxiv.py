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
import time
import math
import pickle

# My modules
from find_mathmode import get_math_mode
import parse_mathmode as pm

try:
    unicode = unicode
except NameError as e:
    # 'unicode' is undefined, must be Python 3
    logging.info("Python 3 detected")
    str = str
    unicode = str
    bytes = bytes
    basestring = (str, bytes)
else:
    # 'unicode' exists, must be Python 2
    str = str
    unicode = unicode
    bytes = str
    basestring = basestring

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


def update_ngrams(ngrams, filename, token_stream):
    """
    Insert the data from token_stream into the ngram dict.

    Parameters
    ----------
    ngrams : dict
    filename : str
        Where the data was extracted from.
    token_stream : list
        List of tokens. Each token should either be in the vocabulary, or be
        '<s>', '<n>', '</n><d>', '</d>', '</s>', '<unk>'
    """

    # TODO: Language model config file
    all_ignore = ['_', '^', '{', '}', '\\right', '\\left',
                  '\\mathrm', '\\mathcal', '\\mathbf', '\\mbox',
                  '&', '%', '<n>', '</n><d>', '</d>', '<unk>']

    # Update unigrams
    ts = []
    for token in token_stream:
        # TODO: Language model config file
        single_ignore = ['<s>', '</s>'] + all_ignore
        if token in single_ignore:
            continue
        if not isinstance(token, basestring):
            # pm.Environment  # TODO - how to deal with that?
            # pm.Block
            pass
        elif token in ngrams['unigrams']:
            ts.append(token)
            if filename in ngrams['unigrams'][token]:
                ngrams['unigrams'][token][filename] += 1
            else:
                ngrams['unigrams'][token][filename] = 1
        else:
            ts.append("<unk>")
            if token in ngrams['unknown']:
                ngrams['unknown'][token].append(filename)
            else:
                ngrams['unknown'][token] = [filename]

    ts = ["<s>"] + ts + ["</s>"]

    for t1, t2 in zip(ts, ts[1:]):
        if t1 in ngrams['bigrams']:
            if t2 in ngrams['bigrams'][t1]:
                ngrams['bigrams'][t1][t2] += 1
            else:
                ngrams['bigrams'][t1][t2] = 1
        else:
            ngrams['bigrams'][t1] = {t2: 1}

    for t1, t2, t3 in zip(ts, ts[1:], ts[2:]):
        if t1 in ngrams['trigrams']:
            if t2 in ngrams['trigrams'][t1]:
                if t3 in ngrams['trigrams'][t1][t2]:
                    ngrams['trigrams'][t1][t2][t3] += 1
                else:
                    ngrams['trigrams'][t1][t2][t3] = 1
            else:
                ngrams['trigrams'][t1][t2] = {t3: 1}
        else:
            ngrams['trigrams'][t1] = {t2: {t3: 1}}


def main(directory, refresh):
    vocabulary = get_vocabulary()
    ngrams_g = {'unknown': {},
                'unigrams': {},
                'bigrams': {},
                'trigrams': {}
                }
    unknown_extensions_g = {}
    for word in vocabulary:
        ngrams_g['unigrams'][word] = {}

    onlyfiles = [f for f in listdir(directory) if isfile(join(directory, f))]
    tarfiles = sorted([os.path.join(directory, f)
                       for f in onlyfiles if f.endswith('.tar')])
    for tarfiles_done, tar_filename in enumerate(tarfiles, start=1):
        # check if this file was already analyzed
        summary_file = os.path.join(directory,
                                    "%s.summary.pickle" % tar_filename)
        if not os.path.isfile(summary_file) or refresh:
            # Initialize
            ngrams_t = {'unknown': {},
                        'unigrams': {},
                        'bigrams': {},
                        'trigrams': {}
                        }
            unknown_exts_t = {}
            for word in vocabulary:
                ngrams_t['unigrams'][word] = {}

            # Start work
            files_by_project = get_data(directory, tar_filename)
            for project in files_by_project:
                for filename in project:
                    extensions = []
                    digits = string.digits
                    if any(filename.lower().endswith(e) for e in extensions):
                        continue
                    elif any(filename.lower().endswith(e) for e in digits):
                        continue
                    elif not filename.lower().endswith('.tex'):
                        _, file_extension = os.path.splitext(filename)
                        file_extension = file_extension.lower()
                        if file_extension in unknown_exts_t:
                            unknown_exts_t[file_extension].append(filename)
                        else:
                            unknown_exts_t[file_extension] = [filename]
                        continue
                    mathmode_contents = []
                    try:
                        mathmode_contents = get_math_mode(filename)
                    except:
                        logging.debug("get_math_mode error with %s.", filename)
                    for mcontent in mathmode_contents:
                        token_stream = pm.tokenize(mcontent,
                                                   filename=filename)

                        # Skip empty streams
                        if token_stream == ["<s>", "</s>"]:
                            continue

                        # Writing this slows execution VERY much down!
                        # with codecs.open("complete-tokens.txt",
                        #                  'a+', 'utf-8') as f:
                        #     try:
                        #         f.write("%s\n" % json.dumps(token_stream))
                        #     except:
                        #         pass
                        update_ngrams(ngrams_t, filename, token_stream)
            # Serialize data
            with open(summary_file, 'wb') as handle:
                pickle.dump({'ngrams': ngrams_t,
                             'unknown_extensions': unknown_exts_t},
                            handle,
                            protocol=pickle.HIGHEST_PROTOCOL)
        else:
            logging.info("%s found.", summary_file)
        # Deserialize data
        update_data(ngrams_g, unknown_extensions_g, summary_file)
        store_data_lm("lm-data-%s-%i.md" % (time.strftime("%H-%M"),
                                            tarfiles_done),
                      ngrams_g,
                      unknown_extensions_g)


def update_data(ngrams, unknown_extensions, summary_file):
    """
    Update the ngrams datastructure as well as the list of unknown extensions
    with data from the summary file.
    """
    with open(summary_file, 'rb') as handle:
        data = pickle.load(handle)

    for key in ['unknown']:
        if key in ngrams:
            for gram, value in data['ngrams'][key].items():
                if gram in ngrams[key]:
                    for filename in data['ngrams'][key][gram]:
                        if filename not in ngrams[key][gram]:
                            ngrams[key][gram].append(filename)
                else:
                    ngrams[key][gram] = value
        else:
            ngrams[key] = data['ngrams'][key]

    for key in ['unigrams']:
        if key in ngrams:
            for gram, value in data['ngrams'][key].items():
                if gram in ngrams[key]:
                    for filename, count in data['ngrams'][key][gram].items():
                        if filename in ngrams[key][gram]:
                            ngrams[key][gram][filename] += count
                        else:
                            ngrams[key][gram][filename] = count
                else:
                    ngrams[key][gram] = value
        else:
            ngrams[key] = data['ngrams'][key]

    for w1, v1 in data['ngrams']['bigrams'].items():
        if w1 in ngrams['bigrams']:
            for w2, count in v1.items():
                if w2 in ngrams['bigrams'][w1]:
                    ngrams['bigrams'][w1][w2] += count
                else:
                    ngrams['bigrams'][w1][w2] = count
        else:
            ngrams['bigrams'][w1] = v1

    for w1, v1 in data['ngrams']['trigrams'].items():
        if w1 in ngrams['trigrams']:
            for w2, v2 in v1.items():
                if w2 in ngrams['trigrams'][w1]:
                    for w3, count in v2.items():
                        if w3 in ngrams['trigrams'][w1][w2]:
                            ngrams['trigrams'][w1][w2][w3] += count
                        else:
                            ngrams['trigrams'][w1][w2][w3] = count
                else:
                    ngrams['trigrams'][w1][w2] = v2
        else:
            ngrams['trigrams'][w1] = v1

    # update unknown extensions
    for ext, count in data['unknown_extensions'].items():
        if ext in unknown_extensions:
            unknown_extensions[ext] += count
        else:
            unknown_extensions[ext] = count


def store_data_lm(filename, ngrams, unknown_extensions):
    """
    Parameters
    ----------
    filename : str
    ngrams: dict of dicts of dicts of ints:
        {'unigrams':
            {'\int': {'paper1': 1, 'paper2': 2},
             '\pi': {'paperx': 3, 'papery': 2}, ...}
         'unknown':
            {'heartsuit': ['paper1', 'paper2', ...]}
    unknown_extensions : dict of ints
        {'jpg': 3, 'png': 5, ...}
    """
    unigrams = ngrams['unigrams']
    unknown = ngrams['unknown']

    directory = os.path.dirname(os.path.realpath(__file__))
    directory = os.path.join(directory, time.strftime("%Y-%m-%d"))
    if not os.path.exists(directory):
        os.makedirs(directory)
    filename = os.path.join(directory, filename)
    with codecs.open(filename, 'w', 'utf-8') as f:
        f.write("\n## Unigrams (Total: %i)\n" %
                sum([v for _, el in unigrams.items() for k, v in el.items()]))
        for k, v in sorted(unigrams.items(),
                           key=lambda n: (sum([v for _, v in n[1].items()]),
                                          n[0]),
                           reverse=True):
            v = sorted(v.items(),
                       key=lambda n: n[1],
                       reverse=True)[:3]
            f.write(u"%i:\t%s\t%s\n" %
                    (sum([val for _, val in v]),
                     k,
                     v[:3]))
        f.write("\n## Unknown Tokens\n")
        for k, v in sorted(unknown.items(),
                           key=lambda n: (len(n[1]), n[0]),
                           reverse=True)[:500]:
            if len(v) > 2:
                f.write(u"%i:\t%s\t%s\n" % (len(v), k, v[:10]))

        f.write("\n## Extensions\n")
        for k, v in sorted(unknown_extensions.items(),
                           key=lambda n: (len(n[1]), n[0]),
                           reverse=True)[:200]:
            if len(v) > 2:
                f.write(u"%i:\t%s\n" % (len(v), k))

    filename = os.path.join(directory,
                            "ngram-%s.txt" % (time.strftime("%Y-%m-%d-%H-%M")))
    write_ngrams(ngrams, filename)


def write_ngrams(ngrams, filename):
    """
    Write ngrams in [ngram format](http://www.speech.sri.com/projects/srilm/
        manpages/ngram-format.5.html)

    Parameters
    ----------
    ngrams : dict
    filename : str
    """
    with codecs.open(filename, 'w', 'utf-8') as f:
        f.write("\\data\\\n")
        f.write("ngram 1=%i\n" % len(ngrams['unigrams']))
        f.write("ngram 2=%i\n" % len([1 for w1 in ngrams['bigrams']
                                      for w2 in ngrams['bigrams'][w1]]))
        f.write("ngram 3=%i\n" % len([1 for w1 in ngrams['trigrams']
                                      for w2 in ngrams['trigrams'][w1]
                                      for w3 in ngrams['trigrams'][w1][w2]]))

        k = 1  # Laplace smoothing / add-k estimation

        # 1-grams
        f.write("\n\\1-grams:\n")
        unk_count = sum([len(c) for _, c in ngrams['unknown'].items()])
        total = sum([v
                     for _, el in ngrams['unigrams'].items()
                     for _, v in el.items()]) + unk_count
        total = math.log10(total)
        vocabulary_size = total
        prob = math.log10(unk_count) - total
        f.write("{prob}\t{word}\n".format(prob=prob,
                                          word="<unk>"))
        write_list = []
        for word, literatur_list in ngrams['unigrams'].items():
            count = sum([v for _, v in literatur_list.items()])
            if count == 0:
                prob = -99.0
            else:
                prob = math.log10(count) - total
            write_list.append((word, prob))
        write_list = sorted(write_list,
                            key=lambda n: (n[1], n[0]),
                            reverse=True)
        for word, prob in write_list:
            f.write(u"{prob}\t{word}\n".format(prob=prob,
                                               word=word))

        # 2-grams
        f.write("\n\\2-grams:\n")
        discount = k * vocabulary_size
        write_list = []
        for w1, t1 in ngrams['bigrams'].items():
            # total number of bigrams starting with w1
            total = sum([bi_count for w2, bi_count in t1.items()])
            total += discount
            total = math.log10(total)

            for w2, count in t1.items():
                prob = math.log10(count) - total
                word = u"%s\t%s" % (w1, w2)
                write_list.append((word, prob))
        write_list = sorted(write_list,
                            key=lambda n: (n[1], n[0]),
                            reverse=True)
        for word, prob in write_list:
            f.write(u"{prob}\t{word}\n".format(prob=prob,
                                               word=word))

        # 3-grams
        f.write("\n\\3-grams:\n")
        discount = k * vocabulary_size**2
        write_list = []
        for w1, t1 in ngrams['trigrams'].items():
            for w2, t2 in t1.items():
                # total number of trigrams starting with w1 and ending with w3
                total = sum([count for _, count in t2.items()])
                total += discount
                total = math.log10(total)
                for w3, count in t2.items():
                    prob = math.log10(count) - total
                    word = u"%s\t%s\t%s" % (w1, w2, w3)
                    write_list.append((word, prob))
        write_list = sorted(write_list,
                            key=lambda n: (n[1], n[0]),
                            reverse=True)
        for word, prob in write_list:
            f.write(u"{prob}\t{word}\n".format(prob=prob,
                                               word=word))
        f.write("\n\\end\\\n")


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
    tar_filename : string
        The name of the file which should get analyzed

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
    parser.add_argument("-r", "--refresh",
                        dest="refresh",
                        help="don't use intermediate results",
                        default=False,
                        action="store_true")
    return parser


if __name__ == "__main__":
    args = get_parser().parse_args()
    main(args.directory, args.refresh)

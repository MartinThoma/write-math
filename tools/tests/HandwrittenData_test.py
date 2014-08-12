#!/usr/bin/env python

import sys
sys.path.append("..")
from HandwrittenData import HandwrittenData
import os


def get_all_symbols():
    current_folder = os.path.dirname(os.path.realpath(__file__))
    symbol_folder = os.path.join(current_folder, "symbols")
    symbols = [os.path.join(symbol_folder, f)
               for f in os.listdir(symbol_folder)
               if os.path.isfile(os.path.join(symbol_folder, f))]
    return symbols


def get_symbol(raw_data_id):
    current_folder = os.path.dirname(os.path.realpath(__file__))
    file_path = os.path.join(current_folder, "symbols/%i.txt" % raw_data_id)
    return file_path


def load_symbol_test():
    for symbol_file in get_all_symbols():
        with open(symbol_file) as f:
            data = f.read()
        HandwrittenData(data)


def width_test():
    with open(get_symbol(97705)) as f:
        data = f.read()
    assert HandwrittenData(data).get_width() == 186, \
        "Got %i" % HandwrittenData(data).get_width()

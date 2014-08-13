#!/usr/bin/env python

import sys
import os
sys.path.append("..")
from HandwrittenData import HandwrittenData
import preprocessing


# Test helper
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


def get_symbol_as_handwriting(raw_data_id):
    symbol_file = get_symbol(raw_data_id)
    with open(symbol_file) as f:
        data = f.read()
    a = HandwrittenData(data)
    return a


def get_all_symbols_as_handwriting():
    handwritings = []
    for symbol_file in get_all_symbols():
        with open(symbol_file) as f:
            data = f.read()
        handwritings.append(HandwrittenData(data))
    return handwritings


def compare_pointlists(a, b, epsilon=0.001):
    """Check if two line lists (a and b) are equal."""
    if len(a) != len(b):
        return False
    for line_a, line_b in zip(a, b):
        if len(line_a) != len(line_b):
            return False
        for point_a, point_b in zip(line_a, line_b):
            keys = ['x', 'y', 'time']
            for key in keys:
                if abs(point_a[key] - point_b[key]) > epsilon:
                    return False
    return True


# Tests
def scale_and_shift_test_all():
    preprocessing_queue = [preprocessing.Scale_and_shift()]
    for a in get_all_symbols_as_handwriting():
        a.preprocessing(preprocessing_queue)
        s = a.get_pointlist()
        assert len(s) > 0


def scale_and_shift_test_simple_1():
    preprocessing_queue = [preprocessing.Scale_and_shift()]
    s = '[[{"x":0, "y":0, "time": 0}]]'
    a = HandwrittenData(s)
    a.preprocessing(preprocessing_queue)
    s = a.get_pointlist()
    expectation = [[{"x": 0, "y": 0, "time": 0}]]
    assert s == expectation, "Got: %s; expected %s" % (s, expectation)


def scale_and_shift_test_simple_2():
    preprocessing_queue = [preprocessing.Scale_and_shift()]
    s = '[[{"x":10, "y":0, "time": 0}]]'
    a = HandwrittenData(s)
    a.preprocessing(preprocessing_queue)
    s = a.get_pointlist()
    expectation = [[{"x": 0, "y": 0, "time": 0}]]
    assert s == expectation, "Got: %s; expected %s" % (s, expectation)


def scale_and_shift_test_simple_3():
    preprocessing_queue = [preprocessing.Scale_and_shift()]
    s = '[[{"x":0, "y":10, "time": 0}]]'
    a = HandwrittenData(s)
    a.preprocessing(preprocessing_queue)
    s = a.get_pointlist()
    expectation = [[{"x": 0, "y": 0, "time": 0}]]
    assert s == expectation, "Got: %s; expected %s" % (s, expectation)


def scale_and_shift_test_simple_4():
    preprocessing_queue = [preprocessing.Scale_and_shift()]
    s = '[[{"x":0, "y":0, "time": 10}]]'
    a = HandwrittenData(s)
    a.preprocessing(preprocessing_queue)
    s = a.get_pointlist()
    expectation = [[{"x": 0, "y": 0, "time": 0}]]
    assert s == expectation, "Got: %s; expected %s" % (s, expectation)


def scale_and_shift_test_simple_5():
    preprocessing_queue = [preprocessing.Scale_and_shift()]
    s = '[[{"x":42, "y":12, "time": 10}]]'
    a = HandwrittenData(s)
    a.preprocessing(preprocessing_queue)
    s = a.get_pointlist()
    expectation = [[{"x": 0, "y": 0, "time": 0}]]
    assert s == expectation, "Got: %s; expected %s" % (s, expectation)


def scale_and_shift_test_a():
    preprocessing_queue = [preprocessing.Scale_and_shift()]
    s = ('[[{"x":232,"y":423,"time":1407885913983},'
         '{"x":267,"y":262,"time":1407885914315},'
         '{"x":325,"y":416,"time":1407885914650}],'
         '[{"x":252,"y":355,"time":1407885915675},'
         '{"x":305,"y":351,"time":1407885916361}]]')
    a = HandwrittenData(s)
    a.preprocessing(preprocessing_queue)
    s = a.get_pointlist()
    expectation = [[{u'y': 1.0, u'x': 0.0, u'time': 0},
                    {u'y': 0.0, u'x': 0.2174, u'time': 332},
                    {u'y': 0.9565, u'x': 0.5776, u'time': 667}],
                   [{u'y': 0.5776, u'x': 0.1242, u'time': 1692},
                    {u'y': 0.5528, u'x': 0.4534, u'time': 2378}]]
    assert compare_pointlists(s, expectation), \
        "Got: %s; expected %s" % (s, expectation)


def scale_and_shift_test_a_center():
    preprocessing_queue = [preprocessing.Scale_and_shift(center=True)]
    s = ('[[{"y": 1.0, "x": -0.3655913978494625, "time": 0}, '
         '{"y": 0.0, "x": -0.1482000935016364, "time": 332}, '
         '{"y": 0.9565, "x": 0.21204835370333253, "time": 667}], '
         '[{"y": 0.5776, "x": -0.24136779536499045, "time": 1692}, '
         '{"y": 0.5528, "x": 0.08782475121886046, "time": 2378}]]')
    a = HandwrittenData(s)
    a.preprocessing(preprocessing_queue)
    s = a.get_pointlist()
    expectation = [[{u'y': 1.0, u'x': -0.3655913978494624, u'time': 0},
                    {u'y': 0.0, u'x': -0.1482000935016363, u'time': 332},
                    {u'y': 0.9565, u'x': 0.21204835370333264, u'time': 667}],
                   [{u'y': 0.5776, u'x': -0.24136779536499034, u'time': 1692},
                    {u'y': 0.5528, u'x': 0.08782475121886058, u'time': 2378}]]
    assert compare_pointlists(s, expectation), \
        "Got: %s; expected %s" % (s, expectation)


def space_evenly_per_line_test_all():
    preprocessing_queue = [preprocessing.Space_evenly_per_line(number=100,
                                                               kind='cubic')]
    for a in get_all_symbols_as_handwriting():
        a.preprocessing(preprocessing_queue)
        s = a.get_pointlist()
        print(s)
        assert len(s) > 0

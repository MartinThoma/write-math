#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""Data multiplication algorithms.

Each algorithm works on the HandwrittenData class. They have to be applied like
this:

 >> import data_multiplication as multiply
 >> a = HandwrittenData(...)
 >> multiplication_queue = [multiply.copy(10),
                            mulitply.rotate(-30, 30, 5)
                            ]
 >> x = a.multiply(multiplication_queue)
"""

import inspect
import numpy
import logging
import sys
logging.basicConfig(format='%(asctime)s %(levelname)s %(message)s',
                    level=logging.DEBUG,
                    stream=sys.stdout)
import math
from copy import deepcopy
# mine
import HandwrittenData


def get_class(name):
    """Get function pointer by string."""
    clsmembers = inspect.getmembers(sys.modules[__name__], inspect.isclass)
    for string_name, act_class in clsmembers:
        if string_name == name:
            return act_class
    logging.debug("Unknown data multiplication class '%s'.", name)
    return None


def get_data_multiplication_queue(model_description_multiply):
    """Get features from a list of dictionaries

    >>> l = [{'Multiply': [{'nr': 1}]}, \
             {'Rotate': [{'minimum':-30}, {'maximum': 30}, {'step': 5}]}]
    >>> get_data_multiplication_queue(l)
    [Multiply (1 times), Rotate (-30.00, 30.00, 5.00)]
    """
    feature_list = []
    for feature in model_description_multiply:
        for feat, params in feature.items():
            feat = get_class(feat)
            if params is None:
                feature_list.append(feat())
            else:
                parameters = {}
                for dicts in params:
                    for param_name, param_value in dicts.items():
                        parameters[param_name] = param_value
                feature_list.append(feat(**parameters))
    return feature_list

# Only data multiplication classes follow
# Everyone must have a __str__, __repr__, __call__ and get_dimension function
# where
# * __call__ must take exactly one argument of type HandwrittenData
# * __call__ must return a list of HandwrittenData objects


# Local features


class Multiply(object):

    def __init__(self, nr=1):
        self.nr = nr

    def __repr__(self):
        return "Multiply (%i times)" % self.nr

    def __str__(self):
        return self.__repr__()

    def __call__(self, handwritten_data):
        assert isinstance(handwritten_data, HandwrittenData.HandwrittenData), \
            "handwritten data is not of type HandwrittenData, but of %r" % \
            type(handwritten_data)
        new_trainging_set = []
        for i in range(self.nr):
            new_trainging_set.append(handwritten_data)
        training_set = new_trainging_set
        return training_set


class Rotate(object):

    def __init__(self, minimum=-30.0, maximum=30.0, num=5.0):
        self.min = minimum
        self.max = maximum
        self.num = num

    def __repr__(self):
        return "Rotate (%0.2f, %0.2f, %0.2f)" % (self.min, self.max, self.step)

    def __str__(self):
        return self.__repr__()

    def __call__(self, handwritten_data):
        assert isinstance(handwritten_data, HandwrittenData.HandwrittenData), \
            "handwritten data is not of type HandwrittenData, but of %r" % \
            type(handwritten_data)
        new_trainging_set = []
        xc, yc = handwritten_data.get_center_of_mass()
        pointlist = handwritten_data.get_pointlist()
        for rotation in numpy.linspace(self.min, self.max, self.num):
            new_poinlist = []
            # Rotate pointlist around center of mass (xc, yc)
            for line in pointlist:
                new_line = []
                for point in line:
                    # Calculate rotation
                    # xnew, ynew = xc, yc
                    # (xnew, ynew) += (x-xc, y-yc)* (cos(rot.)  -sin(rot.))
                    #                               (sin(rot.)   cos(rot.))
                    x, y = point['x'], point['y']
                    cos = math.cos(math.radians(rotation))
                    sin = math.sin(math.radians(rotation))
                    xnew = cos*(x-xc) - sin*(y-yc) + xc
                    ynew = sin*(x-xc) + cos*(y-yc) + yc
                    new_line.append({'x': xnew,
                                     'y': ynew,
                                     'time': point['time']})
                new_poinlist.append(new_line)
            #create the new handwritten data object
            hwd_tmp = deepcopy(handwritten_data)
            hwd_tmp.set_pointlist(new_poinlist)
            new_trainging_set.append(hwd_tmp)
        training_set = new_trainging_set
        return training_set

if __name__ == '__main__':
    import doctest
    doctest.testmod()

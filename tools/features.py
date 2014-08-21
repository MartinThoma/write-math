#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""Feature extraction algorithms.

Each algorithm works on the HandwrittenData class. They have to be applied like
this:

 >> import features
 >> a = HandwrittenData(...)
 >> feature_list = [features.Stroke_Count(), \
                    features.Constant_Point_Coordinates(lines=4, \
                                                        points_per_line=20, \
                                                        fill_empty_with=0)\
                    ]
 >> x = a.feature_extraction(feature_list)
"""

import inspect
import urllib
import os
import Image
import logging
import sys
logging.basicConfig(format='%(asctime)s %(levelname)s %(message)s',
                    level=logging.DEBUG,
                    stream=sys.stdout)
# mine
import HandwrittenData
import preprocessing


def get_class(name):
    """Get function pointer by string."""
    clsmembers = inspect.getmembers(sys.modules[__name__], inspect.isclass)
    for string_name, act_class in clsmembers:
        if string_name == name:
            return act_class
    logging.debug("Unknown class '%s'.", name)
    return None


def get_features(model_description_features):
    """Get features from a list of dictionaries

    >>> l = [{'Stroke_Count': None}, \
             {'Constant_Point_Coordinates': \
              [{'lines': 4}, \
               {'points_per_line': 81}, \
               {'fill_empty_with': 0}, \
               {'pen_down': False}] \
             } \
            ]
    >>> get_features(l)
    [Stroke_Count, Constant_Point_Coordinates
     - lines: 4
     - points per line: 81
     - fill empty with: 0
     - pen down feature: False
    ]
    """
    feature_list = []
    for feature in model_description_features:
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

# Only feature calculation classes follow
# Everyone must have a __str__, __repr__, __call__ and get_dimension function
# where
# * __call__ must take exactly one argument of type HandwrittenData
# * __call__ must return a list of length get_dimension()
# * get_dimension must return a positive number


# Local features


class Constant_Point_Coordinates(object):
    def __init__(self, lines=4, points_per_line=20, fill_empty_with=0,
                 pen_down=True):
        self.lines = lines
        self.points_per_line = points_per_line
        self.fill_empty_with = fill_empty_with
        self.pen_down = pen_down

    def __repr__(self):
        return ("Constant_Point_Coordinates\n"
                " - lines: %i\n"
                " - points per line: %i\n"
                " - fill empty with: %i\n"
                " - pen down feature: %r\n") % \
               (self.lines, self.points_per_line, self.fill_empty_with,
                self.pen_down)

    def __str__(self):
        return ("constant point coordinates\n"
                " - lines: %i\n"
                " - points per line: %i\n"
                " - fill empty with: %i\n"
                " - pen down feature: %r\n") % \
               (self.lines, self.points_per_line, self.fill_empty_with,
                self.pen_down)

    def get_dimension(self):
        if self.lines > 0:
            return 2*self.lines * self.points_per_line
        else:
            if self.pen_down:
                return 3*self.points_per_line
            else:
                return 2*self.points_per_line

    def __call__(self, handwritten_data):
        assert isinstance(handwritten_data, HandwrittenData.HandwrittenData), \
            "handwritten data is not of type HandwrittenData, but of %r" % \
            type(handwritten_data)
        x = []
        pointlist = handwritten_data.get_pointlist()
        if self.lines > 0:
            for line_nr in range(self.lines):
                # make sure that the current symbol actually has that many
                # lines
                if line_nr < len(pointlist):
                    for point_nr in range(self.points_per_line):
                        if point_nr < len(pointlist[line_nr]):
                            x.append(pointlist[line_nr][point_nr]['x'])
                            x.append(pointlist[line_nr][point_nr]['y'])
                        else:
                            x.append(self.fill_empty_with)
                            x.append(self.fill_empty_with)
                else:
                    for i in range(self.points_per_line):
                        x.append(self.fill_empty_with)
                        x.append(self.fill_empty_with)
        else:
            for point in handwritten_data.get_pointlist()[0]:
                if len(x) >= 3*self.points_per_line or \
                   (len(x) >= 2*self.points_per_line and not self.pen_down):
                    break
                x.append(point['x'])
                x.append(point['y'])
                if self.pen_down:
                    x.append(int(point['pen_down']))
            if self.pen_down:
                while len(x) != 3*self.points_per_line:
                    x.append(self.fill_empty_with)
            else:
                while len(x) != 2*self.points_per_line:
                    x.append(self.fill_empty_with)
        assert self.get_dimension() == len(x), \
            "Dimension of %s should be %i, but was %i" % \
            (self.__str__(), self.get_dimension(), len(x))
        return x


class First_N_Points(object):
    def __init__(self, n=81):
        self.n = n

    def __repr__(self):
        return ("First_N_Points\n"
                " - n: %i\n") % \
               (self.n)

    def __str__(self):
        return ("first n points\n"
                " - n: %i\n") % \
               (self.n)

    def get_dimension(self):
        return 2*self.n

    def __call__(self, handwritten_data):
        assert isinstance(handwritten_data, HandwrittenData.HandwrittenData), \
            "handwritten data is not of type HandwrittenData, but of %r" % \
            type(handwritten_data)
        x = []
        pointlist = handwritten_data.get_pointlist()
        left = self.n
        for line in pointlist:
            for point in line:
                if left == 0:
                    break
                else:
                    left -= 1
                    x.append(point['x'])
                    x.append(point['y'])
        assert self.get_dimension() == len(x), \
            "Dimension of %s should be %i, but was %i" % \
            (self.__str__(), self.get_dimension(), len(x))
        return x


# Global features

class Stroke_Count(object):
    def __repr__(self):
        return "Stroke_Count"

    def __str__(self):
        return "stroke count"

    def get_dimension(self):
        return 1

    def __call__(self, handwritten_data):
        assert isinstance(handwritten_data, HandwrittenData.HandwrittenData), \
            "handwritten data is not of type HandwrittenData, but of %r" % \
            type(handwritten_data)
        return [len(handwritten_data.get_pointlist())]


class Bitmap(object):
    def __init__(self, n=28):
        self.n = n  # Size of the bitmap (n x n)

    def __repr__(self):
        return ("Bitmap (n=%i)\n") % (self.n)

    def __str__(self):
        return self.__repr__()

    def get_dimension(self):
        return self.n**2

    def __call__(self, handwritten_data):
        assert isinstance(handwritten_data, HandwrittenData.HandwrittenData), \
            "handwritten data is not of type HandwrittenData, but of %r" % \
            type(handwritten_data)
        x = []
        url = "http://localhost/write-math/website/raw-data/"
        raw_data_id = handwritten_data.raw_data_id
        foldername = "/tmp/write-math/"
        f = urllib.urlopen("{url}{id}.svg".format(url=url, id=raw_data_id))
        with open("%s%i.svg" % (foldername, raw_data_id), "wb") as imgFile:
            imgFile.write(f.read())

        command = ("convert -size 28x28 {folder}{id}.svg  -resize {n}x{n} "
                   "-gravity center -extent {n}x{n} "
                   "-monochrome {folder}{id}.png").format(id=raw_data_id,
                                                          n=self.n,
                                                          url=url,
                                                          folder=foldername)
        os.system(command)
        im = Image.open("%s%i.png" % (foldername, raw_data_id))
        pix = im.load()
        # pixel_image = [[0 for i in range(28)] for j in range(28)]
        for i in range(28):
            for j in range(28):
                # pixel_image[i][j] = pix[i, j]
                x.append(pix[i, j])
        assert self.get_dimension() == len(x), \
            "Dimension of %s should be %i, but was %i" % \
            (self.__str__(), self.get_dimension(), len(x))
        return x


class Ink(object):
    def __repr__(self):
        return "Ink"

    def __str__(self):
        return "ink"

    def get_dimension(self):
        return 1

    def __call__(self, handwritten_data):
        assert isinstance(handwritten_data, HandwrittenData.HandwrittenData), \
            "handwritten data is not of type HandwrittenData, but of %r" % \
            type(handwritten_data)
        ink = 0.
        # calculate ink used for this symbol
        # TODO: What about dots? What about speed?
        for line in handwritten_data.get_pointlist():
            last_point = None
            for point in line:
                if last_point is not None:
                    ink += preprocessing._euclidean_distance(last_point, point)
                last_point = point
        return [ink]


class AspectRatio(object):
    def __repr__(self):
        return "Aspect Ratio"

    def __str__(self):
        return "Aspect Ratio"

    def get_dimension(self):
        return 1

    def __call__(self, handwritten_data):
        assert isinstance(handwritten_data, HandwrittenData.HandwrittenData), \
            "handwritten data is not of type HandwrittenData, but of %r" % \
            type(handwritten_data)
        width = float(handwritten_data.get_width()+1)
        height = float(handwritten_data.get_height()+1)
        return [width/height]


class Width(object):
    def __repr__(self):
        return "Width"

    def __str__(self):
        return "Width"

    def get_dimension(self):
        return 1

    def __call__(self, handwritten_data):
        assert isinstance(handwritten_data, HandwrittenData.HandwrittenData), \
            "handwritten data is not of type HandwrittenData, but of %r" % \
            type(handwritten_data)
        return [float(handwritten_data.get_width())]


class Height(object):
    def __repr__(self):
        return "Height"

    def __str__(self):
        return "Height"

    def get_dimension(self):
        return 1

    def __call__(self, handwritten_data):
        assert isinstance(handwritten_data, HandwrittenData.HandwrittenData), \
            "handwritten data is not of type HandwrittenData, but of %r" % \
            type(handwritten_data)
        return [float(handwritten_data.get_height())]


class Time(object):
    def __repr__(self):
        return "Time"

    def __str__(self):
        return "Time"

    def get_dimension(self):
        return 1

    def __call__(self, handwritten_data):
        assert isinstance(handwritten_data, HandwrittenData.HandwrittenData), \
            "handwritten data is not of type HandwrittenData, but of %r" % \
            type(handwritten_data)
        return [float(handwritten_data.get_time())]


if __name__ == '__main__':
    import doctest
    doctest.testmod()

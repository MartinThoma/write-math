#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""Feature extraction algorithms.

Each algorithm works on the HandwrittenData class. They have to be applied like
this:

>>> import features
>>> a = HandwrittenData(...)
>>> feature_list = [features.Stroke_Count(),
                    features.Constant_Point_Coordinates(lines=4,
                                                        points_per_line=20,
                                                        fill_empty_with=0)
                    ]
>>> x = a.feature_extraction(feature_list)
"""

import HandwrittenData
import preprocessing
import urllib
import os
import Image


def get_class(name):
    if name == "Stroke_Count":
        return Stroke_Count
    elif name == "Constant_Point_Coordinates":
        return Constant_Point_Coordinates
    elif name == "First_N_Points":
        return First_N_Points
    elif name == "Bitmap":
        return Bitmap
    elif name == "Ink":
        return Ink
    else:
        return None


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


class Constant_Point_Coordinates(object):
    def __init__(self, lines=4, points_per_line=20, fill_empty_with=0):
        self.lines = lines
        self.points_per_line = points_per_line
        self.fill_empty_with = fill_empty_with

    def __repr__(self):
        return ("Constant_Point_Coordinates\n"
                " - lines: %i\n"
                " - points per line: %i\n"
                " - fill empty with: %i\n") % \
               (self.lines, self.points_per_line, self.fill_empty_with)

    def __str__(self):
        return ("constant point coordinates\n"
                " - lines: %i\n"
                " - points per line: %i\n"
                " - fill empty with: %i\n") % \
               (self.lines, self.points_per_line, self.fill_empty_with)

    def get_dimension(self):
        if self.lines > 0:
            return 2*self.lines * self.points_per_line
        else:
            return 3*self.points_per_line

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
                if len(x) >= 3*self.points_per_line:
                    break
                x.append(point['x'])
                x.append(point['y'])
                x.append(int(point['pen_down']))
            while len(x) != 3*self.points_per_line:
                x.append(self.fill_empty_with)
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
        return x


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
        ink = 0
        # calculate ink used for this symbol
        # TODO: What about dots? What about speed?
        for line in handwritten_data.get_pointlist():
            last_point = None
            for point in line:
                if last_point is not None:
                    preprocessing._euclidean_distance(last_point, point)
                last_point = point
        return [ink]

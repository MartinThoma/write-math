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
import json


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
        if len(pointlist[0]) < 5:
            return x  # TODO: Improve!
        if self.lines > 0:
            for line_nr in range(self.lines):
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
            # TODO
            preprocessing.space_evenly(handwritten_data,
                                       number=self.points_per_line)
            for point in handwritten_data.get_pointlist()[0]:
                x.append(point['x'])
                x.append(point['y'])
                try:
                    x.append(point['pen_down'])
                except:
                    with open("nopendown.txt", "a") as f:
                        f.write("%i\n" % handwritten_data.raw_data_id)
        return x

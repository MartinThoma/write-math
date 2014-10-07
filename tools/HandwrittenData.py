#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""Representation of a recording (handwritten data)."""

import logging
import json
import matplotlib.pyplot as plt
# mine
import preprocessing


class HandwrittenData(object):
    """Represents a handwritten symbol."""
    def __init__(self, raw_data_json, formula_id=None, raw_data_id=None,
                 formula_in_latex=None, wild_point_count=0,
                 missing_line=0, user_id=0):
        self.raw_data_json = raw_data_json
        self.formula_id = formula_id
        self.raw_data_id = raw_data_id
        self.formula_in_latex = formula_in_latex
        self.wild_point_count = wild_point_count
        self.missing_line = missing_line
        self.user_id = user_id
        assert type(json.loads(self.raw_data_json)) is list, \
            "raw_data_json is not JSON: %r" % self.raw_data_json
        assert len(self.get_pointlist()) >= 1, \
            "The pointlist of formula_id %i is %s" % (self.formula_id,
                                                      self.get_pointlist())
        assert wild_point_count >= 0
        assert missing_line >= 0

    def get_pointlist(self):
        """Get a list of lists of tuples from JSON raw data string.
           Those lists represent lines with control points.

           Every point is a dictionary:
           {'x': 123, 'y': 42, 'time': 1337}
        """
        try:
            pointlist = json.loads(self.raw_data_json)
        except Exception as inst:
            logging.debug("pointLineList: linelistP")
            logging.debug(self.raw_data_json)
            logging.debug("didn't work")
            raise inst

        if len(pointlist) == 0:
            logging.warning("Pointlist was empty. Search for '" +
                            self.raw_data_json + "' in `wm_raw_draw_data`.")
        return pointlist

    def get_sorted_pointlist(self):
        """Make sure that the points and lines are in order."""
        pointlist = self.get_pointlist()
        for i in range(len(pointlist)):
            pointlist[i] = sorted(pointlist[i], key=lambda p: p['time'])
        pointlist = sorted(pointlist, key=lambda line: line[0]['time'])
        return pointlist

    def set_pointlist(self, pointlist):
        """Overwrite pointlist.
        @param pointlist - a list of lists. The inner lists represent strokes.
                           Every stroke consists of points.
                           Every point is a dictinary with 'x', 'y', 'time'.
        """
        assert type(pointlist) is list, \
            "pointlist is not of type list, but %r" % type(pointlist)
        assert len(pointlist) >= 1, \
            "The pointlist of formula_id %i is %s" % (self.formula_id,
                                                      self.get_pointlist())
        self.raw_data_json = json.dumps(pointlist)

    def get_bounding_box(self):
        """ Get the bounding box of a pointlist. """
        pointlist = self.get_pointlist()

        # Initialize bounding box parameters to save values
        minx, maxx = pointlist[0][0]["x"], pointlist[0][0]["x"]
        miny, maxy = pointlist[0][0]["y"], pointlist[0][0]["y"]
        mint, maxt = pointlist[0][0]["time"], pointlist[0][0]["time"]

        # Adjust parameters
        for line in pointlist:
            for p in line:
                minx, maxx = min(minx, p["x"]), max(maxx, p["x"])
                miny, maxy = min(miny, p["y"]), max(maxy, p["y"])
                mint, maxt = min(mint, p["time"]), max(maxt, p["time"])
        return {"minx": minx, "maxx": maxx, "miny": miny, "maxy": maxy,
                "mint": mint, "maxt": maxt}

    def get_width(self):
        """Get the width of the rectangular, axis-parallel bounding box."""
        box = self.get_bounding_box()
        return box['maxx'] - box['minx']

    def get_height(self):
        """Get the height of the rectangular, axis-parallel bounding box."""
        box = self.get_bounding_box()
        return box['maxy'] - box['miny']

    def get_area(self):
        """Get the area in square pixels of the recording."""
        return (self.get_height()+1) * (self.get_width()+1)

    def get_time(self):
        """Get the time in which the recording was created."""
        box = self.get_bounding_box()
        return box['maxt'] - box['mint']

    def preprocessing(self, algorithms):
        """Apply preprocessing algorithms.

        >>> a = HandwrittenData(...)
        >>> preprocessing_queue = [(preprocessing.scale_and_shift, []), \
                                   (preprocessing.connect_lines, []), \
                                   (preprocessing.douglas_peucker, \
                                    {'EPSILON': 0.2}), \
                                   (preprocessing.space_evenly, \
                                    {'number': 100, \
                                     'KIND': 'cubic'})]
        >>> a.preprocessing(preprocessing_queue)
        """
        assert type(algorithms) is list
        for algorithm in algorithms:
            algorithm(self)

    def feature_extraction(self, algorithms):
        """Get a list of features.

        Every algorithm has to return the features as a list."""
        assert type(algorithms) is list
        features = []
        for algorithm in algorithms:
            new_features = algorithm(self)
            assert len(new_features) == algorithm.get_dimension(), \
                "Expected %i features from algorithm %s, got %i features" % \
                (algorithm.get_dimension(), str(algorithm), len(new_features))
            features += new_features
        return features

    def show(self):
        """Show the data graphically in a new pop-up window."""
        pointlist = self.get_pointlist()
        if 'pen_down' in pointlist[0][0]:
            assert len(pointlist) > 1, \
                "Lenght of pointlist was %i. Got: %s" % (len(pointlist),
                                                         pointlist)
            new_pointlist = []
            last = None
            stroke = []
            for point in pointlist[0]:
                if last is None:
                    last = point['pen_down']
                if point['pen_down'] != last:
                    new_pointlist.append(stroke)
                    last = point['pen_down']
                    stroke = []
                else:
                    stroke.append(point)
            new_pointlist.append(stroke)
            pointlist = new_pointlist

        _, ax = plt.subplots()
        ax.set_title("Raw data id: %s, "
                     "Formula_id: %s" % (str(self.raw_data_id),
                                         str(self.formula_id)))

        for line in pointlist:
            xs, ys = [], []
            for p in line:
                xs.append(p['x'])
                ys.append(p['y'])
            if "pen_down" in line[0] and line[0]["pen_down"] is False:
                plt.plot(xs, ys, '-x')
            else:
                plt.plot(xs, ys, '-o')
        plt.gca().invert_yaxis()
        ax.set_aspect('equal')
        plt.show()

    def count_single_dots(self):
        """Count all strokes of this recording that have only a single dot.
        """
        pointlist = self.get_pointlist()
        single_dots = 0
        for line in pointlist:
            if len(line) == 1:
                single_dots += 1
        return single_dots

    def get_center_of_mass(self):
        """Get a tuple (x,y) that is the center of mass. The center of mass
           is not necessarily the same as the center of the bounding box.
           Imagine a black square and a single dot wide outside of the square.
        """
        xsum, ysum, counter = 0., 0., 0
        for line in self.get_pointlist():
            for point in line:
                xsum += point['x']
                ysum += point['y']
                counter += 1
        return (xsum/counter, ysum/counter)

    def __eq__(self, other):
        if isinstance(other, self.__class__):
            return self.__dict__ == other.__dict__
        else:
            return False

    def __ne__(self, other):
        return not self.__eq__(other)

    def __repr__(self):
        return "HandwrittenData(raw_data_id=%s)" % str(self.raw_data_id)

    def __str__(self):
        return self.__repr__()

if __name__ == '__main__':
    pass
    #EXAMPLE.show()

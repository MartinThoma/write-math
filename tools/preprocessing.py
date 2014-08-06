#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
Preprocessing algorithms.

Each algorithm works on the HandwrittenData class. They have to be applied like
this:

>>> a = HandwrittenData(...)
>>> preprocessing_queue = [(preprocessing.scale_and_shift, []), \
                           (preprocessing.connect_lines, []), \
                           (preprocessing.douglas_peucker, \
                            {'EPSILON': 0.2}), \
                           (preprocessing.space_evenly, {'number': 100})]
>>> a.preprocessing(preprocessing_queue)
"""

import HandwrittenData
import numpy
from scipy.interpolate import interp1d
from math import sqrt


def _euclidean_distance(p1, p2):
    return sqrt((p1["x"]-p2["x"])**2 + (p1["y"]-p2["y"])**2)


def _flatten(two_dimensional_list):
    return [i for inner_list in two_dimensional_list for i in inner_list]


def get_algorithm(algorithm_name):
    if algorithm_name == 'scale_and_shift':
        return scale_and_shift
    elif algorithm_name == 'space_evenly':
        return space_evenly
    elif algorithm_name == 'douglas_peucker':
        return douglas_peucker
    elif algorithm_name == 'connect_lines':
        return connect_lines
    elif algorithm_name == 'dot_reduction':
        return dot_reduction
    elif algorithm_name == 'remove_wild_points':
        return remove_wild_points
    else:
        return None


def scale_and_shift(handwritten_data, center=False):
    """ Take a list of points and scale and move it so that it's in the
        unit square. Keep the aspect ratio. Optionally center the points
        inside of the unit square.
    """
    assert isinstance(handwritten_data, HandwrittenData.HandwrittenData), \
        "handwritten data is not of type HandwrittenData, but of %r" % \
        type(handwritten_data)

    def get_scale_and_shift_parameters(handwritten_data, center=False):
        """ Take a list of points and calculate the factors for scaling and
            moving it so that it's in the unit square. Keept the aspect ratio.
            Optionally center the points inside of the unit square.
        """
        a = handwritten_data.get_bounding_box()

        width = a['maxx'] - a['minx']
        height = a['maxy'] - a['miny']

        factorX, factorY = 1, 1
        if width != 0:
            factorX = 1./width

        if height != 0:
            factorY = 1./height

        factor = min(factorX, factorY)
        addx, addy = 0, 0

        if center:
            add = (1 - (max(factorX, factorY) / factor)) / 2

            if factor == factorX:
                addy = add
            else:
                addx = add

        return {"factor": factor, "addx": addx, "addy": addy,
                "minx": a['minx'], "miny": a['miny'], "mint": a['mint']}

    tmp = get_scale_and_shift_parameters(handwritten_data, center)
    factor, addx, addy = tmp['factor'], tmp['addx'], tmp['addy']
    minx, miny, mint = tmp['minx'], tmp['miny'], tmp['mint']

    pointlist = handwritten_data.get_pointlist()
    for linenr, line in enumerate(pointlist):
        for key, p in enumerate(line):
            pointlist[linenr][key] = {"x": (p["x"] - minx) * factor + addx,
                                      "y": (p["y"] - miny) * factor + addy,
                                      "time": p["time"] - mint}
            if "pen_down" in p:
                pointlist[linenr][key]["pen_down"] = p["pen_down"]
    handwritten_data.set_pointlist(pointlist)


def space_evenly(handwritten_data, number=100, kind='cubic'):
    """Space the points evenly. """

    # Make sure that the lists are sorted
    pointlist = handwritten_data.get_sorted_pointlist()

    for i in range(len(pointlist)-1):
        # The last point of the previous line should be lower than the first
        # point of the next line
        assert (pointlist[i][-1]["time"] <= pointlist[i+1][0]["time"]), \
            ("Something is wrong with the time. The last point of line %i "
             "has a time of %0.2f, but the first point of line %i has a "
             "time of %0.2f. See raw_data_id %s") % \
            (i,
             pointlist[i][-1]["time"],
             i+1,
             pointlist[i+1][0]["time"],
             str(handwritten_data.raw_data_id))

    # calculate "pen_down" strokes
    times = []
    for i, line in enumerate(pointlist):
        line_info = {"start": line[0]['time'],
                     "end": line[-1]['time'],
                     "pen_down": True}
        # set up variables for interpolation
        x, y, t = [], [], []
        for point in line:
            if point['time'] not in t:
                x.append(point['x'])
                y.append(point['y'])
                t.append(point['time'])
        x, y = numpy.array(x), numpy.array(y)
        if len(t) == 1:
            # constant interpolation
            fx, fy = lambda x: float(x), lambda y: float(y)
        elif len(t) == 2:
            # linear interpolation
            fx, fy = interp1d(t, x, 'linear'), interp1d(t, y, 'linear')
        elif len(t) == 3:
            # quadratic interpolation
            fx, fy = interp1d(t, x, 'quadratic'), interp1d(t, y, 'quadratic')
        else:
            fx, fy = interp1d(t, x, kind), interp1d(t, y, kind)
        line_info['fx'] = fx
        line_info['fy'] = fy
        times.append(line_info)

    # Model "pen_up" strokes
    for i in range(len(pointlist) - 1):
        line_info = {"start": pointlist[i][-1],
                     "end": pointlist[i+1][0],
                     "pen_down": False}
        x, y, t = [], [], []
        for point in [pointlist[i][-1], pointlist[i+1][0]]:
            if point['time'] not in t:
                x.append(point['x'])
                y.append(point['y'])
                t.append(point['time'])
            else:
                # TODO: That should not happen
                pass
        if len(x) == 1:
            # constant interpolation
            fx, fy = lambda x: float(x), lambda y: float(y)
        else:
            # linear interpolation
            x, y = numpy.array(x), numpy.array(y)
            fx, fy = interp1d(t, x, kind='linear'), interp1d(t, y, kind='linear')
        line_info['fx'] = fx
        line_info['fy'] = fy
        times.append(line_info)

    new_pointlist = []

    tnew = numpy.linspace(pointlist[0][0]['time'],
                          pointlist[-1][-1]['time'],
                          number)

    for time in tnew:
        for line_intervall in times:
            if line_intervall["start"] <= time <= line_intervall["end"]:
                x = float(line_intervall['fx'](time))
                y = float(line_intervall['fy'](time))
                time = float(time)
                new_pointlist.append({'x': x, 'y': y, 'time': time,
                                      'pen_down': line_intervall['pen_down']})
    handwritten_data.set_pointlist([new_pointlist])


def douglas_peucker(handwritten_data, EPSILON=10):
    """
     Apply the Douglas-Peucker algorithm to each line of $pointlist seperately.
     @param  array $pointlist see pointList()
     @return pointlist
    """

    pointlist = handwritten_data.get_pointlist()

    def DouglasPeucker(PointList, EPSILON):
        def LotrechterAbstand(p3, p1, p2):
            """
             * Calculate the distance from p3 to the line defined by p1 and p2.
             * @param list p1 associative array with "x" and "y" start of line
             * @param list p2 associative array with "x" and "y" end of line
             * @param list p3 associative array with "x" and "y" point
            """
            x3 = p3['x']
            y3 = p3['y']

            px = p2['x']-p1['x']
            py = p2['y']-p1['y']

            something = px*px + py*py
            if (something == 0):
                # TODO: really?
                return 0

            u = ((x3 - p1['x']) * px + (y3 - p1['y']) * py) / something

            if u > 1:
                u = 1
            elif u < 0:
                u = 0

            x = p1['x'] + u * px
            y = p1['y'] + u * py

            dx = x - x3
            dy = y - y3

            # Note: If the actual distance does not matter,
            # if you only want to compare what this function
            # returns to other results of this function, you
            # can just return the squared distance instead
            # (i.e. remove the sqrt) to gain a little performance

            dist = sqrt(dx*dx + dy*dy)
            return dist

        # Finde den Punkt mit dem größten Abstand
        dmax = 0
        index = 0
        for i in range(1, len(PointList)):
            d = LotrechterAbstand(PointList[i], PointList[0], PointList[-1])
            if d > dmax:
                index = i
                dmax = d

        # Wenn die maximale Entfernung größer als EPSILON ist, dann rekursiv
        # vereinfachen
        if dmax >= EPSILON:
                # Recursive call
                recResults1 = DouglasPeucker(PointList[0:index], EPSILON)
                recResults2 = DouglasPeucker(PointList[index:], EPSILON)

                # Ergebnisliste aufbauen
                ResultList = recResults1[:-1] + recResults2
        else:
                ResultList = [PointList[0], PointList[-1]]

        # Ergebnis zurückgeben
        return ResultList

    for i in range(0, len(pointlist)):
        pointlist[i] = DouglasPeucker(pointlist[i], EPSILON)
    handwritten_data.set_pointlist(pointlist)


def connect_lines(handwritten_data, minimum_distance=0.05):
    """Detect if lines were probably accidentially disconnected. If that is the
       case, connect them.
    """
    assert isinstance(handwritten_data, HandwrittenData.HandwrittenData), \
        "handwritten data is not of type HandwrittenData, but of %r" % \
        type(handwritten_data)

    pointlist = handwritten_data.get_pointlist()

    # Connecting lines makes only sense when there are multiple lines
    if len(pointlist) > 1:
        lines = []
        last_appended = False
        i = 0
        while i < len(pointlist)-1:
            last_point = pointlist[i][-1]
            first_point = pointlist[i+1][0]
            if _euclidean_distance(last_point, first_point) < minimum_distance:
                lines.append(pointlist[i]+pointlist[i+1])
                pointlist[i+1] = lines[-1]
                if i == len(pointlist)-2:
                    last_appended = True
                i += 1
            else:
                lines.append(pointlist[i])
            i += 1
        if not last_appended:
            lines.append(pointlist[-1])
        handwritten_data.set_pointlist(lines)


def dot_reduction(handwritten_data, threshold):
    """Reduce lines where the maximum distance between points is below a
       threshold to a single dot.
    """

    def get_max_distance(L):
        """Find the maximum distance between two points in a list of points
        @param  list L list of points
        @return float  maximum distance bewtween two points
        """
        if len(L) <= 1:
            return -1
        else:
            max_dist = _euclidean_distance(L[0], L[1])
            for i in range(len(L)-1):
                for j in range(i+1, len(L)):
                    max_dist = max(_euclidean_distance(L[i], L[j]), max_dist)
            return max_dist

    def get_average_point(L):
        """Calculate the average point.
        @param  list L List of points
        @return dict   a single point
        """
        x, y, t = 0, 0, 0
        for point in L:
            x += point['x']
            y += point['y']
            t += point['time']
        x = float(x) / len(L)
        y = float(y) / len(L)
        t = float(t) / len(L)
        return {'x': x, 'y': y, 'time': t}

    new_pointlist = []
    pointlist = handwritten_data.get_pointlist()
    for line in pointlist:
        new_line = line
        if len(line) > 1 and get_max_distance(line) < threshold:
            new_line = [get_average_point(line)]
        new_pointlist.append(new_line)

    handwritten_data.set_pointlist(new_pointlist)


def remove_wild_points(handwritten_data):
    """Find wild points and remove them."""
    # Bounding box criterion:
    # If the distance from point to all others strokes bounding boxes is
    # more than 1/5 of the whole size, it is a wild point
    pass

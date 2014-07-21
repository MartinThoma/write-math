#!/usr/bin/env python
# -*- coding: utf-8 -*-

import HandwrittenData
import numpy
from scipy.interpolate import interp1d
from math import sqrt


def _flatten(two_dimensional_list):
    return [i for inner_list in two_dimensional_list for i in inner_list]


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
    handwritten_data.set_pointlist(pointlist)


def space_evenly(handwritten_data, number=100, KIND='linear'):
    """Space the points evenly. """

    pointlist = handwritten_data.get_pointlist()
    new_pointlist = []

    for line in pointlist:
        new_line = []
        if len(line) < 4:
            new_line = line
        else:
            line = sorted(line, key=lambda p: p['time'])

            x, y, t = [], [], []

            for point in line:
                if point['time'] not in t:
                    x.append(point['x'])
                    y.append(point['y'])
                    t.append(point['time'])

            x, y = numpy.array(x), numpy.array(y)
            fx, fy = interp1d(t, x, kind=KIND), interp1d(t, y, kind=KIND)
            tnew = numpy.linspace(t[0], t[-1], number)

            for x, y in zip(fx(tnew), fy(tnew)):
                new_line.append({'x': x, 'y': y})
        new_pointlist.append(new_line)
    handwritten_data.set_pointlist(new_pointlist)


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

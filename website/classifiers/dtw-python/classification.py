#!/usr/bin/env python
# -*- coding: utf-8 -*-

import json
from math import sqrt, exp

CLASSIFIER_NAME = "dtw-python"

import logging
logging.basicConfig(filename='classificationpy.log',
                    level=logging.DEBUG,
                    format='%(asctime)s %(levelname)s: %(message)s')


def space_evenly(pointlist, number=100, KIND='linear'):
    """Space the points evenly.

    >>> space_evenly([{u'y': 397, u'x': 244, u'time': 69}, {u'y': 394, u'x': 245, u'time': 77}, {u'y': 389, u'x': 246, u'time': 84}, {u'y': 383, u'x': 246, u'time': 92}, {u'y': 378, u'x': 248, u'time': 100}, {u'y': 368, u'x': 250, u'time': 108}, {u'y': 359, u'x': 251, u'time': 116}, {u'y': 349, u'x': 253, u'time': 124}, {u'y': 337, u'x': 256, u'time': 132}, {u'y': 325, u'x': 256, u'time': 141}, {u'y': 313, u'x': 258, u'time': 149}, {u'y': 303, u'x': 260, u'time': 157}, {u'y': 292, u'x': 262, u'time': 164}, {u'y': 282, u'x': 263, u'time': 172}, {u'y': 271, u'x': 265, u'time': 181}, {u'y': 263, u'x': 267, u'time': 189}, {u'y': 254, u'x': 269, u'time': 197}, {u'y': 248, u'x': 271, u'time': 204}, {u'y': 241, u'x': 271, u'time': 212}, {u'y': 237, u'x': 273, u'time': 220}, {u'y': 233, u'x': 274, u'time': 228}, {u'y': 232, u'x': 275, u'time': 236}, {u'y': 231, u'x': 275, u'time': 244}, {u'y': 230, u'x': 276, u'time': 252}, {u'y': 229, u'x': 276, u'time': 269}, {u'y': 231, u'x': 277, u'time': 405}, {u'y': 234, u'x': 278, u'time': 414}, {u'y': 236, u'x': 279, u'time': 420}, {u'y': 240, u'x': 281, u'time': 428}, {u'y': 245, u'x': 283, u'time': 436}, {u'y': 251, u'x': 285, u'time': 444}, {u'y': 258, u'x': 287, u'time': 452}, {u'y': 266, u'x': 292, u'time': 460}, {u'y': 275, u'x': 296, u'time': 468}, {u'y': 285, u'x': 300, u'time': 476}, {u'y': 295, u'x': 305, u'time': 484}, {u'y': 305, u'x': 307, u'time': 492}, {u'y': 313, u'x': 309, u'time': 500}, {u'y': 321, u'x': 311, u'time': 509}, {u'y': 329, u'x': 313, u'time': 517}, {u'y': 337, u'x': 315, u'time': 524}, {u'y': 345, u'x': 317, u'time': 532}, {u'y': 351, u'x': 317, u'time': 540}, {u'y': 357, u'x': 319, u'time': 548}, {u'y': 363, u'x': 321, u'time': 556}, {u'y': 370, u'x': 323, u'time': 564}, {u'y': 374, u'x': 323, u'time': 572}, {u'y': 377, u'x': 324, u'time': 580}, {u'y': 379, u'x': 324, u'time': 588}, {u'y': 380, u'x': 324, u'time': 596}, {u'y': 382, u'x': 325, u'time': 604}, {u'y': 384, u'x': 325, u'time': 612}, {u'y': 385, u'x': 325, u'time': 620}, {u'y': 387, u'x': 326, u'time': 629}, {u'y': 388, u'x': 326, u'time': 637}, {u'y': 389, u'x': 326, u'time': 645}, {u'y': 390, u'x': 326, u'time': 652}], 5)
    """
    import numpy
    from scipy.interpolate import interp1d
    if len(pointlist) < 4:
        return pointlist
    pointlist = sorted(pointlist, key=lambda p: p['time'])
    x = []
    y = []
    t = []
    for point in pointlist:
        if point['time'] not in t:
            x.append(point['x'])
            y.append(point['y'])
            t.append(point['time'])
    x = numpy.array(x)
    y = numpy.array(y)
    fx = interp1d(t, x, kind=KIND)
    fy = interp1d(t, y, kind=KIND)
    tnew = numpy.linspace(t[0], t[-1], number)
    pointlist = []

    for x, y in zip(fx(tnew), fy(tnew)):
        pointlist.append({'x': x, 'y': y})
    return pointlist


def get_bounding_box(pointlist):
    """ Get the bounding box of a pointlist.

    >>> get_bounding_box([{'x': 0, 'y': 0}, {'x': 1, 'y': 1}])
    {'minx': 0, 'miny': 0, 'maxx': 1, 'maxy': 1}
    >>> get_bounding_box([{'x': 12, 'y': 10}, {'x': 1, 'y': 1}])
    {'minx': 1, 'miny': 1, 'maxx': 12, 'maxy': 10}
    """
    minx = pointlist[0]["x"]
    maxx = pointlist[0]["x"]
    miny = pointlist[0]["y"]
    maxy = pointlist[0]["y"]
    for p in pointlist:
        if p["x"] < minx:
            minx = p["x"]
        elif p["x"] > maxx:
            maxx = p["x"]
        if p["y"] < miny:
            miny = p["y"]
        elif p["y"] > maxy:
            maxy = p["y"]
    return {"minx": minx, "maxx": maxx, "miny": miny, "maxy": maxy}


def get_scale_and_center_parameters(pointlist, center=False):
    """ Take a list of points and calculate the factors for scaling and moving
        it so that it's in the unit square. Keept the aspect ratio.
        Optionally center the points inside of the unit square.
    """
    a = get_bounding_box(pointlist)

    width = a['maxx'] - a['minx']
    height = a['maxy'] - a['miny']

    factorX = 1
    factorY = 1
    if width != 0:
        factorX = 1./width

    if height != 0:
        factorY = 1./height

    factor = min(factorX, factorY)
    addx = 0
    addy = 0

    if center:
        add = (1 - (max(factorX, factorY) / factor)) / 2

        if factor == factorX:
            addy = add
        else:
            addx = add

    return {"factor": factor, "addx": addx, "addy": addy,
            "minx": a['minx'], "miny": a['miny']}


def scale_and_center(pointlist, center=False):
    """ Take a list of points and scale and move it so that it's in the unit
        square. Keep the aspect ratio. Optionally center the points inside of
        the unit square.

        >>> scale_and_center([{'x': 0, 'y': 0}, {'x': 10, 'y': 10}])
        [{'y': 0.0, 'x': 0.0}, {'y': 1.0, 'x': 1.0}]
    """

    flat_pointlist = list_of_pointlists2pointlist(pointlist)

    tmp = get_scale_and_center_parameters(flat_pointlist, center)
    factor, addx, addy = tmp['factor'], tmp['addx'], tmp['addy']
    minx, miny = tmp['minx'], tmp['miny']

    for linenr, line in enumerate(pointlist):
        for key, p in enumerate(line):
            pointlist[linenr][key] = {"x": (p["x"] - minx) * factor + addx,
                                      "y": (p["y"] - miny) * factor + addy}

    return pointlist


def distance(p1, p2, squared=False):
    """ Calculate the squared eucliden distance of two points.
    @param  associative array $p1 first point
    @param  associative array $p2 second point
    @return float

    >>> distance({'x': 0, 'y': 0}, {'x': 3, 'y': 4})
    5.0
    >>> '%.2f' % distance({'x': 0, 'y': 0}, {'x': 1, 'y': 22})
    '22.02'
    """
    dx = p1["x"] - p2["x"]
    dy = p1["y"] - p2["y"]
    if squared:
        return (dx*dx + dy*dy)
    else:
        return sqrt(dx*dx + dy*dy)


def dtw(A, B, simple=True, SQUARED=True):
    """ Calculate the distance of A and B by greedy dynamic time warping.
    @param  list A list of points
    @param  list B list of points
    @return float  Minimal distance you have to move points from A to get B

    >>> '%.2f' % dtw([{'x': 0, 'y': 0}, {'x': 1, 'y': 1}], \
                          [{'x': 0, 'y': 0}, {'x': 0, 'y': 5}], False)
    '4.12'
    >>> '%.2f' % dtw([{'x': 0, 'y': 0}, {'x':0, 'y': 10}, \
                                    {'x': 1, 'y': 22}, {'x': 2, 'y': 2}], \
                          [{'x': 0, 'y': 0}, {'x': 0, 'y': 5}], False)
    '25.63'
    >>> '%.2f' % dtw( [{'x': 0, 'y': 0}, {'x': 0, 'y': 5}], \
                                    [{'x': 0, 'y': 0}, {'x':0, 'y': 10}, \
                                    {'x': 1, 'y': 22}, {'x': 2, 'y': 2}], \
                      False)
    '25.63'
    """
    global logging
    if len(A) == 0:
        logging.warning("A was empty. B:")
        logging.warning(A)
        logging.warning("B:")
        #logging.warning(B)
        throw
        return 0
    if len(B) == 0:
        logging.warning("B was empty. A:")
        #logging.warning(A)
        logging.warning("B:")
        #logging.warning(B)
        return 0

    distanceSum = 0.0
    if isinstance(A[0], list):
        if len(A) != len(B):
            return float("inf")
        else:
            from Dtw import Dtw
            for lineA, lineB in zip(A, B):
                a = Dtw(lineA[:], lineB, lambda a, b: distance(a, b, SQUARED))
                distanceSum += a.calculate(simple)
    else:
        from Dtw import Dtw
        a = Dtw(A[:], B, lambda a, b: distance(a, b, SQUARED))
        distanceSum += a.calculate(simple)

    return distanceSum


def LotrechterAbstand(p3, p1, p2):
    """
     * Calculate the distance from p3 to the line defined by p1 and p2.
     * @param list p1 associative array with "x" and "y" (start of line)
     * @param list p2 associative array with "x" and "y" (end of line)
     * @param list p3 associative array with "x" and "y" (point)
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


def DouglasPeucker(PointList, EPSILON):
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


def douglas_peucker(pointlist, EPSILON):
    """
     Apply the Douglas-Peucker algorithm to each line of $pointlist seperately.
     @param  array $pointlist see pointList()
     @return pointlist
    """
    for i in range(0, len(pointlist)):
        pointlist[i] = DouglasPeucker(pointlist[i], EPSILON)
    return pointlist


def pointLineList(linelistP):
    """Get a list of lists of tuples from a JSON string.
       Those lists represent lines with control points.
    >>> pointLineList('[[{"x":606,"y":411,"time":33}, {"x":605,"y":411,"time":35}, {"x":605,"y":412,"time":39}]]')
    [[{u'y': 411, u'x': 606, u'time': 33}, {u'y': 411, u'x': 605, u'time': 35}, {u'y': 412, u'x': 605, u'time': 39}]]
    """
    global logging
    linelist = json.loads(linelistP)

    if len(linelist) == 0:
        logging.waring("Pointlist was empty. Search for '" +
                       linelistP + "' in `wm_raw_draw_data`.")
    return linelist


def list_of_pointlists2pointlist(data):
    result = []
    for line in data:
        result += line
    return result


def get_dimensions(pointlist):
    a = get_bounding_box(pointlist)
    return {"width": a['maxx'] - a['minx'], "height": a['maxy'] - a['miny']}


def get_probability_from_distance(results):
    """ Get a list of results with dtw and formula id and return a dict mapping
        formula-ids to probabilities.

    >>> get_probability_from_distance([{'dtw': 5.638895307327028, 'formula_id': 33L}, {'dtw': 0.30368392840347985, 'formula_id': 31L}])
    [{'p': 0.9952042189554645, 'formula_id': 31L}, {'p': 0.0047957810445354, 'formula_id': 33L}]
    """
    # check if one distance is 0 and meanwhile build sum of distances.
    summe = 0.0
    modified = {}
    for result in results:
        formula_id = result['formula_id']
        dtw = result['dtw']
        if dtw == 0:
            logging.warning("Probability of 1!: %s" % str(formula_id))
            logging.warning(results)
            return [{'formula_id': formula_id, 'p': 1}]
        else:
            modified[formula_id] = exp(-dtw)
            summe += modified[formula_id]

    results = modified

    probabilities = []
    for formula_id, p in results.items():
        probabilities.append({'formula_id': formula_id, 'p': p / summe})
    return sorted(probabilities, key=lambda k: k['p'], reverse=True)


def classify(datasets, A, EPSILON=0, THRESHOLD=100, FLATTEN=True,
             SPACE_EVENLY=False, POINTS=100):
    """
    Classify A with data from datasets and smoothing of EPSILON.
    @param  list datasets [
                            {'data' => ...,
                             'accepted_formula_id' => ...,
                             'id' => ...,
                             'formula_in_latex' => ...,
                            }
                          ]
    @param  list A   List of points
    @return list     List of possible classifications, ordered DESC by
                       likelines
    """
    results = []
    for key, dataset in enumerate(datasets):
        B = dataset['data']
        B = pointLineList(B)
        if EPSILON > 0:
            B = douglas_peucker(B, EPSILON)

        if SPACE_EVENLY:
            Bnew = []
            for line in B:
                Bnew.append(space_evenly(line, POINTS))
            B = Bnew

        B = scale_and_center(B)

        if FLATTEN:
            B = list_of_pointlists2pointlist(B)

        results.append({"dtw": dtw(A, B),
                        "latex": dataset['accepted_formula_id'],
                        "id": dataset['id'],
                        "latex": dataset['formula_in_latex'],
                        "formula_id": dataset['formula_id']})

    results = sorted(results, key=lambda k: k['dtw'])
    results = filter(lambda var: var['dtw'] < THRESHOLD, results)
    # get only best match for each single symbol
    results2 = {}
    for row in results:
        if row['formula_id'] in results2:
            results2[row['formula_id']] = min(results2[row['formula_id']],
                                              row['dtw'])
        else:
            results2[row['formula_id']] = row['dtw']

    results = [{'formula_id': key, 'dtw': el} for key, el in results2.items()]
    results = sorted(results, key=lambda k: k['dtw'])[:10]

    return get_probability_from_distance(results)

if __name__ == "__main__":
    import doctest
    doctest.testmod()

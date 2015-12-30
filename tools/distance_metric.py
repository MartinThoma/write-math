#!/usr/bin/env python
# -*- coding: utf-8 -*-

from hwrt import handwritten_data
import math
import numpy


def softmax(w, t=1.0):
    """
    Calculate the softmax of a list of numbers w.

    Parameters
    ----------
    w : list of numbers

    Returns
    -------
    a list of the same length as w of non-negative numbers

    Examples
    --------
    >>> softmax([0.1, 0.2])
    array([ 0.47502081,  0.52497919])
    >>> softmax([-0.1, 0.2])
    array([ 0.42555748,  0.57444252])
    >>> softmax([0.9, -10])
    array([  9.99981542e-01,   1.84578933e-05])
    >>> softmax([0, 10])
    array([  4.53978687e-05,   9.99954602e-01])
    """
    e = numpy.exp(numpy.array(w) / t)
    dist = e / numpy.sum(e)
    return dist


def point_distance(p1, p2, squared=False):
    """
    Calculate the squared eucliden distance of two points.

    Parameters
    ----------
    p1 : associative array $p1 first point
    p2 : associative array $p2 second point

    Returns
    -------
    float

    Examples
    --------
    >>> point_distance({'x': 0, 'y': 0}, {'x': 3, 'y': 4})
    5.0
    >>> '%.2f' % point_distance({'x': 0, 'y': 0}, {'x': 1, 'y': 22})
    '22.02'
    """
    dx = p1["x"] - p2["x"]
    dy = p1["y"] - p2["y"]
    if squared:
        return (dx*dx + dy*dy)
    else:
        return math.sqrt(dx*dx + dy*dy)


def handwritten_data_greedy_matching_distance(a, b):
    """
    Parameters
    ----------
    a : HandwrittenData object
    b : HandwrittenData object

    Returns
    -------
    float
        Distance of a and b
    """
    assert isinstance(a, handwritten_data.HandwrittenData), \
        "handwritten data is not of type HandwrittenData, but of %r" % \
        type(a)
    assert isinstance(b, handwritten_data.HandwrittenData), \
        "handwritten data is not of type HandwrittenData, but of %r" % \
        type(b)

    def sequence_greedy_distance(A, B, distance_func=point_distance):
        """Calculate the distance between pointlist A and pointlist B.

        Parameters
        ----------
        A : list of points
            this list gets modified, so you should copy it if you want to use
            it later
        B : list of points
            this list gets modified, so you should copy it if you want to use
            it later

        Returns
        -------
        non-negative float
        """
        assert isinstance(A, list), \
            "A is not of type list, but of %r" % type(A)
        assert isinstance(B, list), \
            "B is not of type list, but of %r" % type(B)
        assert len(A) > 0, "A is empty (%s)" % str(A)
        assert len(B) > 0, "B is empty (%s)" % str(B)
        d = 0
        if len(A) == 1:
            a2 = A.pop()
            for p in B:
                d = d + distance_func(a2, p)
            return d
        if len(B) == 1:
            b2 = B.pop()
            for p in A:
                d = d + distance_func(b2, p)
            return d
        a = A.pop()
        b = B.pop()
        d = distance_func(a, b)
        a2 = A.pop()
        b2 = B.pop()
        while len(A) > 0 and len(B) > 0:
            l = distance_func(a2, b)
            m = distance_func(a2, b2)
            r = distance_func(a, b2)
            mu = min(l, m, r)
            d += mu
            if (l == mu):
                a = a2
                a2 = A.pop()
            elif (r == mu):
                b = b2
                b2 = B.pop()
            else:
                a = a2
                b = b2
                a2 = A.pop()
                b2 = B.pop()
        if len(A) == 0:
            for p in B:
                d += distance_func(a2, p)
        elif len(B) == 0:
            for p in A:
                d += distance_func(b2, p)
        return d

    a_pointlist = [[item for sublist in a.get_pointlist() for item in sublist]]
    b_pointlist = [[item for sublist in b.get_pointlist() for item in sublist]]

    distance_sum = 0.0
    if len(a_pointlist) != len(b_pointlist):
        return float("inf")
    else:
        for lineA, lineB in zip(a_pointlist, b_pointlist):
            distance_sum += sequence_greedy_distance(lineA[:], lineB[:])
    return distance_sum

if __name__ == '__main__':
    import doctest
    doctest.testmod()

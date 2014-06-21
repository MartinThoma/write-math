# -*- coding: utf-8 -*-
# An pure python implemetation of Dynamic Time Warpping
# http://en.wikipedia.org/wiki/Dynamic_time_warping


import logging
logging.basicConfig(filename='classifier.log',
                    level=logging.DEBUG,
                    format='%(asctime)s %(levelname)s: %(message)s')

class Dtw(object):
    def __init__(self, seq1, seq2, distance_func=None):
        '''
        seq1, seq2 are two lists,
        distance_func is a function for calculating
        the local distance between two elements.
        '''
        self._seq1 = seq1
        self._seq2 = seq2
        self._distance_func = distance_func if distance_func else lambda: 0
        self._map = {(-1, -1): 0.0}
        self._distance_matrix = {}
        self._path = []

    def get_distance(self, i1, i2):
        ret = self._distance_matrix.get((i1, i2))
        if not ret:
            ret = self._distance_func(self._seq1[i1], self._seq2[i2])
            self._distance_matrix[(i1, i2)] = ret
        return ret

    def calculate_backward(self, i1, i2):
        '''
        Calculate the dtw distance between
        seq1[:i1 + 1] and seq2[:i2 + 1]
        '''
        if self._map.get((i1, i2)) is not None:
            return self._map[(i1, i2)]

        if i1 == -1 or i2 == -1:
            self._map[(i1, i2)] = float('inf')
            return float('inf')

        min_i1, min_i2 = min((i1 - 1, i2), (i1, i2 - 1), (i1 - 1, i2 - 1),
                             key=lambda x: self.calculate_backward(*x))

        self._map[(i1, i2)] = self.get_distance(i1, i2) + \
            self.calculate_backward(min_i1, min_i2)

        return self._map[(i1, i2)]

    def get_path(self):
        '''
        Calculate the path mapping.
        Must be called after calculate()
        '''
        i1, i2 = (len(self._seq1) - 1, len(self._seq2) - 1)
        while (i1, i2) != (-1, -1):
            self._path.append((i1, i2))
            min_i1, min_i2 = min((i1 - 1, i2), (i1, i2 - 1), (i1 - 1, i2 - 1),
                                 key=lambda x: self._map[x[0], x[1]])
            i1, i2 = min_i1, min_i2
        return self._path

    def calculate(self, simplified=True):
        if simplified:
            A = self._seq1
            B = self._seq2
            d = 0
            if len(A) == 0 or len(B) == 0:
                logging.error("This should not happen (0)")
                return 0
            if len(A) == 1:
                logging.info("A had only one")
                logging.info(A)
                a2 = A.pop()
                for p in B:
                    d = d + self._distance_func(a2, p)
                return d
            if len(B) == 1:
                b2 = B.pop()
                for p in A:
                    d = d + self._distance_func(b2, p)
                return d
            a = A.pop()
            b = B.pop()
            d = self._distance_func(a, b)
            a2 = A.pop()
            b2 = B.pop()
            while len(A) > 0 and len(B) > 0:
                l = self._distance_func(a2, b)
                m = self._distance_func(a2, b2)
                r = self._distance_func(a, b2)
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
                    d += self._distance_func(a2, p)
            elif len(B) == 0:
                for p in A:
                    d += self._distance_func(b2, p)
            return d
        else:
            return self.calculate_backward(len(self._seq1) - 1,
                                           len(self._seq2) - 1)

#!/usr/bin/env python

from math import sqrt, exp
import logging
import HandwrittenData


class dtw_classifier(object):
    def __init__(self, THRESHOLD=100):
        self.datasets = []
        # Maximum distance a symbol may have
        self.THRESHOLD = THRESHOLD

    def learn(self, trainingdata):
        """
        @param trainingdata: Dictionaries with 'handwriting' elements and
                             'formula_id', 'id', 'formula_in_latex'
        """
        assert type(trainingdata) is list
        for data in trainingdata:
            assert 'id' in data
            assert 'formula_in_latex' in data
            assert 'formula_id' in data
            assert 'handwriting' in data
            self.datasets.append(data)

    def classify(self, A):
        """
        Classify A with data from datasets and smoothing of EPSILON.
        @param  list A   List of points
        @return list     List of possible classifications, ordered DESC by
                           likelines
        """

        assert type(A) is HandwrittenData.HandwrittenData

        def dtw(A, B, simple=True, SQUARED=True):
            """ Calculate the distance of A and B by greedy dynamic time
            warping.
            @param  list A list of points
            @param  list B list of points
            @return float  Minimal distance you have to move points from A to
                           get B
            """
            assert type(A) is list
            assert type(B) is list

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

            distanceSum = 0.0
            if isinstance(A[0], list):
                if len(A) != len(B):
                    return float("inf")
                else:
                    from Dtw import Dtw
                    for lineA, lineB in zip(A, B):
                        a = Dtw(lineA[:],
                                lineB,
                                lambda a, b: distance(a, b, SQUARED)
                                )
                        distanceSum += a.calculate(simple)
            else:
                from Dtw import Dtw
                a = Dtw(A[:], B, lambda a, b: distance(a, b, SQUARED))
                distanceSum += a.calculate(simple)

            return distanceSum

        results = []
        A = A.get_pointlist()

        for key, dataset in enumerate(self.datasets):
            B = dataset['handwriting'].get_pointlist()
            results.append(dict({"dtw": dtw(A, B)}.items() + dataset.items()))

        results = sorted(results, key=lambda k: k['dtw'])
        results = filter(lambda var: var['dtw'] < self.THRESHOLD, results)
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

        def get_probability_from_distance(results):
            """ Get a list of results with dtw and formula id and return a
                dict mapping formula-ids to probabilities.
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

        return get_probability_from_distance(results)

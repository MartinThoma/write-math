#!/usr/bin/env python

"""
Classify data with a greedy algorithm that is simmilar to DTW (but not DTW!).
"""

import HandwrittenData
import distance_metric
from collections import defaultdict


class dtw_classifier(object):
    def __init__(self, THRESHOLD=1000000):
        self.datasets = []
        # Maximum distance a symbol may have
        self.THRESHOLD = THRESHOLD
        self.datasets_counter = defaultdict(int)  # count data by symbol_id

    def learn(self, trainingdata):
        """
        @param trainingdata: Dictionaries with 'handwriting' elements and
                             'formula_id', 'id', 'formula_in_latex'
        """
        assert type(trainingdata) is list
        for data in trainingdata:
            assert 'formula_in_latex' in data
            assert 'handwriting' in data
            assert isinstance(data['handwriting'],
                              HandwrittenData.HandwrittenData), \
                ("handwritten data is not of type HandwrittenData, "
                 "but of %r") % type(data['handwriting'])
            if self.datasets_counter[data['handwriting'].formula_id] < 50:
                self.datasets_counter[data['handwriting'].formula_id] += 1
                self.datasets.append(data)

    def classify(self, A):
        """
        Classify A with data from datasets and smoothing of EPSILON.
        @param  list A   List of points
        @return list     List of possible classifications, ordered DESC by
                           likelines
        """

        assert type(A) is HandwrittenData.HandwrittenData

        # key: formula_id, value: (dtw, Handwriting) (lowest prefered)
        best_by_symbol = {}

        for dataset in self.datasets:
            B = dataset['handwriting']
            d = distance_metric.handwritten_data_greedy_matching_distance(A, B)
            if d < self.THRESHOLD:
                if B.formula_id in best_by_symbol:
                    if d < best_by_symbol[B.formula_id]:
                        best_by_symbol[B.formula_id] = (d, B)
                else:
                    best_by_symbol[B.formula_id] = (d, B)

        results = []
        for _, tmp in best_by_symbol.items():
            d, B = tmp
            results.append({'p': -1,
                            'dtw': d,
                            'formula_id': B.formula_id,
                            'handwriting': B})
        results = sorted(results, key=lambda k: k['dtw'])[:10]

        def get_probability_from_distance(results):
            """ Get a list of results with dtw and formula id and return a
                dict mapping formula-ids to probabilities.
            """
            numeric_factor = 100
            distances = [-result['dtw']/numeric_factor for result in results]
            softmax_results = distance_metric.softmax(distances)
            probabilities = []
            for dictionary, p in zip(results, softmax_results):
                probabilities.append({'formula_id': dictionary, 'p': p})
            return sorted(probabilities, key=lambda k: k['p'], reverse=True)

        return get_probability_from_distance(results)

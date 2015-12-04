#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
Classify data with a greedy algorithm that is simmilar to DTW (but not DTW!).
"""

import HandwrittenData
import distance_metric
from collections import defaultdict


class DtwClassifier(object):
    """
    A classifier which makes use of dynamic time warping.
    """
    def __init__(self, threshold=1000000):
        self.datasets = []
        # Maximum distance a symbol may have
        self.threshold = threshold
        self.datasets_counter = defaultdict(int)  # count data by symbol_id

    def learn(self, trainingdata):
        """
        Parameters
        ----------
        trainingdata: dict
            has keys 'handwriting', 'formula_id', 'id', 'formula_in_latex'
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

    def classify(self, a):
        """
        Classify a with data from datasets and smoothing of EPSILON.

        Parameters
        ----------
        a : list
            List of points

        Returns
        -------
        list :
            List of possible classifications, ordered DESC by likelines
        """

        assert type(a) is HandwrittenData.HandwrittenData

        # key: formula_id, value: (dtw, Handwriting) (lowest prefered)
        best_by_symbol = {}

        for dataset in self.datasets:
            b = dataset['handwriting']
            d = distance_metric.handwritten_data_greedy_matching_distance(a, b)
            if d < self.threshold:
                if b.formula_id in best_by_symbol:
                    if d < best_by_symbol[b.formula_id]:
                        best_by_symbol[b.formula_id] = (d, b)
                else:
                    best_by_symbol[b.formula_id] = (d, b)

        results = []
        for _, tmp in best_by_symbol.items():
            d, b = tmp
            results.append({'p': -1,
                            'dtw': d,
                            'formula_id': b.formula_id,
                            'handwriting': b})
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

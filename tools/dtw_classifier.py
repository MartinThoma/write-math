#!/usr/bin/env python

import HandwrittenData
import distance_metric
from collections import defaultdict


class dtw_classifier(object):
    def __init__(self, THRESHOLD=100):
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

        results = []

        for key, dataset in enumerate(self.datasets):
            B = dataset['handwriting']
            d = distance_metric.handwritten_data_greedy_matching_distance(A, B)
            results.append(dict({"dtw": d}.items() + dataset.items()))

        results = sorted(results, key=lambda k: k['dtw'])
        results = filter(lambda var: var['dtw'] < self.THRESHOLD, results)
        # get only best match for each single symbol
        results2 = {}
        for row in results:
            if row['handwriting'].formula_id in results2:
                results2[row['handwriting'].formula_id] = min(results2[row['handwriting'].formula_id],
                                                  row['dtw'])
            else:
                results2[row['handwriting'].formula_id] = row['dtw']

        results = [{'formula_id': key, 'dtw': el}
                   for key, el in results2.items()]
        results = sorted(results, key=lambda k: k['dtw'])[:10]

        def get_probability_from_distance(results):
            """ Get a list of results with dtw and formula id and return a
                dict mapping formula-ids to probabilities.
            """
            distances = [-result['dtw'] for result in results]
            softmax_results = distance_metric.softmax(distances)
            probabilities = []
            for formula_id, p in zip(results, softmax_results):
                probabilities.append({'formula_id': formula_id, 'p': p})
            return sorted(probabilities, key=lambda k: k['p'], reverse=True)

        return get_probability_from_distance(results)

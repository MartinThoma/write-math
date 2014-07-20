#!/usr/bin/env python
# -*- coding: utf-8 -*-

import logging
import json
import matplotlib.pyplot as plt


class HandwrittenData(object):
    def __init__(self, raw_data_json, formula_id=None):
        self.raw_data_json = raw_data_json
        self.formula_id = formula_id
        assert type(json.loads(self.raw_data_json)) is list, \
            "raw_data_json is not JSON: %r" % self.raw_data_json
        assert len(self.get_pointlist()) >= 1, \
            "The pointlist of formula_id %i is %s" % (self.formula_id,
                                                      self.get_pointlist())

    def get_pointlist(self):
        """Get a list of lists of tuples from JSON raw data string.
           Those lists represent lines with control points.
        """
        try:
            pointlist = json.loads(self.raw_data_json)
        except Exception as inst:
            logging.debug("pointLineList: linelistP")
            logging.debug(self.raw_data_json)
            logging.debug("didn't work")
            raise inst

        if len(pointlist) == 0:
            logging.waring("Pointlist was empty. Search for '" +
                           self.raw_data_json + "' in `wm_raw_draw_data`.")
        return pointlist

    def set_pointlist(self, pointlist):
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

    def preprocessing(self, algorithms):
        assert type(algorithms) is list
        for algorithm, parameters in algorithms:
            if type(parameters) is dict:
                algorithm(self, **parameters)
            elif type(parameters) is list:
                algorithm(self, *parameters)
            else:
                raise Exception

    def show(self):
        for line in self.get_pointlist():
            xs, ys = [], []
            for p in line:
                xs.append(p['x'])
                ys.append(p['y'])
            plt.plot(xs, ys, '-o')
        plt.gca().invert_yaxis()
        plt.show()

if __name__ == '__main__':
    a = HandwrittenData('[[{"x":305,"y":260,"time":35},{"x":305,"y":264,"time":43},{"x":306,"y":270,"time":52},{"x":306,"y":276,"time":59},{"x":306,"y":283,"time":67},{"x":306,"y":291,"time":75},{"x":306,"y":299,"time":83},{"x":306,"y":307,"time":91},{"x":306,"y":315,"time":99},{"x":306,"y":322,"time":107},{"x":306,"y":330,"time":115},{"x":308,"y":338,"time":123},{"x":308,"y":344,"time":132},{"x":308,"y":350,"time":140},{"x":308,"y":356,"time":149},{"x":308,"y":362,"time":156},{"x":308,"y":368,"time":164},{"x":308,"y":372,"time":172},{"x":308,"y":376,"time":180},{"x":308,"y":380,"time":187},{"x":308,"y":381,"time":196},{"x":308,"y":382,"time":205},{"x":308,"y":383,"time":212},{"x":308,"y":384,"time":219}],[{"x":362,"y":269,"time":6},{"x":360,"y":271,"time":11},{"x":356,"y":275,"time":19},{"x":352,"y":279,"time":27},{"x":348,"y":283,"time":35},{"x":344,"y":287,"time":43},{"x":340,"y":291,"time":51},{"x":336,"y":296,"time":59},{"x":334,"y":302,"time":67},{"x":330,"y":308,"time":75},{"x":326,"y":312,"time":83},{"x":322,"y":316,"time":91},{"x":318,"y":320,"time":99},{"x":316,"y":324,"time":107},{"x":314,"y":325,"time":115},{"x":313,"y":327,"time":123},{"x":311,"y":328,"time":131},{"x":309,"y":329,"time":139},{"x":308,"y":329,"time":147},{"x":307,"y":330,"time":155},{"x":306,"y":330,"time":172},{"x":306,"y":331,"time":180},{"x":305,"y":331,"time":188},{"x":304,"y":331,"time":203},{"x":306,"y":332,"time":325},{"x":308,"y":332,"time":333},{"x":309,"y":333,"time":339},{"x":312,"y":334,"time":347},{"x":314,"y":335,"time":355},{"x":316,"y":337,"time":363},{"x":318,"y":338,"time":372},{"x":320,"y":340,"time":379},{"x":322,"y":342,"time":387},{"x":325,"y":344,"time":396},{"x":327,"y":347,"time":403},{"x":329,"y":349,"time":411},{"x":330,"y":351,"time":419},{"x":332,"y":352,"time":427},{"x":333,"y":354,"time":435},{"x":335,"y":355,"time":443},{"x":336,"y":357,"time":451},{"x":337,"y":358,"time":459},{"x":338,"y":360,"time":468},{"x":339,"y":361,"time":476},{"x":340,"y":362,"time":484}]]')
    a.show()

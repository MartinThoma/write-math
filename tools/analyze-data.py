#!/usr/bin/env python

"""Analyze data in a pickle file by maximum time / width / height and
   similar features.
"""

from __future__ import print_function
import os
import logging
import sys
logging.basicConfig(format='%(asctime)s %(levelname)s %(message)s',
                    level=logging.DEBUG,
                    stream=sys.stdout)
import cPickle as pickle
import time
import numpy
from collections import defaultdict
# My modules
from HandwrittenData import HandwrittenData  # Needed because of pickle
import features
import Geometry
import utils


def sort_by_formula_id(raw_datasets):
    by_formula_id = defaultdict(list)
    for el in raw_datasets:
        by_formula_id[el['handwriting'].formula_id].append(el['handwriting'])
    return by_formula_id


def analyze_feature(raw_datasets, feature, filename):
    """
    @param feature - for example feature = features.AspectRatio()
                   the feature has to be 1 dimensional at the moment
    @param filename - where to store the result
    """
    open(filename, 'w').close()  # Truncate the file
    f = open(filename, "a")

    by_formula_id = sort_by_formula_id(raw_datasets)

    data_list = []
    for formula_id, datasets in by_formula_id.items():
        values = []
        for data in datasets:
            values.append(feature(data)[0])
            if data.formula_id == 183:
                f.write("%0.4f\n" % feature(data)[0])
        data_list.append((datasets[0].formula_in_latex,
                          numpy.mean(values),
                          numpy.std(values)))
    f.close()
    data_list = sorted(data_list, key=lambda n: n[2], reverse=True)
    for latex, mean, std in data_list:
        print("%s: mean: %0.2f, std: %0.2f" % (latex, mean, std))


def analyze_aspect_ratio(raw_datasets):
    filename = "aspect_ratios-int.txt"
    open(filename, 'w').close()  # Truncate the file
    strokefile = open(filename, "a")

    by_formula_id = sort_by_formula_id(raw_datasets)
    aspect_ratio = features.AspectRatio()
    data_list = []
    for formula_id, datasets in by_formula_id.items():
        values = []
        for data in datasets:
            values.append(aspect_ratio(data)[0])
            if data.formula_id == 183:
                strokefile.write("%0.4f\n" % aspect_ratio(data)[0])
        data_list.append((datasets[0].formula_in_latex,
                          numpy.mean(values),
                          numpy.std(values)))
    strokefile.close()
    data_list = sorted(data_list, key=lambda n: n[2], reverse=True)
    for latex, mean, std in data_list:
        print("%s: mean: %0.2f, std: %0.2f" % (latex, mean, std))


def get_aspect_ratio(raw_datasets):
    """For each symbol: sum up the length of all strokes."""
    filename = "aspect_ratios.txt"
    open(filename, 'w').close()  # Truncate the file
    strokefile = open(filename, "a")
    start_time = time.time()
    aspect_ratio = features.AspectRatio()
    for i, raw_dataset in enumerate(raw_datasets):
        if i % 100 == 0 and i > 0:
            utils.print_status(len(raw_datasets), i, start_time)
        ink = aspect_ratio(raw_dataset['handwriting'])[0]
        strokefile.write("%0.2f\n" % ink)
    print("\r100%"+"\033[K\n")
    strokefile.close()


def get_bounding_box_distance(raw_datasets):
    """Get the distances between bounding boxes of strokes of a single symbol.
       Can only be applied to recordings with at least two strokes.
    """

    # TODO: Deal with http://www.martin-thoma.de/write-math/symbol/?id=167
    # 193
    # 524

    def get_stroke_bounding_box(stroke):
        min_x, max_x = stroke[0]['x'], stroke[0]['x']
        min_y, max_y = stroke[0]['y'], stroke[0]['y']
        #  if len(stroke) == 1: ?
        for point in stroke:
            min_x = min(point['x'], min_x)
            max_x = max(point['x'], max_x)
            min_y = min(point['y'], min_y)
            max_y = max(point['y'], max_y)
        minp = Geometry.Point(min_x, min_y)
        maxp = Geometry.Point(max_x, max_y)
        return Geometry.BoundingBox(minp, maxp)

    def get_bb_distance(a, b):
        points_a = [Geometry.Point(a.p1.x, a.p1.y),
                    Geometry.Point(a.p1.x, a.p2.y),
                    Geometry.Point(a.p2.x, a.p1.y),
                    Geometry.Point(a.p2.x, a.p2.y)]
        points_b = [Geometry.Point(b.p1.x, b.p1.y),
                    Geometry.Point(b.p1.x, b.p2.y),
                    Geometry.Point(b.p2.x, b.p1.y),
                    Geometry.Point(b.p2.x, b.p2.y)]
        min_distance = points_a[0].dist_to(points_b[0])
        for pa in points_a:
            for pb in points_b:
                min_distance = min(min_distance, pa.dist_to(pb))
        lines_a = [Geometry.LineSegment(points_a[0], points_a[1]),
                   Geometry.LineSegment(points_a[1], points_a[2]),
                   Geometry.LineSegment(points_a[2], points_a[3]),
                   Geometry.LineSegment(points_a[3], points_a[0])]
        lines_b = [Geometry.LineSegment(points_b[0], points_b[1]),
                   Geometry.LineSegment(points_b[1], points_b[2]),
                   Geometry.LineSegment(points_b[2], points_b[3]),
                   Geometry.LineSegment(points_b[3], points_b[0])]
        for la in lines_a:
            for lb in lines_b:
                min_distance = min(min_distance, la.dist_to(lb))
        return min_distance

    bbfile = open("bounding_boxdist.html", "a")
    start_time = time.time()
    for i, raw_dataset in enumerate(raw_datasets):
        if i % 100 == 0 and i > 0:
            utils.print_status(len(raw_datasets), i, start_time)
        pointlist = raw_dataset['handwriting'].get_pointlist()
        if len(pointlist) < 2:
            continue
        bounding_boxes = []
        for stroke in pointlist:
            # TODO: Get bounding boxes of strokes
            bounding_boxes.append(get_stroke_bounding_box(stroke))

        got_change = True
        while got_change:
            got_change = False
            i = 0
            while i < len(bounding_boxes):
                j = i + 1
                while j < len(bounding_boxes):
                    if Geometry.do_bb_intersect(bounding_boxes[i],
                                                bounding_boxes[j]):
                        got_change = True
                        new_bounding_boxes = []
                        p1x = min(bounding_boxes[i].p1.x, bounding_boxes[j].p1.x)
                        p1y = min(bounding_boxes[i].p1.y, bounding_boxes[j].p1.y)
                        p2x = max(bounding_boxes[i].p2.x, bounding_boxes[j].p2.x)
                        p2y = max(bounding_boxes[i].p2.y, bounding_boxes[j].p2.y)
                        p1 = Geometry.Point(p1x, p1y)
                        p2 = Geometry.Point(p2x, p2y)
                        new_bounding_boxes.append(Geometry.BoundingBox(p1, p2))
                        for k in range(len(bounding_boxes)):
                            if k != i and k != j:
                                new_bounding_boxes.append(bounding_boxes[k])
                        bounding_boxes = new_bounding_boxes
                    j += 1
                i += 1

        # sort bounding boxes (decreasing) by size
        bounding_boxes = sorted(bounding_boxes,
                                key=lambda bbox: bbox.get_area(),
                                reverse=True)

        # Bounding boxes have been merged as far as possible
        # check their distance and compare it with the highest dimension
        # (length/height) of the biggest bounding box
        if len(bounding_boxes) != 1:
            bb_dist = []
            for k, bb in enumerate(bounding_boxes):
                dist_tmp = []
                for j, bb2 in enumerate(bounding_boxes):
                    if k == j:
                        continue
                    dist_tmp.append(get_bb_distance(bb, bb2))
                bb_dist.append(min(dist_tmp))
            bb_dist = max(bb_dist)
            dim = max([bb.get_largest_dimension() for bb in bounding_boxes])
            if bb_dist > 1.5*dim:
                # bounding_box_h = raw_dataset['handwriting'].get_bounding_box()
                # bbsize = (bounding_box_h['maxx'] - bounding_box_h['minx']) * \
                #          (bounding_box_h['maxy'] - bounding_box_h['miny'])
                if raw_dataset['handwriting'].formula_id not in \
                   [635, 636, 936, 992, 260, 941, 934, 184] and \
                   raw_dataset['handwriting'].wild_point_count == 0 and \
                   raw_dataset['handwriting'].missing_line == 0:
                    # logging.debug("bb_dist: %0.2f" % bb_dist)
                    # logging.debug("dim: %0.2f" % dim)
                    # for bb in bounding_boxes:
                    #     print(bb)
                    #     print("width: %0.2f" % bb.get_width())
                    #     print("height: %0.2f" % bb.get_height())
                    #     print("maxdim: %0.2f" % bb.get_largest_dimension())
                    # bb_dist = []
                    # for k, bb in enumerate(bounding_boxes):
                    #     dist_tmp = []
                    #     for j, bb2 in enumerate(bounding_boxes):
                    #         if k == j:
                    #             continue
                    #         dist_tmp.append(get_bb_distance(bb, bb2))
                    #     print(dist_tmp)
                    #     bb_dist.append(min(dist_tmp))
                    # raw_dataset['handwriting'].show()
                    # exit()
                    bbfile.write("<a href='http://www.martin-thoma.de/write-math/view/?raw_data_id=%i'>a</a>\n" % raw_dataset['handwriting'].raw_data_id)
    print("\r100%"+"\033[K\n")


def get_max_distances(raw_datasets):
    """For each symbol and each line of the symbol: Get the maximum
       two points have. Print this distance to a file.
    """
    pass


def get_summed_symbol_strok_lengts(raw_datasets):
    """For each symbol: sum up the length of all strokes."""
    strokefile = open("stroke-lengths.txt", "a")
    start_time = time.time()
    calculate_ink = features.Ink()
    for i, raw_dataset in enumerate(raw_datasets):
        if i % 100 == 0 and i > 0:
            utils.print_status(len(raw_datasets), i, start_time)
        ink = calculate_ink(raw_dataset['handwriting'])[0]
        strokefile.write("%0.2f\n" % ink)
    print("\r100%"+"\033[K\n")
    strokefile.close()


def get_bounding_box_sizes(raw_datasets):
    """Get and save the metrics of each recordings bounding box.
       That includes width, height and time.
    """
    bouding_box_sizes = []
    start_time = time.time()
    widthfile = open("widths.txt", "a")
    heightfile = open("height.txt", "a")
    timefile = open("times.txt", "a")
    for i, raw_dataset in enumerate(raw_datasets):
        if i % 100 == 0 and i > 0:
            utils.print_status(len(raw_datasets), i, start_time)
        box = raw_dataset['handwriting'].get_bounding_box()
        widthfile.write(str(box["maxx"] - box["minx"]) + "\n")
        heightfile.write(str(box["maxy"] - box["miny"]) + "\n")
        timefile.write(str(box["maxt"] - box["mint"]) + "\n")
        if box["maxx"] - box["minx"] > 400:
            raw_dataset['handwriting'].show()
    print("\r100%"+"\033[K\n")
    widthfile.close()
    heightfile.close()
    timefile.close()
    return bouding_box_sizes


def get_time_between_controll_points(raw_datasets):
    """For each recording: Store the average time between controll points of
       one stroke / controll points of two different lines.
    """
    average_between_points = open("average_time_between_points.txt", "a")
    average_between_lines = open("average_time_between_lines.txt", "a")
    start_time = time.time()
    for i, raw_dataset in enumerate(raw_datasets):
        if i % 100 == 0 and i > 0:
            utils.print_status(len(raw_datasets), i, start_time)

        # Do the work
        times_between_points, times_between_lines = [], []
        last_line_end = None
        if len(raw_dataset['handwriting'].get_pointlist()) == 0:
            logging.warning("%i has no content." %
                            raw_dataset['handwriting'].raw_data_id)
            continue
        for line in raw_dataset['handwriting'].get_sorted_pointlist():
            if last_line_end is not None:
                times_between_lines.append(line[-1]['time'] - last_line_end)
            last_line_end = line[-1]['time']
            last_point_end = None
            for point in line:
                if last_point_end is not None:
                    times_between_points.append(point['time'] - last_point_end)
                last_point_end = point['time']
        # The recording might only have one point
        if len(times_between_points) > 0:
            average_between_points.write("%0.2f\n" %
                                         numpy.average(times_between_points))
        # The recording might only have one line
        if len(times_between_lines) > 0:
            average_between_lines.write("%0.2f\n" %
                                        numpy.average(times_between_lines))
    print("\r100%"+"\033[K\n")
    average_between_points.close()
    average_between_lines.close()


def main(handwriting_datasets_file):
    """Start the creation of the wanted metric."""
    # Load from pickled file
    logging.info("Start loading data '%s' ...", handwriting_datasets_file)
    loaded = pickle.load(open(handwriting_datasets_file))
    raw_datasets = loaded['handwriting_datasets']
    logging.info("%i datasets loaded.", len(raw_datasets))
    logging.info("Start analyzing...")
    # get_time_between_controll_points(raw_datasets)
    # get_bounding_box_sizes(raw_datasets)
    # get_summed_symbol_strok_lengts(raw_datasets)
    # get_bounding_box_distance(raw_datasets)
    analyze_aspect_ratio(raw_datasets)


if __name__ == '__main__':
    PROJECT_ROOT = utils.get_project_root()

    # Get latest model description file
    MODELS_FOLDER = os.path.join(PROJECT_ROOT, "archive/datasets")
    LATEST_DATASET = utils.get_latest_in_folder(MODELS_FOLDER, "raw.pickle")

    from argparse import ArgumentParser, ArgumentDefaultsHelpFormatter
    parser = ArgumentParser(description=__doc__,
                            formatter_class=ArgumentDefaultsHelpFormatter)
    parser.add_argument("-d", "--handwriting_datasets",
                        dest="handwriting_datasets",
                        help="where are the pickled handwriting_datasets?",
                        metavar="FILE",
                        type=lambda x: utils.is_valid_file(parser, x),
                        default=LATEST_DATASET)
    args = parser.parse_args()
    main(args.handwriting_datasets)

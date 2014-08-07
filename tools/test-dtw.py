#!/usr/bin/env python
# -*- coding: utf-8 -*-

from __future__ import print_function
import logging
import sys
logging.basicConfig(format='%(asctime)s %(levelname)s %(message)s',
                    level=logging.DEBUG,
                    stream=sys.stdout)
import time
from HandwrittenData import HandwrittenData  # Needed because of pickle
from dtw_classifier import dtw_classifier
from make_crossvalidation_dataset import main as make_crossvalidation_dataset
import cPickle as pickle
import logging
import os
import datetime
import utils


def pp_results(results, data, formula_id2latex):
    """Pretty-Print the results of the cross-validation."""
    s = "Raw-Data-ID: %i; Reality: %s\n" % \
        (data['id'], formula_id2latex[data['formula_id']])
    for result in results:
        s += "\t%0.3f for\t%s (Raw_dataset_id: %i)\n" % \
             (result['p'],
              formula_id2latex[result['formula_id']['formula_id']],
              result['formula_id']['handwriting'].raw_data_id)
    return s


def main(K_FOLD=10, get_new_dataset=False):
    if get_new_dataset:
        logging.info("Download dataset ...")
        from download_dataset import main as download_dataset
        download_dataset()
        logging.info("make_crossvalidation_dataset ...")
        make_crossvalidation_dataset()

    PROJECT_ROOT = utils.get_project_root()

    logging_folder = os.path.join(PROJECT_ROOT, "archive/logs")
    time_prefix = time.strftime("%Y-%m-%d-%H-%M")
    LOGFILE = os.path.join(logging_folder, "%s-DTW.log" % time_prefix)
    with open(LOGFILE, "a") as f:
        f.write("Correct_Formula_ID,RAW_DATA_ID,1,2,3,4,5,6,7,8,9,10,"
                "confused 1,confused 2,confused 3,confused 4, confused 5,"
                "confused 6,confused 7,confused 8, confused 9,"
                "confused 10\n")

    # Get latest model description file
    cv_folder = os.path.join(PROJECT_ROOT, "archive/cv-datasets")
    latest_cv_dataset = utils.get_latest_in_folder(cv_folder, ".pickle")
    logging.info("Load '%s' ..." % latest_cv_dataset)
    tmp = pickle.load(open(latest_cv_dataset))
    cv = tmp['cv']
    formula_id2latex = tmp['formula_id2latex']

    # start testing
    logging.info("Start testing")
    ca = []
    i = 0

    for testset in range(K_FOLD):
        logging.info("Start test set: %i" % testset)
        ca.append({'correct': 0, 'wrong': 0, 'c10': 0, 'w10': 0, 'time': 0,
                   'processed_datasets': 0})
        classifier = dtw_classifier()

        learndata = []
        for i in range(K_FOLD):
            if i != testset:
                learndata += cv[i]
        classifier.learn(learndata)
        start_time = time.time()
        for i_loop, data in enumerate(cv[testset]):
            if i_loop % 10 == 0 and i_loop > 0:
                # Show how much work was done / how much work is remaining
                percentage_done = float(i)/len(cv[testset])
                current_running_time = time.time() - start_time
                remaining_seconds = current_running_time / percentage_done
                tmp = datetime.timedelta(seconds=remaining_seconds)
                sys.stdout.write("\r%0.2f%% (%s remaining)   " %
                                 (percentage_done*100, str(tmp)))
                sys.stdout.flush()
            i += 1
            start = time.time()
            results = classifier.classify(data['handwriting'])
            end = time.time()

            with open(LOGFILE, "a") as f:
                f.write(("%i,%i,%i,%i,%i,%i,%i,%i,%i,%i,%i,"
                         "%i,%i,%i,%i,%i,%i,%i,%i,%i,%i,%i\n") %
                        (data['formula_id'],
                         data['id'],
                         results[0]['formula_id']['formula_id'],
                         results[1]['formula_id']['formula_id'],
                         results[2]['formula_id']['formula_id'],
                         results[3]['formula_id']['formula_id'],
                         results[4]['formula_id']['formula_id'],
                         results[5]['formula_id']['formula_id'],
                         results[6]['formula_id']['formula_id'],
                         results[7]['formula_id']['formula_id'],
                         results[8]['formula_id']['formula_id'],
                         results[9]['formula_id']['formula_id'],
                         results[0]['formula_id']['handwriting'].raw_data_id,
                         results[1]['formula_id']['handwriting'].raw_data_id,
                         results[2]['formula_id']['handwriting'].raw_data_id,
                         results[3]['formula_id']['handwriting'].raw_data_id,
                         results[4]['formula_id']['handwriting'].raw_data_id,
                         results[5]['formula_id']['handwriting'].raw_data_id,
                         results[6]['formula_id']['handwriting'].raw_data_id,
                         results[7]['formula_id']['handwriting'].raw_data_id,
                         results[8]['formula_id']['handwriting'].raw_data_id,
                         results[9]['formula_id']['handwriting'].raw_data_id))

            ca[testset]['processed_datasets'] += 1
            ca[testset]['time'] += end - start

            if len(results) > 0:
                if results[0]['formula_id']['formula_id'] == data['formula_id']:
                    ca[testset]['correct'] += 1
                    ca[testset]['c10'] += 1
                else:
                    ca[testset]['wrong'] += 1

                    if data['formula_id'] in [r['formula_id']['formula_id']
                                              for r in results]:
                        ca[testset]['c10'] += 1
                    else:
                        ca[testset]['w10'] += 1
                        # logging.info(pp_results(results,
                        #                         data,
                        #                         formula_id2latex))
            else:
                logging.debug("No result for Raw-Data-ID: %i; Reality: %s\n" %
                              (data['id'],
                               formula_id2latex[data['formula_id']]))
                ca[testset]['wrong'] += 1
                ca[testset]['w10'] += 1

            if i % 100 == 0:
                logging.info(ca)
        print("\r100%"+"\033[K\n")
    return ca

if __name__ == '__main__':
    from argparse import ArgumentParser, ArgumentDefaultsHelpFormatter
    parser = ArgumentParser(description=__doc__,
                            formatter_class=ArgumentDefaultsHelpFormatter)
    parser.add_argument("-k", "--kfold", dest="kfold", type=int, default=10,
                        help="K Fold cross validation")
    parser.add_argument("-r", "--refresh", dest="refresh_dataset",
                        action="store_true", default=False,
                        help="refresh dataset")

    args = parser.parse_args()
    ca = main(args.kfold, args.refresh_dataset)
    print(ca)

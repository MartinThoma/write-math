#!/usr/bin/env python
"""
Display a raw_data_id.
"""

import os
import yaml
# mine
from HandwrittenData import HandwrittenData
import MySQLdb
import MySQLdb.cursors
import utils
import preprocessing
import features


def fetch_data(raw_data_id):
    """Get the data from raw_data_id from the server."""
    # Import configuration file
    cfg = utils.get_database_configuration()

    # Establish database connection
    connection = MySQLdb.connect(host=cfg[args.mysql]['host'],
                                 user=cfg[args.mysql]['user'],
                                 passwd=cfg[args.mysql]['passwd'],
                                 db=cfg[args.mysql]['db'],
                                 cursorclass=MySQLdb.cursors.DictCursor)
    cursor = connection.cursor()

    # Download dataset
    sql = ("SELECT `id`, `data` "
           "FROM `wm_raw_draw_data` WHERE `id`=%i") % args.id
    cursor.execute(sql)
    data = cursor.fetchone()
    return data


def display_data(raw_data_string, raw_data_id, model_folder):
    PROJECT_ROOT = utils.get_project_root()

    # Get model description
    model_description_file = os.path.join(model_folder, "info.yml")
    with open(model_description_file, 'r') as ymlfile:
        model_description = yaml.load(ymlfile)

    # Get the feature description
    feature_description_file = os.path.join(
        PROJECT_ROOT,
        model_description['data-source'],
        "info.yml")
    with open(feature_description_file, 'r') as ymlfile:
        feature_description = yaml.load(ymlfile)

    # Get the preprocessing description
    preprocessing_description_file = os.path.join(
        PROJECT_ROOT,
        feature_description['data-source'],
        "info.yml")
    with open(preprocessing_description_file, 'r') as ymlfile:
        preprocessing_description = yaml.load(ymlfile)

    # Get Handwriting
    a = HandwrittenData(raw_data_string, raw_data_id=raw_data_id)

    # Get the preprocessing queue
    tmp = preprocessing_description['queue']
    preprocessing_queue = preprocessing.get_preprocessing_queue(tmp)
    a.preprocessing(preprocessing_queue)

    tmp = feature_description['features']
    feature_list = features.get_features(tmp)
    x = a.feature_extraction(feature_list)
    t = [round(el, 3) for el in x]
    print(t)
    a.show()

if __name__ == '__main__':
    PROJECT_ROOT = utils.get_project_root()

    # Get latest model description file
    models_folder = os.path.join(PROJECT_ROOT, "archive/models")
    latest_model = utils.get_latest_in_folder(models_folder, ".yml")

    # Parse command line arguments
    from argparse import ArgumentParser
    parser = ArgumentParser(description=__doc__)
    parser.add_argument("-i", "--id", dest="id", default=279062,
                        type=int,
                        help="which RAW_DATA_ID do you want?")
    parser.add_argument("--mysql", dest="mysql", default='mysql_online',
                        help="which mysql configuration should be used?")
    parser.add_argument("-m", "--model",
                        dest="model",
                        help="where is the model folder (with a info.yml)?",
                        metavar="FOLDER",
                        type=lambda x: utils.is_valid_folder(parser, x),
                        default=latest_model)
    args = parser.parse_args()

    # do something
    data = fetch_data(args.id)
    if data is None:
        print("RAW_DATA_ID %i does not exist." % args.id)
    else:
        display_data(data['data'], data['id'], args.model)

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


def display_data(raw_data_string, raw_data_id):
    PROJECT_ROOT = utils.get_project_root()

    # Get latest model description file
    models_folder = os.path.join(PROJECT_ROOT, "archive/models")
    latest_model = utils.get_latest_in_folder(models_folder, ".yml")

    # Read the model description file
    with open(latest_model, 'r') as ymlfile:
        model_description = yaml.load(ymlfile)

    # Get the preprocessing queue
    preprocessing_queue = []
    print(model_description['preprocessing'])
    for el in model_description['preprocessing']:
        parameters = {}
        algorithms = el.keys()
        for algorithm in algorithms:
            parameters = {}
            if el[algorithm] is not None:
                for param in el[algorithm]:
                    for key in param.keys():
                        print(key)
                        parameters[key] = param[key]
            algorithm = preprocessing.get_algorithm(algorithm)
            preprocessing_queue.append((algorithm, parameters))

    a = HandwrittenData(raw_data_string, raw_data_id=raw_data_id)
    a.preprocessing(preprocessing_queue)
    a.show()

if __name__ == '__main__':
    from argparse import ArgumentParser
    parser = ArgumentParser(description=__doc__)
    parser.add_argument("-i", "--id", dest="id", default=279062,
                        type=int,
                        help="which RAW_DATA_ID do you want?")
    parser.add_argument("--mysql", dest="mysql", default='mysql_online',
                        help="which mysql configuration should be used?")
    args = parser.parse_args()

    data = fetch_data(args.id)
    if data is None:
        print("RAW_DATA_ID %i does not exist." % args.id)
    else:
        display_data(data['data'], data['id'])

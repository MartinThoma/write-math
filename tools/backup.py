#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
Download raw data from online server and back it up (e.g. on DropBox)
handwriting_datasets.pickle.
"""

import logging
import sys
import os
logging.basicConfig(format='%(asctime)s %(levelname)s %(message)s',
                    level=logging.INFO,
                    stream=sys.stdout)
try:  # Python 2
    import cPickle as pickle
except ImportError:  # Python 3
    import pickle
import pymysql
import pymysql.cursors
import dropbox
import hashlib
import webbrowser
import yaml
import time
import tempfile
import tarfile

# hwrt modules
from hwrt.HandwrittenData import HandwrittenData
from hwrt import filter_dataset
from hwrt import utils


def input_string(question=""):
    """A function that works for both, Python 2.x and Python 3.x.
       It asks the user for input and returns it as a string.

    Parameters
    ----------
    question : string
        The question displayed to the user asking for input.

    Returns
    -------
    string :
        The user input
    """
    if sys.version_info[0] == 2:
        return raw_input(question)
    else:
        return input(question)


def check_dropbox():
    """Check if the DropBox signin data is correct."""
    cfg = utils.get_project_configuration()
    if 'dropbox_app_key' not in cfg:
        logging.error("'dropbox_app_key' was not found.")
        return False
    elif 'dropbox_app_secret' not in cfg:
        logging.error("'dropbox_app_key' was not found.")
        return False
    else:
        return True


def dropbox_upload(filename, directory, client):
    """
    Upload the data to DropBox.

    Parameters
    ----------
    filename : string
        Name of the file that gets uploaded.
    directory : string
        Name of the directory in which the file is that gets uploaded (relativ
        to the project root)
    client :
        a DropBox client object
    """
    local_path = os.path.join(utils.get_project_root(), directory, filename)
    online_path = os.path.join(directory, filename)
    filesize = os.path.getsize(local_path)
    logging.info("Start uploading '%s' (%s)...",
                 filename,
                 utils.sizeof_fmt(filesize))
    with open(local_path, 'rb') as f:
        uploader = client.get_chunked_uploader(f, filesize)
        uploader.upload_chunked()
        uploader.finish(online_path, overwrite=True)
    url = client.share(online_path,
                       short_url=False)['url'].encode('ascii', 'ignore')
    url = url.replace("?dl=0", "?dl=1")
    return url


def sync_directory(directory):
    """Sync a directory. Return if syncing was successful."""
    # Developers should read
    # https://www.dropbox.com/developers/core/start/python
    # before modifying the following code
    cfg = utils.get_project_configuration()

    # Information about files in this folder
    project_root = utils.get_project_root()
    directory_information_file = os.path.join(project_root,
                                              directory, "info.yml")
    if not os.path.isfile(directory_information_file):  # create if not exists
        with open(directory_information_file, 'w') as ymlfile:
            ymlfile.write(yaml.dump([]))

    # Dropbox stuff
    APP_KEY = cfg['dropbox_app_key']
    APP_SECRET = cfg['dropbox_app_secret']

    flow = dropbox.client.DropboxOAuth2FlowNoRedirect(APP_KEY, APP_SECRET)
    authorize_url = flow.start()
    webbrowser.open_new_tab(authorize_url)
    print("1. Go to: " + authorize_url)
    print("2. Click 'Allow' (you might have to log in first)")
    print("3. Copy the authorization code.")
    access_token = input_string().strip()

    try:
        # This will fail if the user enters an invalid authorization code
        access_token, user_id = flow.finish(access_token)
        client = dropbox.client.DropboxClient(access_token)
    except Exception as e:
        logging.error("Dropbox connection error: %s", e)
        return False

    # Get all local files
    local_path = os.path.join(project_root, directory)
    files = [f for f in os.listdir(local_path)
             if os.path.isfile(os.path.join(local_path, f))]
    files = filter(lambda n: n.endswith(".pickle"), files)

    new_yaml_content = []

    # upload them
    for filename in files:
        file_meta = {}
        file_meta['filename'] = filename
        file_meta['online_path'] = os.path.join(directory, filename)
        local_path_file = os.path.join(local_path, filename)
        file_meta['md5'] = hashlib.md5(open(local_path_file,
                                            'rb').read()).hexdigest()
        new_yaml_content.append(file_meta)
        file_meta['url'] = dropbox_upload(filename, directory, client)
        if not file_meta['url']:
            return False

    # TODO: Remove all files from Dropbox that are not in local folder

    # Update YAML file
    with open(directory_information_file, 'w') as ymlfile:
        ymlfile.write(yaml.dump(new_yaml_content, default_flow_style=False))

    return True


def get_formulas(cursor, dataset='all'):
    """Get a list of formulas.

    Parameters
    ----------
    cursor : a database cursor
    dataset : string
        Either 'all' or a path to a yaml symbol file.

    Returns
    -------
    list :
        A list of formulas
    """
    if dataset == 'all':
        sql = ("SELECT `id`, `formula_in_latex` FROM `wm_formula` "
               "ORDER BY `id` ASC")
        cursor.execute(sql)
        formulas = cursor.fetchall()
    else:
        formulas = filter_dataset.get_symbol_ids(dataset,
                                                 filter_dataset.get_metadata())
    return formulas


def main(destination=os.path.join(utils.get_project_root(),
                                  "raw-datasets"),
         dataset='all',
         renderings=False):
    """Main part of the backup script."""
    time_prefix = time.strftime("%Y-%m-%d-%H-%M")
    filename = ("%s-handwriting_datasets-%s-raw.pickle" %
                (time_prefix, dataset.replace('/', '-')))
    destination_path = os.path.join(destination, filename)
    logging.info("Data will be written to '%s'", destination_path)

    cfg = utils.get_database_configuration()
    mysql = cfg['mysql_online']
    connection = pymysql.connect(host=mysql['host'],
                                 user=mysql['user'],
                                 passwd=mysql['passwd'],
                                 db=mysql['db'],
                                 cursorclass=pymysql.cursors.DictCursor)
    cursor = connection.cursor()

    formulas = get_formulas(cursor, dataset)
    logging.info('Received %i formulas.', len(formulas))
    handwriting_datasets = []
    formula_id2latex = {}

    # Go through each formula and download every raw_data instance
    for formula in formulas:
        formula_id2latex[formula['id']] = formula['formula_in_latex']
        sql = (("SELECT `wm_raw_draw_data`.`id`, `data`, `is_in_testset`, "
                "`wild_point_count`, `missing_line`, `user_id`, "
                "`display_name` "
                "FROM `wm_raw_draw_data` "
                "JOIN `wm_users` ON "
                "(`wm_users`.`id` = `wm_raw_draw_data`.`user_id`) "
                "WHERE `accepted_formula_id` = %s "
                # "AND `display_name` LIKE 'MfrDB::%%'"
                ) %
               str(formula['id']))
        cursor.execute(sql)
        raw_datasets = cursor.fetchall()
        logging.info("%s (%i)", formula['formula_in_latex'], len(raw_datasets))
        for raw_data in raw_datasets:
            try:
                handwriting = HandwrittenData(raw_data['data'],
                                              formula['id'],
                                              raw_data['id'],
                                              formula['formula_in_latex'],
                                              raw_data['wild_point_count'],
                                              raw_data['missing_line'],
                                              raw_data['user_id'],
                                              user_name=raw_data['display_name'])
                handwriting_datasets.append({'handwriting': handwriting,
                                             'id': raw_data['id'],
                                             'formula_id': formula['id'],
                                             'formula_in_latex':
                                             formula['formula_in_latex'],
                                             'is_in_testset':
                                             raw_data['is_in_testset']})
            except Exception as e:
                logging.info("Raw data id: %s", raw_data['id'])
                logging.info(e)
    pickle.dump({'handwriting_datasets': handwriting_datasets,
                 'formula_id2latex': formula_id2latex},
                open(destination_path, "wb"),
                2)

    if renderings:
        logging.info("Start downloading SVG renderings...")
        svgfolder = tempfile.mkdtemp()
        sql = """SELECT t1.formula_id, t1.svg from wm_renderings t1
                 LEFT JOIN wm_renderings t2 ON t1.formula_id = t2.formula_id
                 AND t1.creation_time < t2.creation_time
                 WHERE t2.id is null"""
        cursor.execute(sql)
        formulas = cursor.fetchall()
        logging.info("Create svg...")
        for formula in formulas:
            filename = os.path.join(svgfolder,
                                    "%s.svg" % str(formula['formula_id']))
            with open(filename, 'wb') as temp_file:
                temp_file.write(formula['svg'])
        logging.info("Tar at %s", os.path.abspath("renderings.tar"))

        tar = tarfile.open("renderings.tar.bz2", "w:bz2")
        for fn in os.listdir(svgfolder):
            filename = os.path.join(svgfolder, fn)
            if os.path.isfile(filename):
                print(filename)
                tar.add(filename, arcname=os.path.basename(filename))
        tar.close()


def get_parser():
    """Return the parser object for this script."""
    project_root = utils.get_project_root()
    archive_path = os.path.join(project_root, "raw-datasets")
    from argparse import ArgumentParser, ArgumentDefaultsHelpFormatter
    parser = ArgumentParser(description=__doc__,
                            formatter_class=ArgumentDefaultsHelpFormatter)
    parser.add_argument("-d", "--destination", dest="destination",
                        default=archive_path,
                        help="where to write the handwriting_dataset.pickle",
                        type=lambda x: utils.is_valid_folder(parser, x),
                        metavar="FOLDER")
    parser.add_argument("--dataset", dest="dataset",
                        default='all',
                        help=("of which symbols do you want the recordings?"))
    parser.add_argument("-r", "--renderings", dest="renderings",
                        action="store_true", default=False,
                        help=("should the svg renderings be downloaded?"))
    parser.add_argument("--dropbox", dest="dropbox",
                        action="store_true", default=False,
                        help=("upload to new files to DropBox"))
    return parser


if __name__ == '__main__':
    args = get_parser().parse_args()

    logging.info("Don't forget to run 'create_testset_online_once.py'.")

    if not check_dropbox():
        logging.error("Dropbox login data was not correct. "
                      "Please check your '~/.hwrtrc' file.")
    else:
        main(args.destination, args.dataset, args.renderings)
        if args.dropbox:
            return_value = sync_directory("raw-datasets")
            logging.info(("Successfully uploaded files to Dropbox. "
                          "Return value: %s"),
                         return_value)
        else:
            logging.info("Files were NOT uploaded to dropbox.")

#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""Find raw_datasets which are not accepted by the administrator and look
   different than other known datasets with the same accepted_formula_id.
"""
import sys
import logging
logging.basicConfig(level=logging.INFO,
                    stream=sys.stdout,
                    format='%(asctime)s %(levelname)s: %(message)s')
logger = logging.getLogger(__name__)

sys.path.append("/var/www/write-math/website/clients/python")
from HandwrittenData import HandwrittenData
# Database stuff
import MySQLdb
import MySQLdb.cursors

sys.path.append("/var/www/write-math/website/clients/dtw-python")
from classification import dtw

import preprocessing
import webbrowser
import yaml


def main(cfg):
    connection_local = MySQLdb.connect(host=cfg['mysql_online']['host'],
                                       user=cfg['mysql_online']['user'],
                                       passwd=cfg['mysql_online']['passwd'],
                                       db=cfg['mysql_online']['db'],
                                       cursorclass=MySQLdb.cursors.DictCursor)
    cursor_local = connection_local.cursor()
    with open("nopendown-2.txt") as f:
        content = f.read()
    for raw_data_id in content.split("\n"):
        print(raw_data_id)
        sql = ("UPDATE `wm_raw_draw_data` "
               "SET  `has_old_time_format` =  '1' "
               "WHERE  `wm_raw_draw_data`.`id` =%i LIMIT 1;") % \
              (int(raw_data_id))
        cursor_local.execute(sql)
    connection_local.commit()
    cursor_local.close()
    connection_local.close()

if __name__ == '__main__':
    with open("/var/www/write-math/website/clients/python/db.config.yml", 'r') as ymlfile:
        cfg = yaml.load(ymlfile)
    main(cfg)

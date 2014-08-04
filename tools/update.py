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

sys.path.append("../website/clients/python")
from HandwrittenData import HandwrittenData
import preprocessing
sys.path.append("../website/clients/dtw-python")
import yaml
# Database stuff
import MySQLdb
import MySQLdb.cursors


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
    from argparse import ArgumentParser
    parser = ArgumentParser(description=__doc__)
    args = parser.parse_args()
    with open("../website/clients/python/db.config.yml", 'r') as ymlfile:
        cfg = yaml.load(ymlfile)
    main(cfg)

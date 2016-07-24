#!/usr/bin/python

# This script was tested only on RHEL 5/6/7 with python 2.6 or higher.

import sqlite3
import os
import shutil

try:
    import json
except ImportError:
    import simplejson


for each in os.listdir('/appl/hadouken/json/'):
    if each.endswith('.json'):
        os.chdir(r'/appl/hadouken/json/')
        with open(each, 'r') as fp:
            hadouken = json.load(fp)
            db = sqlite3.connect('db.sqlite')
            cursor = db.cursor()
            cursor.execute(
                'INSERT INTO info(server_name,server_release,server_site,server_vendor,server_model,server_serial,'
                'server_cpu,server_memory,server_ip,server_cluster,server_clusternodes,server_frame,'
                'server_wwpn,server_db) VALUES(?,?,?,?,?,?,?,?,?,?,?,?,?,?)',
                (
                    hadouken['server_name'], hadouken['server_release'], hadouken['server_site'],
                    hadouken['server_vendor'],
                    hadouken['server_model'], hadouken['server_serial'], hadouken['server_cpu'],
                    hadouken['server_memory'],
                    hadouken['server_ip'], hadouken['server_cluster'], hadouken['server_clusternodes'],
                    hadouken['server_frame'], hadouken['server_wwpn'], hadouken['server_db']))
            db.commit()
            db.close()

            # move json file to out dir.
            infile = 'json/in/%s' % each
            outfile = 'json/out/%s' % each
            shutil.move(infile, outfile)
            
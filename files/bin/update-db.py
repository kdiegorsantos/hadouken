#!/usr/bin/python2

import os
import shutil
import sqlite3
import json

# all need files is in project directory.
my_project = '/etc/ansible/hadouken/files'

# find all json files and loads it on sqlite db.
for each in os.listdir('%s/json/' % my_project):
    if each.endswith('.json'):
        os.chdir(r'%s/json/' % my_project)
        with open(each) as fp:
            try:
                hadouken = json.load(fp)
                db = sqlite3.connect('%s/db/db.sqlite' % my_project)
                cursor = db.cursor()
                cursor.execute(
                    'INSERT OR IGNORE INTO info(server_name,server_release,server_site,server_vendor,server_model,'
                    'server_serial,server_cpu,server_memory,server_ip,server_cluster,server_clusternodes,server_frame,'
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

                infile = '%s/json/%s' % (my_project, each)
                outfile = '%s/tmp/%s' % (my_project, each)
                shutil.move(infile, outfile)
            
            # if we got an error loading the json print an error message. 
            except ValueError as e:
                print("Error loading %s" % each)
                continue

#!/usr/bin/python

# This script was tested only on RHEL 5/6/7 with python 2.6 or higher.

import platform
import subprocess

# checks if operating system is Linux.
if platform.system() == 'Linux':
    # call ansible-playbook
    proc = subprocess.Popen(
        ["/usr/bin/ansible-playbook -i /appl/hadouken/ansible/hosts /appl/hadouken/ansible/task.yml"],
        stdout=subprocess.PIPE, shell=True)
    x = proc.communicate()[0]

    # call hadoukendb.py to populate the sqlite3 db.
    proc = subprocess.Popen(
        ["/appl/hadouken/sbin/hadoukendb.py"],
        stdout=subprocess.PIPE, shell=True)
    x = proc.communicate()[0]

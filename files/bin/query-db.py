#!/usr/bin/python2.7

import sqlite3

#conn = sqlite3.connect('/etc/ansible/hadouken/files/db/db.sqlite')
conn = sqlite3.connect('/home/p1nk7/PycharmProjects/hadouken/files/db/db.sqlite')
cursor = conn.cursor()

cursor.execute("""
SELECT * FROM info;
""")

for row in cursor.fetchall():
    print(row)

conn.close()

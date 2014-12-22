__author__ = 'HartmannBlank'

import os
import psycopg2

connect = psycopg2.connect(database='database', user='username', host='host', password='password')
cursor = connect.cursor()
cursor.execute("DROP SCHEMA PUBLIC CASCADE;")
cursor.execute("CREATE SCHEMA PUBLIC;")
cursor.execute("CREATE TABLE directories(nest_id INT, id INT, parent_id INT, name TEXT);")

# Set the directory you want to start from
rootDir = 'c:\\folder'  # change to '.' for linux
base_list = (1, 1, 0, 'folder', 'c:\\')  # base in format  |how far from root|id|parent_id|name|
i = len(rootDir.split('\\'))

for dirName, subdirList, files in os.walk(rootDir):

    names = dirName.split('\\')
    full_path = dirName.split(names[-1])[0]
    # full path to current folder without current name, necessary for equivalent parent folder names occasion
    parent_index = base_list[base_list.index(full_path)-3]
    # shift back because of base format
    base_list += (len(names), i, parent_index, names[-1], dirName+'\\')
    sql_call = "INSERT INTO directories(nest_id, id, parent_id, name) VALUES ('%d', '%d', '%d', '%s');" \
                  % (base_list[-5], base_list[-4], base_list[-3], base_list[-2])
    cursor.execute(sql_call)
    connect.commit()
    i += 1
    names = []

"""
# show database and delete all tables from it

cursor.execute("SELECT * FROM directories;")
for row in cursor:
    print(row)
cursor.execute("drop schema public cascade;")
cursor.execute("create schema public;")
connect.close()
"""

#!/usr/bin/python3
#
# initial stuff by Cac Ko <email@gdpr_protected_stuff> 
# additional by <geroy@horizon9.org>
#
# import very large cvs-like file in postgre database
# 01.02.2019
#
# requires psycopg2 postgresql lib for python
# file format is:
# ----------------------------
# something12:otherthing2345
# something7134:otherthing4243
# .....
# License: Public Domain

import os
from time import sleep
import sys
import psycopg2
from psycopg2.extras import execute_values

# use file in tmpfs for faster read/write
POS_FILE = '/run/.position'

# get current position from POS_FILE location
def getPosition():
    result = 0
    if os.path.exists(POS_FILE):
        with open(POS_FILE, 'rb') as f:
            try:
                result = int(f.read())
                print("result = %d" % result)
            except Exception as error: 
                print("Error read():", error)
                result = 0
    return result

# write to this file after each commit()
def storePosition(pos):
    with open(POS_FILE, 'w') as f:
        f.write(str(pos))

# uncomment the following 3 lines if you want perentage / position on stdout
#    y = pos/whole*100
#    print('{0:.2f}%'.format(y), end = '')
#    print(" pos=%s" % (str(pos)))


# store stuff in database
def storeInDb(line, bulk_data):
#    print(line)
    x = []
    x = line.split(':')
    sql = b'INSERT into secrets (somestuff1, somestuff2) VALUES %s'
    try:
        execute_values(cur, sql, bulk_data)
        connection.commit()
    except Exception as error:
        print("Error pri INSERT", error)
        pass

if __name__ == '__main__':
    try:
        if len(sys.argv) < 2:
            print('usage: ./large-file-import.py filename-to-import.csv')
            exit
        f = open(sys.argv[1], 'r', buffering=2000000, errors='replace')
        whole = os.path.getsize(sys.argv[1])
        pos = getPosition()
        print("Start reading from pos=%d" % pos)
        f.seek(pos)
        line = f.readline()
        try:
            bulk_count = 0;
            connection = psycopg2.connect(
                user="postgres", password="somestuff", host="127.0.0.1", port="5433", database="postgres")
            cur = connection.cursor()
            bulk_data = []
            split_line = []
            while line:
                
                split_line = line.split(':')
                try:
                    l = tuple(split_line)
                    bulk_data.append(l)
                except (Exception) as error:
                    print(error)
                    pass
                
                storePosition(f.tell())
                line = f.readline()
                bulk_count = bulk_count + 1
                # store and commit in db after X lines
                if bulk_count == 9000:
                    storeInDb(line,bulk_data)
                    bulk_count = 0;
                    bulk_data = []

                #connection.commit()
        except (Exception, psycopg2.Error) as error:
            print("Error while connecting to PostgreSQL", error)
        finally:
            if(connection):
                cur.close()
                connection.close()
                print("PostgreSQL connection is closed")

    except KeyboardInterrupt:
        storePosition(f.tell())
        if(connection):
            cur.close()
            connection.close()
            print("PostgreSQL connection is closed")

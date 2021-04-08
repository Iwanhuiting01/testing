#!/usr/bin/python

import sqlite3

conn = sqlite3.connect('music.sqlite')

Forbidden = conn.execute("SELECT * FROM songs "
                    "INNER JOIN albums "
                    "ON songs.album = albums._id "
                    "WHERE albums.name = 'Forbidden'"
                    "ORDER BY songs.track ASC")

DeepPurple = conn.execute("SELECT * FROM songs "
                    "INNER JOIN albums "
                    "ON songs.album = albums._id "
                    "WHERE albums.name = 'Forbidden'"
                    "ORDER BY songs.track ASC")

for row in Forbidden:
    print(row)

conn.close()


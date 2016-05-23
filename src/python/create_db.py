#!/usr/bin/python
# -*- coding: utf-8 -*-

import sqlite3

conn = sqlite3.connect('temperature.db')

c = conn.cursor()

c.execute('DROP TABLE temperature')

# Create table
c.execute('''create table temperature
             (ts timestamp, id integer, value real)''')

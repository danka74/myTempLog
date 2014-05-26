#!/usr/bin/python
# -*- coding: utf-8 -*-

import tellcore.telldus as td
import tellcore.constants as const

import MySQLdb as mdb
import sys

tdCore = td.TelldusCore()

try:
    con = mdb.connect('192.168.1.100', 'tempuser', 'App3lKnyckar1azz', 'tempdb');

    cur = con.cursor()

    for sensor in tdCore.sensors():
	value = sensor.value(const.TELLSTICK_TEMPERATURE)
	print value
        cur.execute("INSERT INTO temperature VALUES (NOW(), %s, %s);", (sensor.id, value))

    con.commit()
    
except mdb.Error, e:

    con.rollback()
  
    print "Error %d: %s" % (e.args[0],e.args[1])
    sys.exit(1)
    
finally:    
        
    if con:    
        con.close()

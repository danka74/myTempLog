#!/usr/bin/python
# -*- coding: utf-8 -*-

import tellcore.telldus as td
import tellcore.constants as const

import MySQLdb as mdb
import sys

import time

def format_value(sensor, datatype, formatter):
        if not sensor.has_value(datatype):
            return ("", None)
        value = sensor.value(datatype)
        return (formatter(value.value), value.timestamp)

tdCore = td.TelldusCore()

try:
    con = mdb.connect('192.168.1.100', 'tempuser', 'App3lKnyckar1azz', 'tempdb');

    cur = con.cursor()

    for sensor in tdCore.sensors():
	value = format_value(sensor, const.TELLSTICK_TEMPERATURE, lambda x: "{}".format(x))
	print "{} at {}".format(value[0], time.ctime(value[1]))
        cur.execute("INSERT INTO temperature VALUES (FROM_UNIXTIME(%s), %s, %s);", (value[1], sensor.id, value[0]))

    con.commit()
    
except mdb.Error, e:

    con.rollback()
  
    print "Error %d: %s" % (e.args[0],e.args[1])
    sys.exit(1)
    
finally:    
        
    if con:    
        con.close()

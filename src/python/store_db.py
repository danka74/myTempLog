#!/usr/bin/python
# -*- coding: utf-8 -*-

import tellcore.telldus as td
import tellcore.constants as const

import MySQLdb as mdb
import sys

import time

core = td.TelldusCore()
impossible_value = -300
prev_values = {}

while True:
	
	sensors = core.sensors()
	
	time.sleep(60)

	try:
	    con = mdb.connect('192.168.1.100', 'tempuser', 'App3lKnyckar1azz', 'tempdb');
	
	    cur = con.cursor()
	
	    for sensor in sensors:
		value = sensor.value(const.TELLSTICK_TEMPERATURE)
		print "{} at {}".format(value.value, time.ctime(value.timestamp))
		if abs(value.value - prev_values.get(sensor.id, impossible_value)) > 0.5:
	        	cur.execute("INSERT INTO temperature VALUES (FROM_UNIXTIME(%s), %s, %s);", (value.timestamp, sensor.id, value.value))
	        	prev_values[sensor.id] = value.value
	
	    con.commit()

	except mdb.Error, e:
	
	    con.rollback()
	  
	    print "Error %d: %s" % (e.args[0],e.args[1])
	    sys.exit(1)
	    
	finally:    
	        
	    if con:    
	        con.close()

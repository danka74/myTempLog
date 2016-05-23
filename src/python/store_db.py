#!/usr/bin/python
# -*- coding: utf-8 -*-

import tellcore.telldus as td
import tellcore.constants as const

import sqlite3
import sys

import time

core = td.TelldusCore()
impossible_value = -300.0
prev_values = {}

while True:
	
	sensors = core.sensors()
	
	try:
		con = sqlite3.connect('temperature.db');
	
		cur = con.cursor()
	
		for sensor in sensors:
			value = sensor.value(const.TELLSTICK_TEMPERATURE)
			print "{} at {}".format(value.value, time.ctime(value.timestamp))
			if abs(float(value.value) - prev_values.get(sensor.id, impossible_value)) >= 0.5:
				print "stored!"
				cur.execute("INSERT INTO temperature VALUES (?, ?, ?);", (value.timestamp, sensor.id, value.value))
				prev_values[sensor.id] = float(value.value)
	
		con.commit()

	except sqlite3.Error, e:
	
		con.rollback()
		print "Error %d: %s" % (e.args[0], e.args[1])
		sys.exit(1)
		
	finally:    
		if con:
			con.close()

	time.sleep(60)

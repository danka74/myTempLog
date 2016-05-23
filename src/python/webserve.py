#!/usr/bin/python3
'''
Created on May 29, 2014

@author: daniel
'''
from bottle import HTTPError, template, route, run, response
import bottle
import bottle.ext.sqlite

import pygal
from pygal.style import LightSolarizedStyle

import datetime

app = bottle.Bottle()
# dbhost is optional, default is localhost
plugin = bottle.ext.sqlite.Plugin(dbfile='temperature.db')
#plugin = bottle_mysql.Plugin(dbhost='192.168.1.100', dbuser='tempuser', dbpass='App3lKnyckar1azz', dbname='tempdb', keyword='db')
app.install(plugin)

@app.route('/hello/<name>')
def index(name):
    return template('<b>Hello {{name}}</b>!', name=name)

@app.route('/sensors')
def sensors( db):
    rows = db.execute('SELECT DISTINCT id FROM temperature;')
    #rows = db.fetchall()
    return template('sensors', rows=rows)
    
@app.route('/now/<sensorid>')
def now(sensorid, db):
    cur = db.execute('SELECT * FROM temperature WHERE id=? ORDER BY ts DESC LIMIT 1', (sensorid,))
    row = cur.fetchone()
    if row:
        return template('current_temp', temp=row[2], id=row[1], timestamp=datetime.datetime.fromtimestamp(row[0]).strftime('%Y-%m-%d %H:%M:%S'))
    return HTTPError(404, "Page not found")

@app.route('/last24/<sensorid>')
def last24(sensorid, db):
    rows = db.execute('SELECT * FROM temperature WHERE id=? AND datetime(ts) > datetime("now", "-1 day")', (sensorid,))

    if rows:
        return template('day_table', rows=rows)
    return HTTPError(404, "Page not found")

@app.route('/last24svg/<sensorid>')
def last24svg(sensorid, db):
    rows = db.execute('SELECT ts, value FROM temperature WHERE id=? AND datetime(ts) > datetime("now", "-1 day")', (sensorid,))
    if not rows:
        return HTTPError(404, "Page not found")
    response.content_type = 'image/svg+xml'
    
    data = []
    for row in rows:
        data.append((datetime.datetime.fromtimestamp(row[0]), row[1]))
                    

    print data

    dia = pygal.DateY(x_label_rotation=20, style=LightSolarizedStyle)
    dia.x_label_format = "%a %H:%M"
    dia.add("Sensor {}".format(sensorid), data)
    return dia.render()    

if __name__=='__main__':
    app.run(host='0.0.0.0', port=8080, debug=True)

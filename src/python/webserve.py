#!/usr/bin/python3
'''
Created on May 29, 2014

@author: daniel
'''
from bottle import HTTPError, template, route, run, response
import bottle 
import bottle_mysql

import pygal
from pygal.style import LightSolarizedStyle


app = bottle.Bottle()
# dbhost is optional, default is localhost
plugin = bottle_mysql.Plugin(dbhost='192.168.1.100', dbuser='tempuser', dbpass='App3lKnyckar1azz', dbname='tempdb', keyword='db')
app.install(plugin)

@app.route('/hello/<name>')
def index(name):
    return template('<b>Hello {{name}}</b>!', name=name)

@app.route('/now/<sensorid>')
def now(sensorid, db):
    db.execute('SELECT * FROM temperature WHERE id={} ORDER BY timestamp DESC LIMIT 1;'.format(sensorid))
    row = db.fetchone()
    if row:
        return template('current_temp', temp=row['value'], id=row['id'], timestamp=row['timestamp'])
    return HTTPError(404, "Page not found")

@app.route('/last24/<sensorid>')
def last24(sensorid, db):
    db.execute('SELECT * FROM temperature WHERE id={} AND timestamp > (NOW() - INTERVAL 1 DAY);'.format(sensorid))
    rows = db.fetchall()
    if rows:
        return template('day_table', rows=rows)
    return HTTPError(404, "Page not found")

@app.route('/last24svg/<sensorid>')
def last24svg(sensorid, db):
    db.execute('SELECT timestamp, value FROM temperature WHERE id={} AND timestamp > (NOW() - INTERVAL 1 DAY);'.format(sensorid))
    rows = db.fetchall()
    if not rows:
        return HTTPError(404, "Page not found")
    response.content_type = 'image/svg+xml'
    
    data = []
    for row in rows:
        data.append((row['timestamp'], row['value']))
                    
    dia = pygal.DateY(x_label_rotation=20, style=LightSolarizedStyle)
    dia.x_label_format = "%a %H:%M"
    dia.add("Sensor {}".format(sensorid), data)
    return dia.render()    

if __name__=='__main__':
    app.run(host='0.0.0.0', port=8080, debug=True)
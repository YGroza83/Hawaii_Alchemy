from flask import Flask, jsonify
import numpy as np
import sqlalchemy
from sqlalchemy.ext.automap import automap_base
from sqlalchemy.orm import Session
from sqlalchemy import create_engine, func
engine = create_engine("sqlite:///hawaii.sqlite")
Base = automap_base()
Base.prepare(engine, reflect=True)
Mesurement = Base.classes.measurement
Station = Base.classes.station
app = Flask(__name__)
@app.route("/")
def home():
    return """Valid API calls: <br>     /<br>     /api/v1.0/precipitation<br>     /api/v1.0/stations<br>
     /api/v1.0/tobs<br>     /api/v1.0/start<br>     /api/v1.0/start/end"""
@app.route("/api/v1.0/precipitation")
def perc():
    session = Session(engine)
    results = session.query(Mesurement.date,Mesurement.prcp).filter(Mesurement.date > '2016-08-23')
    session.close()
    all_mesurements = dict(results)
    return jsonify(all_mesurements)
@app.route("/api/v1.0/stations")
def stat():
    session = Session(engine)
    results = session.query(Station.id,Station.name,Station.station).all()
    session.close()
    all_stations = list(results)
    return jsonify(all_stations)
@app.route("/api/v1.0/tobs")
def tobs():
    session = Session(engine)
    results = session.query(Mesurement.date,Mesurement.tobs).filter(Mesurement.station == 'USC00519281', Mesurement.date > '2016-08-23')
    session.close()
    all_mesurements = list(results)
    return jsonify(all_mesurements)   
@app.route("/api/v1.0/<start>")
@app.route("/api/v1.0/<start>/<end>")
def get_temps(start, end = '2017-08-23'):
    session = Session(engine)
    results = session.query(func.min(Mesurement.tobs),func.avg(Mesurement.tobs),func.max(Mesurement.tobs)).filter(Mesurement.date >= start, Mesurement.date <= end)
    session.close()
    minmax_mesurements = list(results)
    return jsonify(minmax_mesurements)
if __name__ == "__main__":
    app.run(debug=True)
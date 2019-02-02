from flask import Flask, jsonify
import datetime as dt
import numpy as np

import sqlalchemy
from sqlalchemy.ext.automap import automap_base
from sqlalchemy.orm import Session
from sqlalchemy import create_engine, func, inspect

engine= create_engine("sqlite:///Resources/hawaii.sqlite")
base = automap_base()
base.prepare(engine, reflect=True)
session = session(engine)

Measurement = base.classes.Measurement
Station = base.classes.Measurement

app = Flask(__name__)

@app.route("/")
def home():
    print("Server received request for 'Home' page....")
    return(
        f"Wecome to the 'Home' page<br/>"
        f"Available Routes: <br/>"
        f"/api/v1.0/precipitation<br/>"
        f"/api/v1.0/stations<br/>"
        f"/api/v1.0/tobs<br/>"
        f"/api/v1.0/<start><br/>"
        f"/api/v1.0/<start>/<end><br/>"
    )

@app.route("/api/v1.0/precipitation")
def precipitation():
    """Return a list of all precipitation"""

    year_ago = dt.date(2017,8,23) - dt.timedelta(days=365)

    annualprecip = session.query(Measurement.date, Measurement.prcp).\
                    filter(Measurement.date >= year_ago).all()
    precip ={date: prcp for date, prcp in annualprecip}
    return jsonify(precip)

@app.route("/api/v1.0/stations")
def stations():
    """Returns a list of all stations"""
    results = session.query(Station.station).all()

    all_stations = list(np.ravel(results))

    return jsonify(all_stations)

@app.route("/api/v1.0/tobs")
def tobs():
   """Returns a list of the dates and temperature observations from a year from last data point"""
   year_ago = dt.date(2017,8,23) - dt.timedelta(days=365)

   annual_temps = session.query(Measurement.tobs).\
                   filter(Measurement.station == 'USC00519281').\
                   filter(Measurement.date >= year_ago).all()


   temps = list(np.ravel(annual_temps))

   return jsonify(temps)


@app.route("/api/v1.0/<start>")
def start_temp(start):
    results = session.query(func.min(Measurement.tobs), func.avg(Measurement.tobs), func.max(Measurement.tobs)).\
        filter(Measurement.date >= start).all()
    return jsonify(results)

@app.route("/api/v1.0/<start>/<end>")
def start_end_temp(start,end):
    results = session.query(func.min(Measurement.tobs), func.avg(Measurement.tobs), func.max(Measurement.tobs)).\
        filter(Measurement.date >= start).\
        filter(Measurement.date <= end).all()
    return jsonify(results)


if __name__ == "__main__":
    app.run(debug=True)
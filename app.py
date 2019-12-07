# 1. import Flask
from flask import Flask, jsonify
import sqlalchemy
from sqlalchemy.ext.automap import automap_base
from sqlalchemy.orm import Session
from sqlalchemy import create_engine, func, inspect
import numpy as np
import pandas as pd
import datetime as dt
from datetime import date

engine = create_engine("sqlite:///Resources/hawaii.sqlite")

# reflect an existing database into a new model
Base = automap_base()
# reflect the tables
Base.prepare(engine, reflect=True)

# Save references to each table
Measurement = Base.classes.measurement
Station = Base.classes.station




#Create an app, being sure to pass __name__
app = Flask(__name__)


#Define what to do when a user hits the index route
@app.route("/")
def home():
    """List all available api routes."""
    return (
        f"Available Routes:<br/>"
        f"/api/v1.0/stations<br/>"
        f"/api/v1.0/tobs<br/>"
        f"/api/v1.0/start<br/>"
        f"/api/v1.0/start/end<br/>"
    )


#Define what to do when a user hits the /stations route
@app.route("/api/v1.0/stations")
def stations():
    # Create our session (link) from Python to the DB
    session = Session(engine)
    result = session.query(Station.station).all()
    session.close()

    return jsonify(result)

#Define what to do when a user hits the /tobs route
@app.route("/api/v1.0/tobs")
def tobs():
    # Create our session (link) from Python to the DB
    session = Session(engine)
    ##get max date from measurement
    result = engine.execute('SELECT max(date) as date FROM measurement').fetchall()
    max_date = date.fromisoformat(result[0]['date'])

    ##calculate start date (i.e. 12 months prior)
    start_date = max_date - dt.timedelta(days=365)

    result = session.query(Measurement.date, Measurement.prcp).filter(Measurement.date >= start_date).all()

    session.close()

    return jsonify(result)

#Define what to do when a user hits the /start/end route
@app.route("/api/v1.0/start/<start>/end/<end>")
def calc_temp2(start, end):
    # Create our session (link) from Python to the DB
    session = Session(engine)
    ##get max date from measurement
    
    result =  session.query(func.min(Measurement.tobs), func.avg(Measurement.tobs), func.max(Measurement.tobs)).\
        filter(Measurement.date >= start).filter(Measurement.date <= end).all()

    session.close()

    return jsonify(result)

#Define what to do when a user hits the /start route
@app.route("/api/v1.0/start/<start>")
def calc_temp1(start):
    # Create our session (link) from Python to the DB
    session = Session(engine)
    ##get max date from measurement

    return calc_temp2(start, '9999-01-01')


if __name__ == "__main__":
    app.run(debug=True)
 
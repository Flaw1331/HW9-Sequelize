# Imports
import datetime as dt
import numpy as np
import pandas as pd

import sqlalchemy
from sqlalchemy.ext.automap import automap_base
from sqlalchemy.orm import Session
from sqlalchemy import create_engine, func

from flask import Flask, jsonify


# DataBase Setup
engine = create_engine("sqlite:///hawaii.sqlite")

Base = automap_base()
Base.prepare(engine, reflect=True)

Measurement = Base.classes.measurements
Station = Base.classes.stations

session = Session(engine)



# Flask Setup
app = Flask(__name__)



# Routes

# Precip Route
@app.route("/api/v1.0/precipitation")
def precipitation():
    results = session.query(Measurement.date, Measurement.prcp) \
                    .filter(Measurement.date >= '2016-08-23')\
                    .order_by(Measurement.date.desc()).all()
    stations_dict = {}
    for x in results:                    
        stations_dict.update({x[0]: x[1]})
    return jsonify(stations_dict)

# Stations Route
@app.route("/api/v1.0/stations")
def stations():
    results = session.query(Measurement.station).group_by(Measurement.station).all()
    all_names = list(np.ravel(results))
    return jsonify(all_names)

# Tobs Route
@app.route("/api/v1.0/tobs")
def tobs():
    results = session.query(Measurement.date, Measurement.tobs) \
                    .filter(Measurement.date >= '2016-08-23')\
                    .order_by(Measurement.date.desc()).all()
    temps = list(np.ravel(results))
    return jsonify(temps)
    #return jsonify(results)

# Start Route
@app.route("/api/v1.0/<start>")
def start_date(start):
    results = session.query(Measurement.date, Measurement.tobs) \
                    .filter(Measurement.date >= start)
    temps_df = pd.DataFrame(results[::], columns=['date','temp'])
    min_temp = temps_df['temp'].min()
    max_temp = temps_df['temp'].max()
    avg_temp = temps_df['temp'].mean()
    return ('min_temp = ' + str(min_temp) + '\n' + 'max_temp = ' + str(max_temp) + '\n' + 'avg_temp = ' + str(avg_temp))

# End Route
@app.route("/api/v1.0/<start>/<end>")
def start_end_date(start, end):
    results = session.query(Measurement.date, Measurement.tobs) \
                    .filter((Measurement.date >= start), (Measurement.date <= end))
    temps_df = pd.DataFrame(results[::], columns=['date','temp'])
    min_temp = temps_df['temp'].min()
    max_temp = temps_df['temp'].max()
    avg_temp = temps_df['temp'].mean()
    return ('min_temp = ' + str(min_temp) + '\n' + 'max_temp = ' + str(max_temp) + '\n' + 'avg_temp = ' + str(avg_temp))





# Debug to run - False when deploy
if __name__ == '__main__':
    app.run(debug=True)
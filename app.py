import numpy as np 
import datetime as dt 
import sqlalchemy
from sqlalchemy.ext.automap import automap_base
from sqlalchemy.orm import Session
from sqlalchemy import create_engine, func

from flask import Flask, jsonify

# Create app
app = Flask(__name__)

# Create engine
engine = create_engine("sqlite:///Resources/hawaii.sqlite")

# Create Base
Base = automap_base()

# Reflect database on new model
Base.prepare(engine, reflect = True)

# Save reference to tables
Measurement = Base.classes.measurement 
Station = Base.classes.station 

# Create home page routes
@app.route('/')
def home():
    home = f"""
    Welcome to the Hawaii Weather Data Home Page!</br>
    </br>
    Check out these links:</br>
    <a href='/api/v1.0/stations'>All Station IDs</a></br>
    <a href='/api/v1.0/precipitation'>All Precipitation Data by Date</a></br>
    <a href='/api/v1.0/tobs'>Last Year of Temperature data for Station USC00519281</a>
    """
    return home

# station api
@app.route('/api/v1.0/stations')
def station():
    
    # Start Session
    session = Session(engine)

    # Query for all stations
    station_query = session.query(Station.station).all()

    # Close Session
    session.close()

    # Make a list of all the stations
    all_stations = list(np.ravel(station_query))

    # jsonify the list of stations
    return jsonify(all_stations)

# precipitation api
@app.route('/api/v1.0/precipitation')
def precipitation():
    
    # Start Session
    session = Session(engine)

    # Query precipitation for each date
    precip_query = session.query(Measurement.date, Measurement.prcp).all()

    # Close Session
    session.close()

    # Create a precip list to append in the for loop
    precip_list = []

    # Create a For Loop to create a dictionary to append and jsonify (Thanks Luis!)
    for date, prcp in precip_query:
        precip_dict = {}
        precip_dict.update({date: prcp})
        precip_list.append(precip_dict)

    # jsonify the dictionary of precip dates
    return jsonify(precip_list)

# temperature api
@app.route('/api/v1.0/tobs')
def temperature():
    
    # Start Session
    session = Session(engine)

    # Query temperature for each date
    temp_query = session.query(Measurement.station, Measurement.date, Measurement.tobs).\
        filter(Measurement.station == 'USC00519281', Measurement.date >='2016-08-23').all()

    # Close Session
    session.close()

    # Create a Temp list
    temp_list = []

    # Create a For Loop to identify all the Temp data for station USC00519281 and append it to the temp list to jsonify
    for temp in temp_query:
        temperature = temp[2]
        temp_list.append(temperature)

    # jsonify the list of temps for station USC00519281
    return jsonify(temp_list)

if __name__ == '__main__':
    app.run(debug=True)
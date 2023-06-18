# Import the dependencies.
import numpy as np

import sqlalchemy
from sqlalchemy.ext.automap import automap_base
from sqlalchemy.orm import Session
from sqlalchemy import create_engine, func

from flask import Flask, jsonify


#################################################
# Database Setup
#################################################
engine = create_engine("sqlite:///../Resources/hawaii.sqlite")

# reflect an existing database into a new model
Base = automap_base()

# reflect the tables
Base.prepare(autoload_with=engine)

# Save references to each table
station = Base.classes.station
measurement = Base.classes.measurement

# Create our session (link) from Python to the DB
session = Session(engine)

#################################################
# Flask Setup
#################################################
app = Flask(__name__)



#################################################
# Flask Routes
#################################################

@app.route("/")
def welcome():
    """List all available routes."""
    return (
        f"Available Routes: <br/>"
        f"/api/v1.0/precipitation <br/>"
        f"/api/v1.0/stations <br/>"
        f"/api/v1.0/tobs <br/>"
        f"/api/v1.0/&ltstart&gt <br/>"
        f"/api/v1.0/&ltstart&gt/&ltend&gt"
    )

@app.route("/api/v1.0/precipitation")
def precipitation():
    """Get precipitation data from last 12 months and convert to a dictionary. Return a json"""
    return (
        
    )

@app.route("/api/v1.0/stations")
def stations():
    """Return a json list of stations from the dataset"""
    return (
        
    )

@app.route("/api/v1.0/tobs")
def tobs():
    """Query the dates and temperature of the most-active station for the previous year of data"""
    return (

    )

@app.route("/api/v1.0/<start>")
def temp_start():
    """Return a json list of min, mean, and max for a specified start time til end of data"""
    return (
    )

@app.route("/api/v1.0/<start>/<end>")
def temp_start_end():
    """Return a json list of min, mean, and max for a specified date range"""
    return (
    )


if __name__ == '__main__':
    app.run(debug = True)
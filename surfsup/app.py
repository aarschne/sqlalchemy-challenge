# Import the dependencies.
import numpy as np
import sqlalchemy
from sqlalchemy.ext.automap import automap_base
from sqlalchemy.orm import Session
from sqlalchemy import create_engine, func
from flask import Flask, jsonify
from datetime import datetime, timedelta


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

# Find the most recent date in the data set.
most_recent_date = session.query(measurement.date)\
                        .order_by(measurement.date.desc()).first()[0]
    
# Calculate the date one year from the last date in data set.
most_recent_date = datetime.strptime(most_recent_date, '%Y-%m-%d').date()
year_before_most_recent = most_recent_date - timedelta(days = 365)

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

    # Create our session (link) from Python to the DB
    session = Session(engine)

    

    # Perform a query to retrieve the data and precipitation scores
    results = session.query(measurement) \
        .with_entities(measurement.station, measurement.date, measurement.prcp) \
        .filter(measurement.date >= year_before_most_recent)

    session.close()

    precipation_dict = {}

    for station, date, precip in results:
        precipation_dict[date] = precip

    return (
        jsonify(precipation_dict)
    )

@app.route("/api/v1.0/stations")
def stations():
    """Return a json list of stations from the dataset"""

    # Create our session (link) from Python to the DB
    session = Session(engine)

    station_list = session.query(measurement.station).distinct().all()

    results = [tuple(row)[0] for row in station_list]

    session.close()

    return (
        jsonify(results)
    )

@app.route("/api/v1.0/tobs")
def tobs():
    """Query the dates and temperature of the most-active station for the previous year of data"""

    # Create our session (link) from Python to the DB
    session = Session(engine)

    # Design a query to find the most active stations (i.e. which stations have the most rows?)
    # List the stations and their counts in descending order.

    query_station = sqlalchemy.select([measurement.station,
                            sqlalchemy.func.count(measurement.station)
                          ]) \
                        .group_by(measurement.station) \
                        .order_by(func.count(measurement.station).desc())

    result = engine.execute(query_station).fetchall()

    # save the most active station
    most_active_station = result[0][0]

    # find temperature data for the last year of data for the most active station
    query_most_active = session.query(measurement) \
        .with_entities(measurement.tobs) \
        .filter(measurement.station == most_active_station) \
        .filter(measurement.date >= year_before_most_recent)

    # make a list of temperature for most active station
    most_active_temp = []

    for record in query_most_active:
        most_active_temp.append(tuple(record)[0])

    session.close()

    return (
        jsonify(most_active_temp)
    )

@app.route("/api/v1.0/<start>")
def temp_start(start):
    """Return a json list of min, mean, and max for a specified start time til end of data"""

    # Create our session (link) from Python to the DB
    session = Session(engine)

    query = session.query(measurement) \
        .with_entities(measurement.tobs) \
        .filter(measurement.date >= start)

    session.close()

    # filter out null values and make a list of temperatures
    temperatures = []

    for record in query:
        if type(record.tobs) == float:
            temperatures.append(record.tobs)

    # find statistics for the list of temperatures
    lowest_temp = min(temperatures)
    highest_temp = max(temperatures)
    mean_temp = np.mean(temperatures)

    # make return dict
    return_dict = {}
    return_dict["Lowest temperature"] = lowest_temp
    return_dict["Highest temperature"] = highest_temp
    return_dict["Average temperature"] = mean_temp

    return (
        jsonify(return_dict)
    )

@app.route("/api/v1.0/<start>/<end>")
def temp_start_end(start,end):
    """Return a json list of min, mean, and max for a specified date range"""

    # Create our session (link) from Python to the DB
    session = Session(engine)

    query = session.query(measurement) \
        .with_entities(measurement.tobs) \
        .filter(measurement.date >= start) \
        .filter(measurement.date <= end)

    session.close()

    # filter out null values and make a list of temperatures
    temperatures = []

    for record in query:
        if type(record.tobs) == float:
            temperatures.append(record.tobs)

    # find statistics for the list of temperatures
    lowest_temp = min(temperatures)
    highest_temp = max(temperatures)
    mean_temp = np.mean(temperatures)

    # make return dict
    return_dict = {}
    return_dict["Lowest temperature"] = lowest_temp
    return_dict["Highest temperature"] = highest_temp
    return_dict["Average temperature"] = mean_temp

    return (
        jsonify(return_dict)
    )


if __name__ == '__main__':
    app.run(debug = True)
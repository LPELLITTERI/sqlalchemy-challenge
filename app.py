import numpy as np

import sqlalchemy
from sqlalchemy.ext.automap import automap_base
from sqlalchemy.orm import Session
from sqlalchemy import create_engine, func
from flask import Flask, jsonify

#################################################
# Database Setup
#################################################
engine = create_engine("sqlite:///hawaii.sqlite")


# reflect an existing database into a new model
Base = automap_base()

# reflect the tables
Base.prepare(autoload_with=engine)

# View all of the classes that automap found
Base.classes.keys()

# Save reference to the table
Measurement = Base.classes.measurement

Station = Base.classes.station

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
    """List all available api routes."""
    return (
        f"Available Routes:<br/>"
    )


#query results from precipiation analysis only last 12 months
@app.route('/api/v1.0/precipitation')
def precipitation():
    session = Session()
    prcp = session.query(Measurement.date, Measurement.prcp).filter(Measurement.date >= '2016-08-23').all()
    session.close()
    
    prcp_dict = {}
    for date, prcp in prcp:
        prcp_dict[date] = prcp
    
    return jsonify(prcp_dict)



#Return a JSON list of stations from the dataset
@app.route('/api/v1.0/stations')
def stations():
    session = Session()
    station = session.query(Station.station).all()
    session.close()

    stations_list = list(np.travel(results))
    return jsonify(stations_list)


#Query the dates and temperature observations of the most-active station for the previous year of data.
#Return a JSON list of temperature observations for the previous year.
@app.route('/api/v1.0/tobs')
def most_active():
    session = Session()
    most_active = session.query(Measurement.station, func.count(Measurement.station)).\
              group_by(Measurement.station).\
              order_by(func.count(Measurement.station).desc()).all()
    session.close()

# Select the station with the highest number of temperature observations
    most_active_station = most_active[0][0]

# Query the most active station's temperature data for the previous year
    temps_last_year = session.query(Measurement.tobs).\
                      filter(Measurement.station == most_active_station).\
                      filter(Measurement.date >= '2016-08-23').all()

# Convert the query results to a list
    temps_list = list(np.ravel(temps_last_year))

    # Return the JSON representation of the list
    return jsonify(temps_list)


    session.close()


if __name__ == '__main__':
    app.run()


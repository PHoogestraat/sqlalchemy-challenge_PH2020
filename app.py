
########## SQL Alcehemy Homework API
####  Import Dependencies

import numpy as np
import sqlalchemy
from sqlalchemy.ext.automap import automap_base
from sqlalchemy.orm import Session
from sqlalchemy import create_engine, func
import datetime as dt
from flask import Flask, jsonify


#################################################
# Database Setup
#################################################
engine = create_engine("sqlite:///Resources/hawaii.sqlite")

# reflect an existing database into a new model
Base = automap_base()
# reflect the tables
Base.prepare(engine, reflect=True)
#### Save reference to the table
######### Map Station class
STAT = Base.classes.station
MEASUR = Base.classes.measurement


#################################################
# Flask Setup
#################################################
app = Flask(__name__)

#################################################
# Flask Routes
#################################################

@app.route("/api/v1.0/precipitation")
def precip():
    # Create our session (link) from Python to the DB
    session = Session(bind=engine)
    """Return precipitation data"""
    # Query for last day and first day on new data set
    query_date = dt.date(2017, 8, 23) - dt.timedelta(days=365)
    # Design a query to retrieve the last 12 months of precipitation data and plot the results
    last_year_precip = session.query(MEASUR.date, MEASUR.prcp).\
    filter(MEASUR.date > query_date).all()

    session.close()
    # Convert list of tuples into normal list
    #all_names = list(np.ravel(last_year_precip))

    return jsonify(last_year_precip)
     
@app.route("/api/v1.0/stations")

def station():
    """Returns data for all stations in data set """
    # Create our session (link) from Python to the DB
    session = Session(bind=engine)

    # Design a query to show how many stations are available in this dataset?
    station_id_data = session.query(STAT.station, STAT.name, STAT.elevation).all()
   
    # Convert list of tuples into normal list
    #stations = list(np.ravel(station_id_data))
    session.close()
    return jsonify(station_id_data)

@app.route("/api/v1.0/tobs")
def temp():
    """Returns temprature from a start date """
    # Create our session (link) from Python to the DB
    session = Session(bind=engine)
    # Query for last day and first day on new data set
    query_date = dt.date(2017, 8, 23) - dt.timedelta(days=365)

    temp_dat = [MEASUR.station, MEASUR.tobs,MEASUR.date]

    temp_data = session.query(*temp_dat).\
        filter(MEASUR.date > query_date).\
        filter(MEASUR.station =='USC00519397').all()
    
    session.close()
    return jsonify(temp_data)

@app.route("/api/v1.0/<start>")

def single_date_ave(start):

    # Create our session (link) from Python to the DB
    session = Session(bind=engine)

    #temp_dat = [MEASUR.station, MEASUR.tobs,MEASUR.date]
    
    temp_data = session.query(MEASUR.tobs).\
        filter(MEASUR.date == start).all()
    # getting the STATS    
    temp_mean = round(np.mean(temp_data),1)
    temp_max =  max(temp_data)
    temp_min = min(temp_data)
    temp_count = len(temp_data)
    
    temp_stats = {"temp observations": temp_count, "temp high": temp_max, "temp low" : temp_min,
                     "temp average" : temp_mean , "start date": start}
    
    
    session.close()
    return jsonify(temp_stats)



@app.route("/api/v1.0/<start>/<end>")
def dates(start, end):
    # Create our session (link) from Python to the DB
    session = Session(bind=engine)

    #temp_dat = [MEASUR.station, MEASUR.tobs,MEASUR.date]
    
    temp_data = session.query(MEASUR.tobs).\
        filter(MEASUR.date > start, MEASUR.date < end).all()
    
    # getting the STATS    
    temp_mean = round(np.mean(temp_data),1)
    temp_max =  max(temp_data)
    temp_min = min(temp_data)
    temp_count = len(temp_data)
    temp_stats = {"temp observations": temp_count, "temp high": temp_max, "temp low" : temp_min,
                     "temp average" : temp_mean, "start date": start, "end date" : end}

        
    session.close()
    return jsonify(temp_stats)

@app.route("/")
def welcome():
    return (
        f"****************************************************************************"
        f"<h1>     Welcome to the Cliamte App Home Page</h1>"
        f"****************************************************************************"
        f"<h3>Available Routes:<br/></h3>"
        f"/api/v1.0/precipitation"
        f"<br/>"
        f"<br/>"
        f"/api/v1.0/stations"
        f"<br/>"
        f"<br/>"
        f"/api/v1.0/tobs"
        f"<br/>"
        f"<br/>"
        f"/api/v1.0/<start>" 
        f"<br/>"
        f"<br/>"
        f"/api/v1.0/<start>/<end>" 
    )


if __name__ == "__main__":
    app.run(debug=True)

########## SQL Alcehemy Homework API
####  Import Dependencies

import numpy as np
import sqlalchemy
from sqlalchemy.ext.automap import automap_base
from sqlalchemy.orm import Session
from sqlalchemy import create_engine, func
import datetime as dt
from flask import Flask, jsonify
import string

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
    # First identifiy last date in data set
    last_day = session.query(MEASUR.date).order_by(MEASUR.date.desc()).first()
    last_day

    # converts tuple to 3 integers
    # this is needed to get the delta time
    year = int(last_day[0][0:4])
    month = int(last_day[0][6:7])
    day = int(last_day[0][8:10])
    
    # calulated the time range
    query_date = dt.date(year, month, day) - dt.timedelta(days=365)
    # Design a query to retrieve the last 12 months of precipitation data and plot the results
    last_year_precip = session.query(MEASUR.date, MEASUR.prcp).\
    filter(MEASUR.date > query_date).all()

    session.close()
    # Convert list of tuples into normal list
    #all_names = list(np.ravel(last_year_precip))

    return jsonify(last_year_precip)
     
@app.route("/api/v1.0/stations")

def station():
    """Returns list of station names in data set """
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
    """Returns temprature data from a start date and most active station """
    # Create our session (link) from Python to the DB
    session = Session(bind=engine)
    ##### Step 1 get the date range
    # Query for last day and first day on new data set
    query_date = dt.date(2017, 8, 23) - dt.timedelta(days=365)

    # Query most acitve station
    # Calculates the stats for the most active station Stats Using query
    
    ###### step 2 find active station
    dat = [MEASUR.station,
        func.count(MEASUR.tobs),
        func.max(MEASUR.tobs),
        func.min(MEASUR.tobs),
        func.avg(MEASUR.tobs)] 

    most_active_station = session.query(*dat).\
        group_by(MEASUR.station).\
        order_by(func.count(MEASUR.tobs).desc()).first()

    # Extract station id from data
    temp_a = str(most_active_station).split(' ').pop(0)
    # strip punctuation
    active_station = temp_a.translate(str.maketrans('', '', string.punctuation))
    
    ###### Step 3
    #  Get temprature data from a start date and most active station
    temp_dat = [MEASUR.station, MEASUR.tobs,MEASUR.date]

    temp_data = session.query(*temp_dat).\
        filter(MEASUR.date > query_date).\
        filter(MEASUR.station == active_station).all()
    
    session.close()
    return jsonify(temp_data)

@app.route("/api/v1.0/<start>")

def single_date_ave(start):
    """retuns temp data bassed on date entry """
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
    """retuns temp data bassed on date range entry """
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
        f"<p><h1>     Welcome to the Climate App Home Page</h1></p>"
        f"****************************************************************************<br/>"
        f"<h2><u>Available Routes:<br/></u></h2>"
        f"<h3>Provides Precipitaton Data for last year available in data set.</h3> "
        f"<u>Path:<br/></u>"
        f"/api/v1.0/precipitation<br/>"
        
        f"<br/>"
        f"<h3>Provides station data (ID#, Name-address, elavation).</h3> "
        f"<u>Path:<br/></u>"
        f"/api/v1.0/stations"
        f"<br/>"
        f"<br/>"
        f"<h3>Provides date and temprature data for most active weather station.</h3> "
        f"<u>Path:<br/></u>"
        f"/api/v1.0/tobs"
        f"<br/>"
        f"<br/>"
        f"<h3>Enter date for historic temprature statistics.<br/> "
        f"Query format example: /api/v1.0/2016-08-23</h3> "
        f"<u>Path:<br/></u>"
        f"/api/v1.0/<start>" 
        f"<br/>"
        f"<br/>"
        f"<h3>Enter date range for historic temprature statistics.<br/> "
        f"Query format example:/api/v1.0/2016-08-23/2016-09-23</h3> "
        f"<u>Path:<br/></u>"
        f"/api/v1.0/<start>/<end>" 
    )


if __name__ == "__main__":
    app.run(debug=True)
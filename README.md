# SQLAlchemy Homework - Surfs Up!

## Overview
## Step 1 - Climate App
### Get the Data
1. Import Dependencies
2. Reflect Tables into SQL Alchemy ORM
3. Data exploration.

### Precipitation Analysis
1.  Design a query to retrieve the last 12 months of precipitation data.
2.  Select only the `date` and `prcp` values.
3.  Load the query results into a Pandas DataFrame and set the index to the date column.
4.  Sort the DataFrame values by `date`.
5.  Plot the results using the DataFrame `plot` method.
6.  Use Pandas to print the summary statistics for the precipitation data.

### Precipitation Analysis
1. Design a query to calculate the total number of stations.
2. Design a query to find the most active stations.
  * List the stations and observation counts in descending order.
  * Which station has the highest number of observations?
  * Hint: You will need to use a function such as `func.min`, `func.max`, `func.avg`, and `func.count` in your queries.
3. Design a query to retrieve the last 12 months of temperature observation data (TOBS).
  * Filter by the station with the highest number of observations.
  * Plot the results as a histogram with `bins=12`.

## Step 2 - Climate App
1. Use FLASK to develop climate APP (API)
2. Create landing page
3. Create query that returns data in JSON format
    A. Precipitation for last year.
    B. List of Stations. 
    C. Temprature data.
    D. Search temprature data by date.
    E. Search temprature data by date range.

![surfs-up.png](Images/surfs-up.png)


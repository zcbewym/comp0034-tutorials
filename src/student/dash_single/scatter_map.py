import sqlite3
from importlib import resources

import pandas as pd
import plotly.express as px


def scatter_geo():
    with resources.path("data", "paralympics.db") as path:
        # create database connection
        connection = sqlite3.connect(path)

        # define the sql query
        sql = '''
        SELECT event.year, host.host, host.latitude, host.longitude FROM event
        JOIN host_event ON event.event_id = host_event.event_id
        JOIN host on host_event.host_id = host.host_id
        '''
        
        # Use pandas read_sql to run a sql query and access the results as a DataFrame
        df_locs = pd.read_sql(sql=sql, con=connection, index_col=None)
        
        # The lat and lon are stored as string but need to be floats for the scatter_geo
        df_locs['longitude'] = df_locs['longitude'].astype(float)
        df_locs['latitude'] = df_locs['latitude'].astype(float)
        
        # Adds a new column that concatenates the city and year e.g. Barcelona 2012
        df_locs['name'] = df_locs['host'] + ' ' + df_locs['year'].astype(str)
        
        # Create the figure
        fig = px.scatter_geo(df_locs,
                             lat=df_locs.latitude,
                             lon=df_locs.longitude,
                             hover_name=df_locs.name,
                             title="Where have the paralympics been held?",
                             )
        return fig

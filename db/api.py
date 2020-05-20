import MySQLdb
import pandas as pd
from info import user, psswd, db_name

def connect_to_db():
    # Connect to the Database
    db = MySQLdb.connect(host="localhost",  # your host, usually localhost
                         user=user,  # your username
                         passwd=psswd,  # your password
                         db=db_name)  # the database

    return db

def get_wind_data(start, end):
    """
    Query wind data rows between two ranges

    :params start: start row id
    :params end: end row id
    :returns: pandas dataframe object
    """

    con = connect_to_db()
    query = f'SELECT rssi FROM rala WHERE id > "{start}" AND id <= "{end}";'
    df = pd.read_sql_query(query, con)
    return df


def get_wind_data_by_id(id):
    """
    Query a row from the Wind Table

    :params id: a row id
    :returns: pandas dataframe object
    """

    con = connect_to_db()
    query = f'SELECT * FROM rala WHERE id = "{id}";'
    df = pd.read_sql_query(query, con)
    return df

from PyDST.connection import connection
from PyDST.mapper import mapper

import geopandas as gpd
import matplotlib.pyplot as plt

import cmocean


# Example useage - assume we want to study the development in

conn = connection.connection('da')
meta = conn.get_metadata('FOLK1A')
df = conn.get_data('FOLK1A', variables = ['Tid', 'område'], values = {'tid':['*']}).df

plot = mapper.KOMplot(df[df['TID'] == '2008K2'], cmap = cmocean.cm.balance)


import sqlite3
import pandas as pd


meta


def to_sqlite(data, table_name, dbconnection = False, metadata = False, table_id = False):
    """ Saves data to the SQLite database connected to trough connection
    Args:
        data (pd.DataFrame): the data to save
        table_name (str): The name to save the data under
        connection (sqlite3 connection): connection to database
    """
    if not isinstance(dbconnection, sqlite3.Connection):
        dbconnection = sqlite3.connect('DEFAULT_DATABASE.sqlite')
        print('Connection is not a sqlite3.Connection. Setting default connection')

    if not isinstance(metadata, connection.metadata_return):
        msg = "metadata is not a metadata_return class, {}"

        if isinstance(tableid, str):
            metadata = connection.connection('da').get_metadata(table_id)
            print(msg.format(f"Getting metadata from {table_id}"))
        else:
            print(msg.format('Terminating and returning None'))
            return None

    if isinstance(table_name, str) and isinstance(table_id, str):
        # save a conversion key between name and ID in the database
    
    try:
        data.to_sql(table_name, dbconnection, if_exists = "replace")
        print('Saved data to database')

    except:
        raise ValueError('Something went wrong')







def from_sqlite(table_name, dbconnection = False, query = False):
    """ Reads data from a sqlite database.
    Args:
        table_name (str): table name in database
        connection (sqlite3 connection/bool): connection to database
            If False
        query
    """
    if not isinstance(dbconnection, sqlite3.Connection):
        dbconnection = sqlite3.connect('DEFAULT_DATABASE.sqlite')

    if not isinstance(query, str):
        query = f"select * from {table_name}"

    return pd.read_sql_query(query, connection)





DB = 'PyDST/local_db/test_file.sqlite'
dbconn = sqlite3.connect(DB)

to_sqlite(df, 'name', dbconn, meta, 'FOLK1A')



df.to_sql('FOLK1A', connection, if_exists = "replace")


pd.read_sql_query("select * from name", dbconn)


def is_updated(table_id):
    """
    """
    # look up in database if the table id exists. if it does, continue else
    # raise error

    # look in metadata if table id exists, if it does get the last updated value
    # and continue, else raise err

    # call DST to get the metadata, and compare with the last updated value above
    # if the same: return True
    # else, return False


meta.last_updated

df


import pandas as pd

pd.to_datetime('2008K2'.replace('K',''), format = '%Y')


def convert_yearquarter(time):
    year = time.str[0:4]
    quarter = time.str[-1]



convert(df['TID'], 'asd')



df

from PyDST.connection import connection
from PyDST.mapper import mapper

import geopandas as gpd
import matplotlib.pyplot as plt

import cmocean


# Example useage - assume we want to study the development in

conn = connection.connection('da')
df = conn.get_data('FOLK1A', variables = ['Tid', 'område'], values = {'tid':['*']}).df


plot = mapper.KOMplot(df[df['TID'] == '2008K2'], cmap = cmocean.cm.balance)


def convert(time, format_from = 'yearquarter'):
    """ Converts
    """
    formatlist = ['yearquarter']

    if format_from == 'yearquarter':
        return convert_yearquarter(time)
    else:
        raise NotImplementedError(f"""This format is either not implemented,
                    or does not exist. Valid formats are:
                    {','.join(formatlist)}""")


import pandas as pd

pd.to_datetime('2008K2'.replace('K',''), format = '%Y')


def convert_yearquarter(time):
    year = time.str[0:4]
    quarter = time.str[-1]



convert(df['TID'], 'asd')



df

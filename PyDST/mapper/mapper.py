
# This file should be able to map data from DST at various levels
from PyDST.utils import mappingutils as mutils

import geopandas as gpd
import matplotlib.pyplot as plt




def KOMplot(data, color = 'INDHOLD', komvar = 'OMRÅDE', cmap = 'hot', title = 'Municipality map'):
    """ A municipal map colored by 'color'.
    Args:
        data: A pandas dataframe with are codes and numeric data to plot
        color (str): Name of variable to use for coloring
        komvar (str): name of variable containing municipality names
        cmap (object): the colormap to use
        title (str): title of plot
    Returns:
        None
    """

    geo = gpd.read_file('PyDST/data/KOMMUNE.shp')
    data = geo.merge(data, how = 'left', left_on = 'KOMNAVN', right_on = komvar)

    if not data.shape[0] == geo.shape[0]:
        raise ValueError('There are duplicated municiaplities in your data.')

    data.plot(column = 'INDHOLD', colormap = cmap)
    plt.axis('off')
    plt.title(title)

    return None

import os
import pkg_resources
DATA_PATH = pkg_resources.resource_filename('PyDST', 'data/')


def are_files_installed():
        assert set(os.listdir(DATA_PATH)) == set(['KOMMUNE.dbf', 'KOMMUNE.prj', 'KOMMUNE.shp', 'KOMMUNE.shx',
                                       'SOGN.dbf', 'SOGN.prj', 'SOGN.shp', 'SOGN.shx'])
        print('Files are properly installed.')

def geopandas():
    import geopandas as gpd
    try:
        x = gpd.read_file(DATA_PATH + '/KOMMUNE.shp')
        x.plot()
    except:
        x = None

    assert x is not None
    print('Geopandas is working properly.')


if __name__ == '__main__':
    print('assessing that all geo-files are installed.')
    are_files_installed()
    print('Checking if geopandas works')
    geopandas()

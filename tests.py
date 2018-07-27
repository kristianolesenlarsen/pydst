import os
import pkg_resources
DATA_PATH = pkg_resources.resource_filename('PyDST', 'data/')


def are_files_installed():
    print("If this test passes, data are installed correctly")
    assert set(os.listdir(DATA_PATH)) == set(['KOMMUNE.dbf', 'KOMMUNE.prj', 'KOMMUNE.shp', 'KOMMUNE.shx',
                                       'SOGN.dbf', 'SOGN.prj', 'SOGN.shp', 'SOGN.shx'])

def geopandas():
    import geopandas as gpd
    try:
        x = gpd.read_file(DATA_PATH + '/KOMMUNE.shp')
    except:
        x = None

    assert x is not None


if __name__ == '__main__':
    are_files_installed()
    geopandas()

import os
import pkg_resources
DATA_PATH = pkg_resources.resource_filename('PyDST', 'data/')


def are_files_installed():
    print("If this test passes, data are installed correctly")
    assert set(os.listdir(DATA_PATH)) == set(['KOMMUNE.dbf', 'KOMMUNE.prj', 'KOMMUNE.shp', 'KOMMUNE.shx',
                                       'SOGN.dbf', 'SOGN.prj', 'SOGN.shp', 'SOGN.shx'])


if __name__ == '__main__':
    are_files_installed()

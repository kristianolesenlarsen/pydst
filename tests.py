import os
import pkg_resources
DATA_PATH = pkg_resources.resource_filename('PyDST', 'data/')


def are_files_installed():
        assert set(os.listdir(DATA_PATH)) == set(['KOMMUNE.dbf', 'KOMMUNE.prj', 'KOMMUNE.shp', 'KOMMUNE.shx',
                                       'SOGN.dbf', 'SOGN.prj', 'SOGN.shp', 'SOGN.shx'])
        print('Files are properly installed.')


if __name__ == '__main__':
    print('assessing that all geo-files are installed.')
    are_files_installed()

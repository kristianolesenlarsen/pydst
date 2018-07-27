from setuptools import setup

setup(name='PyDST',
      version='0.1',
      description='Grab data from Statistics Denmark',
      url='http://github.com/KristianUrupLarsen/PyDST',
      author='Kristian Urup Olesen Larsen',
      license='MIT',
      packages=['PyDST'],
      install_requires=[
        'matplotlib',
        'pandas',
        'requests'
      ],
zip_safe=False)

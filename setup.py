from setuptools import setup, find_packages

setup(name='statisticsdenmark',
      version='0.2',
      description='Grab data from the Statistics Denmark API',
      url='http://github.com/KristianUrupLarsen/PyDST',
      author='Kristian Urup Olesen Larsen',
      license='MIT',
      packages=find_packages(),
      install_requires=[
        'requests',
        'pytest'
      ],
zip_safe=False)

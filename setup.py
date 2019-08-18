from setuptools import setup, find_packages

setup(name='PyDST',
      version='0.2',
      description='Grab data from Statistics Denmark',
      url='http://github.com/KristianUrupLarsen/PyDST',
      author='Kristian Urup Olesen Larsen',
      license='MIT',
      packages=find_packages(),
      install_requires=[
        'pandas',
        'requests',
        'pytest'
      ],
zip_safe=False)

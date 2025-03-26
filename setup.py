from setuptools import setup, find_packages

setup(name='pydst',
      version='0.2.0',
      description='Pull data from Statistics Denmark',
      url='http://github.com/KristianUrupLarsen/pydst',
      author='Kristian Urup Olesen Larsen',
      license='MIT',
      packages=find_packages(),
      install_requires=[
        'requests', 'pandas'
      ],
      zip_safe=False)

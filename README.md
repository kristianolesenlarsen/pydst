# A tiny script for accessing the API of Statistics Denmark

PyDST holds functions to do basic interaction with the API of Statistics Denmark.  


<p align="center">
<img src="gdp.png" alt="GDP plot">
</p>

## Content

* class `DST()` takes variables `language` and `form` (output format) on initialization. Both have default values.
    * `__init__(language, form)`
        * `language` is `en` (english) as default, can be set to  `da` (danish).
        * `form` is `json` as default, can be set to `csv`.
    * `get_data(table_id, vars, values, **kwargs)` retrieves a specific table.
        * `table_id` is the id given to a specific table by Statistics Denmark.
        * `vars` is a list of variables to request.
        * `values` is a dictionary with keys being variables and values being the data-values of each variable to request. Note if vars are not supplied, the dictionary keys from values will be used instead.
        * `**kwargs` allow you to pass other parameters in the URL.
    * `browse_subject(subject_id, **kwargs)` allows you to browse and navigate the data hierachy as it appears on [statistikbanken](http://www.statistikbanken.dk/).
        * `id` is a unique number identifying the branch of the hierachy you want to browse (top level id's run from 01 to 18)
        * `**kwargs` allow you to pass other parameters in the URL.
    * `subject_tables(subject_id, **kwargs)` finds all tables associated with a specific subject or sub-subject
        * `subject_id` the subject id (or a list of id's), equivalent to the one used in browse_subject
        * `**kwargs` allow you to pass other parameters in the URL.
    * `metadata(table_id, output_format, **kwargs)` gives access to metadata about specific tables.
        * `table_id` the table you want metadata about
        * `output_format` the level of detail in the output, can be `full`, `variables` or `values`
        * `**kwargs` allow you to pass other parameters in the URL.
    * `toCSV(table, name)` converts the output to a csv file and saves it on drive. (note, this might be removed in the future)
        * `table` the raw output of `get_data(.)`
        * `name` the relative path to store the file at

## Usage
The script contains the class `DST()`, which takes arguments `language` and `form` (output format), both of which have default values. To learn more about what values can be supplied here or as kwargs, check out [the API console](http://api.statbank.dk/console#subjects).


After importing the .py file, you can call the following command to get information about the various datasets, or simply check the website of [DST](statistikbanken.dk).

```python
DST().subject('01')     # runs from 01 to 18
DST().table(subjects = ['01','02'])
```
Datasets are stored with alphanumeric id's such as `FOLK1A`, to download these simply runs

```python
DST(lang = 'da').getData(id = 'FOLK1A')
```

To control which variables are produced `.getData()` takes a list, while a dictionary is used to define which levels/values of each variable is wanted. The call below returns population data from the dataset `FOLK1A`, with variables for time (`Tid`), gender (`KØN`), subsetted to only return females, and area (`OMRÅDE`) subsetted to only return individuals in the municipality of Brøndby. (note that the `*` is used to signal that all possible levels should be returned)

```python
DST().getData(id = 'FOLK1A',
              vars = ['Tid', 'KØN', 'OMRÅDE'],
              values =  {'Tid': ['*'], 'KØN': ['2'], 'OMRÅDE':['153']} )
```

To figure out which data are available in a given dataset, simply call `DST().metadata(id)`, to get a rather complex JSON of variables and values of a given dataset. Finally the function `DST().toCSV(table = output_from_getData , name = intended_filename)` handles a small quirk of the returned CSV's (at least on windows machines) making it easy to save the returned values as .csv's.

The `*` does more than instruct the API to return all levels of a variable, as it can act as a joker, as such requesting `*K1` should return all levels ending in _K1_.


### Advanced requests
The API supports a number of advanced request formats, for now danish documentation of these can be found at DST, but hopefully they will be included at some point. The gist of it is that you can do lookups like

```python
DST().getData(id = 'FOLK1A',
              vars = ['ALDER'],
              values =  {'ALDER':['sum(0;1;2;3;4)']} )
```
which returns the sum of individuals with an age (`ALDER`) of 0,1,2,3 or 4 years.

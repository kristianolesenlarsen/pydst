# pydst
Simple functions for pulling data from the API of statistics denmark. 


## Usage
Look up data topics with 
```python
alltopics = pydst.get_topics()
alltopics.json()
```
To see subtopics you can do
```python
alltopics = pydst.get_topics(topics = '02', recursive = True)
alltopics.json()
```
To get the table id's associated with a specific topic use
```python
tables = pydst.get_tables(topics = '01')
tables.json()
```
Metadata about a table, including information on what variables are available in the data can be retrieved with
```python
pydst.get_metadata('FOLK1A').json()
```
To get an actual dataset 
```python
pydst.get_data('FOLK1A', variables = {'OMRÅDE': '*', 'Tid':, '*'}).json()
```
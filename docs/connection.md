# The `connection` class
`connection` sets up a session containing basic information like language. In the future it will hopefully support a broader range of options.



## class `connection`               [[source]](https://github.com/Kristianuruplarsen/PyDST/blob/master/PyDST/connection/connection.py)

_Parameters:_
* language (`str`): must be either `'da'` or `'en'` for either Danish or English language.
* store (`bool`): If store is set to `True` a list in the class instance `connection.data` is populated with API responses as you make the calls. (Default: `False`)
* retrn (`bool`): If retrn is set to `True` the connection methods actually return the API responses. (Default: `True`)
* Verbose (`bool`): should the class be verbose? (Default: `True`)

<br><br>
### `connection.get_data(table_id, variables=False, values=False, **kwargs)`
Send a request to DST's data retrieving API with specified parameters.

_Parameters:_
* table_id (`str`): table id, a list of available id's can be gained  from `connection.get_topics()` or the DST website.
* variables (`str`, `list(str)`, optional): which variables to get in the table will default to whatever DST serves as default if not set.
* values (`dict`, optional): which levels of each variable to get, will default to all available levels if not set.
* `**kwargs`: other variables passed in the URL.

_Returns:_
* class [`data_return`](return_classes/data_return)

<br><br>
### `connection.get_topics(topics, **kwargs)`
Gets information for the topics/subtopics available.

_Parameters:_
* topics (`str`/`list`): either a comma-separated string of topic-codes to search, or a list of topic-codes to seach.
* `**kwargs`: any other parameters to pass in the URL.

_Returns:_
* class [`topic_return`](return_classes/topic_return)


<br><br>
### `connection.get_tables(topics, **kwargs)`
Gets information in the tables available in a given topic.

_Parameters:_
* topics (`str`/`list`): either a string of topic ID's with one or more ID's separated by a comma, or a list of topic ID's, each a string.
* `**kwargs`: any other arguments you want to pass in the url.

_Returns:_
* class [`table_return`](return_classes/table_return)


<br><br>
### `connection.get_metadata(table_id, **kwargs)`

_Parameters:_
* table_id (`str`): ID of the table to get metadata on. ID's can be searched using the `connection.get_tables()` function.
* `**kwargs`: other arguments to the API URL.

_Returns:_
* class [`metadata_return`](return_classes/metadata_return)

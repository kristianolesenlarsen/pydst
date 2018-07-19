# The `connection` class
`connection` sets up a session containing basic information like language. In the future it will hopefully support a broader range of options.

## class `connection`               [[source]](https://github.com/Kristianuruplarsen/PyDST/blob/master/PyDST/connection/connection.py)

_Parameters:_
* language (`str`): must be either `'da'` or `'en'` for either Danish or English language.


### `connection.get_topics(topics, **kwargs)`
Gets information for the topics/subtopics available.

_Parameters:_
* topics (`str`/`list`): either a comma-separated string of topic-codes to search, or a list of topic-codes to seach.
* `**kwargs`: any other parameters to pass in the URL.

_Returns:_
* class [`topic_return`](return_classes/topic_return)

### `connection.get_tables(topics, **kwargs)`
Gets information in the tables available in a given topic.

_Parameters:_
* topics (`str`/`list`): either a string of topic ID's with one or more ID's separated by a comma, or a list of topic ID's, each a string.
* `**kwargs`: any other arguments you want to pass in the url.

_Returns:_
* class [`table_return`](return_classes/table_return)

### `connection.get_metadata(table_id, **kwargs)`

_Parameters:_
* table_id (`str`): ID of the table to get metadata on. ID's can be searched using the `connection.get_tables()` function.
* `**kwargs`: other arguments to the API URL.

_Returns:_
* class [`metadata_return`](return_classes/metadata_return)

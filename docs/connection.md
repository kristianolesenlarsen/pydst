# The `connection` class
`connection` sets up a session containing basic information like language. In the future it will hopefully support a broader range of options.

## class `connection`               [[source]](https://github.com/Kristianuruplarsen/PyDST/blob/master/PyDST/connection/connection.py)
_Parameters:_
* language (`str`): must be either `'da'` or `'en'` for either Danish or English language.

_Returns_:

### `connection.get_topics(topics, **kwargs)`
Gets information for the topics/subtopics available.
_Parameters:_
* topics (`str`/`list`): either a comma-separated string of topic-codes to search, or a list of topic-codes to seach.
* `**kwargs`: any other parameters to pass in the URL.
_Returns:_
* class [`topic_return`](return_classes/topic_return)

### `connection.`

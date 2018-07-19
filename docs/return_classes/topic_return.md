# The `topic_return` class     [[source]](https://github.com/Kristianuruplarsen/PyDST/blob/master/PyDST/connection/connection.py)
Contains the return of a topic call. This is a return class for responses from [`connection.get_topics()`](connection).

## class `topic_return`

_Parameters:_
* response: a raw requests response served by `connection.get_topics()`.

_Attributes:_
* `info`: dataframe of responses (this is the one you want to see)
* `json_list`: raw response json data
* `raw`: raw response
* `id_list`: list of querried ID's
* `descriptions`: list of descriptions for the ID's
* `active_list`: active status of each ID
* `subtopic_list`: list of lists of subtopics

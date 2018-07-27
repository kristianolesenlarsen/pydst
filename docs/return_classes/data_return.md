# The `data_return` class     [[source]](https://github.com/Kristianuruplarsen/PyDST/blob/master/PyDST/connection/connection.py)
Contains the return of a data call. This is a return class for responses from `connection.get_data()`.

_Parameters:_
* response: a raw requests response served by `connection.get_tables()`.

_Attributes:_
* `raw`: raw response
* `df`: pandas dataframe with the returned content
* `dict`: The data as a dictionary with name:[values] formatting


<br>
<br>
[back](../connection)

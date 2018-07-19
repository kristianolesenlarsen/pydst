# The `data_return` class
Contains the return of a table call. This is a return class for responses from `connection.get_data()`.

_Parameters:_
* response: a raw requests response served by `connection.get_tables()`.

_Attributes:_
* `raw`: raw response
* `df`: pandas dataframe with the returned content

# The `table_return` class
Contains the return of a table call. This is a return class for responses from `connection.get_tables()`.

_Parameters:_
* response: a raw requests response served by `connection.get_tables()`.

_Attributes:_
* `info`: dataframe of responses (this is the one you want to see)
* `raw`: raw response
* `json_list`: response json
* `id_list`: table id's
* `text_list`: table descriptions
* `unit_list`: table unit of measures
* `last_updated_list`: date of last updates
* `first_list`: earliest observation in tables
* `last_list`: latest observation in tables
* `active_list`: active status for tables
* `vars_list`: variables available in tables

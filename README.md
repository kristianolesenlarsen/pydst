
# PyDST
## This project is currently being reworked
Goals of the revamp are:

1) PyDST should be _very_ easy to extend with new functionality.
2) PyDST should have a segmented codebase to fulfill 1) and to make collaboration easy.
3) PyDST shuld not only currate data, but also handle storage, visualization etc.


## functionality

You should be able to get data as pandas dataframes from the API with
```python
from PyDST import connection
```

All other functions should be stored in e.g.
```python
from PyDST import plotting
from PyDST import db_storage
```

Everything must be segmented in folders like `connection` which has a clearly stated input and output.

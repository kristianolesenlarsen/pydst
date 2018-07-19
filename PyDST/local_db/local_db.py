
# In this file resides all the code for creating local SQLite databases which
# store both data and metadata

import sqlite3


DB = 'PyDST/local_db/test_file.sqlite'


connection = sqlite3.connect(DB)

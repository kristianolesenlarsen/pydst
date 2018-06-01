from PyDST.connection import connection



conn = connection.connection('en')

meta = conn.get_metadata('FOLK1A')





df = conn.get_data('FOLK1A', variables = ['Tid', 'område'], values = {'tid':'2018Q2'}).df


df

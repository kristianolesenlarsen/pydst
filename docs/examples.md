# Example 1: using PyDST to return response objects
The simplest way to use PyDST is to use it in the same way which is shown on
the front page. Imagine you want to know about the state of the book-market
in Denmark. A good place to start is then the `BOG03` dataset from statistics
denmark. It shows how many books are published each year split by genre and media.

We set up PyDST by initiating a connection and getting metadata for the table:

```python
import PyDST

>>> conn = PyDST.connection(language = 'en')

>>> meta = conn.get_metadata('BOG03')
>>> meta.variables
['boger', 'sprog', 'oversat', 'medie', 'tid']
```

Next we run `meta.json` to get a more detailed picture of the table contents.
This tells us that `MEDIE=660` is all books, while `MEDIE=670` only contains
print books. We then construct a request to get these two for all years.

```python
>>> resp = conn.get_data('BOG03',
                     variables = ['tid', 'medie'],
                     values = {'tid':['*'], 'medie': ['660', '670']}
                     )
```

We can then access the dataframe by typing `resp.df`. From here you can plot the figure either using one of pythons many plotting libraries.  


# Example 2: using the `store` option.
Sometimes we want to load multiple data at once, perhaps because we want to loop over each dataset, or merge them together. Say we want a separate dataset with each of the two media codes from above. We can achieve this by

```python
import PyDST

>>> conn = PyDST.connection(language = 'en', store = True, return = False)

>>> for mediaCode in '660','670':
>>>     conn.get_data('BOG03',
                     variables = ['tid', 'medie'],
                     values = {'tid':['*'], 'medie': mediaCode}
                     )
```
Now we can access `conn.data` to get a list of two data return objects similar to the one we stored in `resp` above. 

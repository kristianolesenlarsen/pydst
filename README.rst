
Pydst is a simple package for pulling data from the API of statistics Denmark. Documentation is at https://kristianuruplarsen.github.io/pydst/.

To install you can run 

>>> pip install git+https://github.com/Kristianuruplarsen/pydst.git

The main interface is through four functions that respectively browse subjects, browse tables within a subject, retrieve metadata about tables, and retrieves actual tables of data. Except for ``get_data`` the default format is json. ``get_data`` uses semicolon separated csv as its default.

Example
=======
This example covers the basics of ``pydst``. First import the package and retrieve the list of available subjects


.. code-block:: python

    >>> import pydst 
    >>> resp = pydst.get_subjects()      # No table_id gets all available subjects
    DSTResponse(entrypoint=subjects, lang=en, fmt=json, recursive=None, omit_empty=None, include_tables=None)

The ``DSTResponse`` object is a thin wrapper around ``requests.Response`` that stores a bit of information about the request. To get to the data do

.. code-block:: python
    
    >>> resp.json()
    [{'id': '02',
      'description': 'Population and elections',
      'active': True,
      'hasSubjects': True,
      'subjects': []},
        ...

Say we want data from subject ``'16'``, "Money and credit market". To find out what tables are available run

.. code-block:: python

    >>> tables = pydst.get_tables(subjects = '16').json()
        [{'id': 'DNVPDKS',
        'text': 'VP-registered securities',
        'unit': 'm DKK',
        'updated': '2020-07-28T08:00:00',
        'firstPeriod': '1999M12',
        'latestPeriod': '2020M06',
        'active': True,
        'variables': ['type of security',
        'coupon',
        'currency',
        'maturity',
        'issuer sector',
        'investor sector',
        'valuation',
        'data type',
        'time']},    
            ...

Here we can pick a dataset, e.g. ``'DNTRENDT'`` containing "Interest rates by item, country, methodology and time". We still need to figure out what data are available in this table, so before calling ``get_data`` let us find some detailed information on ``'DNTRENDT'``

.. code-block:: python

    >>> info = pydst.get_tableinfo(table_id = 'DNTRENDT').json()

This will produce a large json file containing metadata including when the table was last updated, contact details for whoever is responsible for maintaining the dataset and more importantly, variable names and values of the dataset. In this case we will get the discount rate (variable ``'INSTRUMENT'`` and value ``'ODKNAA'``) all months since 1983 (variable ``'Tid'``, which is *time* in Danish, all values ``*``). Finally we will get an error unless we set the ``'OPGOER'`` variable, so we will set this to "Daily interest rates (per cent)" (``'E'``).

.. code-block:: python

    >>> data = pydst.get_data(table_id = 'DNRENTD',
    >>>                       variables = {'INSTRUMENT': 'ODKNAA',
    >>>                                    'Tid': '*',
    >>>                                    'OPGOER': 'E'})

As a final step, we can convert the data to a ``pandas.DataFrame`` with

.. code-block:: python

    >>> df = pydst.utils.to_dataframe(data)
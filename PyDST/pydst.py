
''' Make requests to the DST API. Results are returned as raw requests responses 
    to facilitate custom postprocessing.
'''

import requests
from .utils import *

BASE_URL = "https://api.statbank.dk/v1"


def get_topics(topics='', 
               lang='en', 
               fmt = 'json',
               recursive=None,
               omit_empty=None,
               include_tables=None
               ):
    ''' Request a json of available topics. These are
        broad categories of data (e.g. 'population and elections'
        or 'culture and church'). The default is to retrieve
        all high level topics. Set the topics parameter to retrieve
        only a subset.

        Parameters
        ----------
        :param lang: Language of result (da/en).
        :type lang: str

        :param fmt: format (default is json).
        :type fmt: str

        :param recursive: Recursively include topics from the hierachy.
        :type recursive: bool

        :param omit_empty: Omit topics with no tables associated.
        :type omit_empty: bool

        :param include_tables: Include table id's as lowest level topics.
        :type include_tables: bool

        :return: :class: `Response` a requests response object.
        :rtype: requests.models.Response        

        Usage::

            >>> from pydst import get_topics
            >>> topics = get_topics(topics = '02')
            >>> print(topics.json())
    '''
    topics = coerce_input_to_str(topics)
    url = f"{BASE_URL}/subjects/{topics}"
    url = add_url_parameters(url=url,
                             lang=lang,
                             format=fmt, 
                             recursive=recursive,
                             omitSubjectsWithoutTables=omit_empty,
                             includeTables=include_tables)

    return requests.get(url)


def get_tables(topics = None,
               lang = 'en',
               fmt = 'json',
               past_days=None,
               include_inactive=None,
               ):
    ''' Get table id's associated with a (list of) topics.

        Parameters
        ----------
        :param topics: topics to retrieve table id's for.
        :type topics: str/list/tuple 

        :param lang: Language of result (da/en).
        :type lang: str

        :param fmt: format (default is json).
        :type fmt: str

        :param past_days: include tables updated in the past x days. Must be positive if included.
        :type past_days: int

        :param include_inactive: include tables that are no longer updated.
        :type include_inactive: bool 

        :return: :class: `Response` a requests response object.
        :rtype: requests.models.Response        

        Usage::

            >>> from pydst import get_tables
            >>> tables = get_tables(topics = '02')
            >>> print(tables.json())
    '''
    topics = topics if topics is None else coerce_input_to_str(topics)
    url = f"{BASE_URL}/tables/"

    url = add_url_parameters(url=url,
                             subjects=topics,
                             lang=lang,
                             format=fmt,
                             pastDays=past_days,
                             includeInactive=include_inactive
                             )
    return requests.get(url)


def get_metadata(table_id,
                 lang = 'en',
                 fmt = 'json'
                 ):
    ''' Get metadata for a specific table id.

        Parameters
        ----------
        :param table_id: a table id (e.g. FOLK1A). 
        :type table_id: str

        :param lang: language (da/en)
        :type lang: str

        :param fmt: format (default is json)
        :type fmt: str

        :return: :class: `Response` a requests response object.
        :rtype: requests.models.Response

        Usage::

            >>> from pydst import get_metadata
            >>> meta = get_metadata(table_id = 'FOLK1A')
            >>> print(meta.json())
    '''
    url = f"{BASE_URL}/tableinfo/{table_id}"

    url = add_url_parameters(url=url,
                             lang=lang,
                             format=fmt,
                             )
    return requests.get(url)


def get_data(table_id, 
             variables, 
             lang = 'en',
             fmt = 'json',
             coding = None,
             order = None,
             delim = None
             ):
    ''' Get actual data from a specific table identified by its `table_id`.

        :param table_id: id of table to get.
        :type table_id: str

        :param variables: dictionary of variable-name, variable-value pairs. Use '*' to select all available values.
        :type variables: dict            

        :param lang: language (da/en)
        :type lang: str

        :param fmt: format (default is json)
        :type fmt: str

        :param coding: return data as code ('Code'), string label ('Value'), both ('CodeAndValue') or default ('Default')
        :type coding: str

        :param order: order data 'ascending' or 'descending'.
        :type order: str

        :param delim: delimiter ('tab' or 'semicolon')
        :type delim: str

        :return: :class: `Response` a requests response object.
        :rtype: requests.models.Response        

        Usage::

            >>> from pydst import get_data
            >>> import pandas as pd
            >>> from io import StringIO
            >>> resp = get_data(table_id = 'FOLK1A', 
            >>>                 variables = {'Tid': '*'}, 
            >>>                 fmt = 'csv')
            >>> pd.read_csv(StringIO(resp.text), sep = ';')
    '''
    fmt = fmt if fmt != 'json' else 'jsonstat'
    url = f"{BASE_URL}/data/{table_id}/{fmt}"    
    url = add_url_parameters(url=url,
                             lang=lang,
                             format=fmt,
                             valuePresentation=coding,
                             timeOrder=order,
                             delimiter=delim,
                             **{k:coerce_input_to_str(v) for k, v in variables.items()}
                             )
    return requests.get(url)


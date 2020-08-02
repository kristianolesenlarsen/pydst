
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

        Parameters with a value of None are not included
        in the final url.

        Parameters
        ----------
        lang (str): language (da/en).
        fmt (str): format (json by default)
        recursive (bool/None): recursively include topics from the hierachy.
        omit_empty: omit topics with no tables associated.
        include_tables: include table id's as lowest level topics.

        Returns
        -------
        requests.models.Response
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
        topics (str/list/tuple): topics to retrieve table id's for.
        lang (str): language (da/en)
        fmt (str): format (default is json)
        past_days (int>0): include tables updated in the past x days,
        include_inactive (bool): include tables that are no longer updated.

        Returns
        -------
        requests.models.Response        
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
        table_id (str): a table id (e.g. FOLK1A). 
        lang (str): language (da/en)
        fmt (str): format (default is json)

        Returns
        -------
        requests.models.Response        
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
    ''' Get table id's associated with a (list of) topics.

        Parameters
        ----------
        table_id (str): id of table to get.
        variables (dict): dictionary of variable-name, variable-value
            pairs. Use '*' to select all available values.
        variables
        values
        lang (str): language (da/en)
        fmt (str): format (default is json)
        coding (str): return data as code ('Code'), string label ('Value'),
                      both ('CodeAndValue') or default ('Default')
        order (str): order data 'ascending' or 'descending'.
        delim (str): delimiter ('tab' or 'semicolon')

        Returns
        -------
        requests.models.Response        
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


""" Make requests to the DST API. Results are returned as raw requests responses 
    to facilitate custom postprocessing.
"""

import requests
from .utils import (
    coerce_input_to_str,
    add_url_parameters,
    list_from_comma_separated_string,
    DSTResponse,
)

BASE_URL = "https://api.statbank.dk/v1"


def get_subjects(
    subjects="", lang="en", fmt="json", recursive=None, omit_empty=None, include_tables=None,
):
    """ Request a json of available topics. These are
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

        :return: :class: `DSTResponse` a response class wrapping the raw request.

        Usage::

            >>> from pydst import get_subjects
            >>> subs = get_subjects(subjects = '02')
            >>> print(subs.json())
    """
    subjects = coerce_input_to_str(subjects)
    url = f"{BASE_URL}/subjects/{subjects}"
    url = add_url_parameters(
        url=url,
        lang=lang,
        format=fmt,
        recursive=recursive,
        omitSubjectsWithoutTables=omit_empty,
        includeTables=include_tables,
    )

    return DSTResponse(
        response=requests.get(url),
        entrypoint="subjects",
        lang=lang,
        fmt=fmt,
        recursive=recursive,
        omit_empty=omit_empty,
        include_tables=include_tables,
    )


def get_tables(
    subjects=None, lang="en", fmt="json", pastdays=None, include_inactive=None,
):
    """ Get table id's associated with a (list of) topics.

        Parameters
        ----------
        :param topics: topics to retrieve table id's for.
        :type topics: str/list/tuple 

        :param lang: Language of result (da/en).
        :type lang: str

        :param fmt: format (default is json).
        :type fmt: str

        :param pastdays: include tables updated in the past x days. Must be positive if included.
        :type pastdays: int

        :param include_inactive: include tables that are no longer updated.
        :type include_inactive: bool 

        :return: :class: `DSTResponse` a response class wrapping the raw request.

        Usage::

            >>> from pydst import get_tables
            >>> tables = get_tables(topics = '02')
            >>> print(tables.json())
    """
    subjects = subjects if subjects is None else coerce_input_to_str(subjects)
    url = f"{BASE_URL}/tables/"

    url = add_url_parameters(
        url=url,
        subjects=subjects,
        lang=lang,
        format=fmt,
        pastDays=pastdays,
        includeInactive=include_inactive,
    )
    return DSTResponse(
        response=requests.get(url),
        entrypoint="tables",
        subjects=subjects,
        lang=lang,
        format=fmt,
        pastDays=pastdays,
        includeInactive=include_inactive,
    )


def get_tableinfo(
    table_id, lang="en", fmt="json",
):
    """ Get metadata for a specific table id.

        Parameters
        ----------
        :param table_id: a table id (e.g. FOLK1A). 
        :type table_id: str

        :param lang: language (da/en)
        :type lang: str

        :param fmt: format (default is json)
        :type fmt: str

        :return: :class: `DSTResponse` a response class wrapping the raw request.

        Usage::

            >>> from pydst import get_tableinfo
            >>> meta = get_tableinfo(table_id = 'FOLK1A')
            >>> print(meta.json())
    """
    url = f"{BASE_URL}/tableinfo/{table_id}"

    url = add_url_parameters(url=url, lang=lang, format=fmt)
    return DSTResponse(response=requests.get(url), entrypoint="tableinfo", lang=lang, fmt=fmt)


def get_data(
    table_id, variables={}, lang="en", fmt="csv", coding=None, order=None, delim=None,
):
    """ Get actual data from a specific table identified by its `table_id`.

        :param table_id: id of table to get.
        :type table_id: str

        :param variables: dictionary of variable-name, variable-value pairs. Use '*' to select all available values.
        :type variables: dict            

        :param lang: language (da/en)
        :type lang: str

        :param fmt: format (default is 'csv')
        :type fmt: str

        :param coding: return data as code ('Code'), string label ('Value'), both ('CodeAndValue') or default ('Default')
        :type coding: str

        :param order: order data 'ascending' or 'descending'.
        :type order: str

        :param delim: delimiter ('tab' or 'semicolon')
        :type delim: str

        :return: :class: `DSTResponse` a response class wrapping the raw request.

        Usage::

            >>> from pydst import get_data
            >>> resp = get_data(table_id = 'FOLK1A', 
            >>>                 variables = {'Tid': '*'}, 
            >>>                 fmt = 'csv')
    """
    fmt = fmt if fmt != "json" else "jsonstat"
    url = f"{BASE_URL}/data/{table_id}/{fmt}"
    url = add_url_parameters(
        url=url,
        lang=lang,
        valuePresentation=coding,
        timeOrder=order,
        delimiter=delim,
        **{k: coerce_input_to_str(v) for k, v in variables.items()},
    )
    return DSTResponse(
        response=requests.get(url),
        entrypoint="data",
        fmt="json" if fmt == "jsonstat" else fmt,
        lang=lang,
        valuePresentation=coding,
        timeOrder=order,
        delimiter=delim,
        **{k: coerce_input_to_str(v) for k, v in variables.items()},
    )


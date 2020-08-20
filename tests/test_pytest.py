import pytest

import pydst
from pydst.utils import (
    DSTResponse,
    coerce_input_to_str,
    add_url_parameters,
    list_from_comma_separated_string,
)
from pydst.dataframes import _data_csv_to_dataframe

import requests
import pandas as pd


def test_coerce_input_to_str():
    assert coerce_input_to_str(["a", "b", "c"]) == "a,b,c"
    assert coerce_input_to_str(("a", "b", "c")) == "a,b,c"
    assert coerce_input_to_str("a,b,c") == "a,b,c"

    with pytest.raises(ValueError):
        coerce_input_to_str(lambda x: x + 1)


def test_add_url_parameters():
    assert add_url_parameters("something.com", a="a", b="b") == "something.com?a=a&b=b"
    assert add_url_parameters("something.com") == "something.com"
    assert add_url_parameters("something.com", a=None) == "something.com"
    assert add_url_parameters("something.com", a="a", b=None) == "something.com?a=a"
    assert add_url_parameters("something.com", a=None, b="b") == "something.com?b=b"


def test_list_from_comma_separated_string():
    assert list_from_comma_separated_string("a,b,c") == ["a", "b", "c"]
    assert list_from_comma_separated_string("a, b, c") == ["a", "b", "c"]
    assert list_from_comma_separated_string("ab c") == ["abc"]


def test_get_subjects():
    call = pydst.get_subjects()
    assert isinstance(call, DSTResponse)
    assert hasattr(call, "response")
    assert hasattr(call, "entrypoint")
    assert type(call.response) == requests.models.Response
    assert type(call.entrypoint) == str
    assert call.status_code == 200
    call.json()


def test_get_tables():
    call = pydst.get_tables()
    assert isinstance(call, DSTResponse)
    assert hasattr(call, "response")
    assert hasattr(call, "entrypoint")
    assert type(call.response) == requests.models.Response
    assert type(call.entrypoint) == str
    assert call.status_code == 200
    assert pydst.get_tables(subjects="01").status_code == 200
    assert pydst.get_tables(subjects=["01", "02"]).status_code == 200
    call.json()


def test_get_tableinfo():
    call = pydst.get_tableinfo(table_id="FOLK1A")
    assert isinstance(call, DSTResponse)
    assert hasattr(call, "response")
    assert hasattr(call, "entrypoint")
    assert type(call.response) == requests.models.Response
    assert type(call.entrypoint) == str
    assert call.status_code == 200
    call.json()


def test_get_data():
    call = pydst.get_data(table_id="FOLK1A")
    assert isinstance(call, DSTResponse)
    assert hasattr(call, "response")
    assert hasattr(call, "entrypoint")
    assert hasattr(call, "fmt")
    assert type(call.response) == requests.models.Response
    assert type(call.entrypoint) == str
    assert call.status_code == 200
    assert call.fmt == "json"
    call.json()

    call = pydst.get_data(table_id="FOLK1A", fmt="csv")
    assert call.fmt == "csv"
    call.text


def test_to_dataframe():
    call = pydst.get_data(table_id="FOLK1A", fmt="csv")
    df = to_dataframe(call)
    assert isinstance(df, pd.DataFrame)

    call = pydst.get_data(table_id="FOLK1A")
    assert call.fmt == "json"

    with pytest.raises(ValueError):
        to_dataframe(call)

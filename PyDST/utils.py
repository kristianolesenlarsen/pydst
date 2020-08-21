""" Utility functions for the pydst library.
"""
from .errors import DSTApiError

from pandas import read_csv
from requests.exceptions import HTTPError
from io import StringIO


def coerce_input_to_str(data):
    """ Coerce url data to a comma separated string.
        e.g. ['a','b'] becomes 'a,b' while 'c,d' is
        unchanged.

        :param data: Input data to coerce.
        :type data: str, list, tuple

        :return: Joined string.
        :rtype: str

    """
    if isinstance(data, str):
        return data
    elif isinstance(data, (list, tuple)):
        return ",".join(data)
    raise ValueError(f"{data} is not a valid input.")


def list_from_comma_separated_string(s):
    """ Convert a comma separated string such
        as '1,2,3' to a list.

        :param s: string of items separated by commas.
        :type s: str

        :return: list of separated values.
        :rtype: list
    """
    return s.replace(" ", "").split(",")


def add_url_parameters(url, **parameters):
    """ Add url parameters to the base url.

        :param url: base url.
        :type url: str


        :kwargs: key-value pairs of the url parameters to add. If the value is None, the pair is not added.
        
        :return: url string.
        :rtype: str
    """
    parameters = {k: v for k, v in parameters.items() if v is not None}
    if len(parameters) == 0:
        return url
    parameters = "&".join([f"{k}={v}" for k, v in parameters.items()])
    return f"{url}?{parameters}"


class DSTResponse:
    """ Response wrapper. Preserves information on the entrypoint and format of the 
        data to allow automatic conversion to pandas.

        :param response: requests.Response object.
        :type response: requests.Response

        :param entrypoint: The API entrypoint of the call.
        :type entrypoint: str

        :kwargs: Extra parameters passed to the API.

        :ivar response: requests Response object.
        :type response: requests.Response

        :ivar entrypoint: used entrypoint of the API.
        :type entrypoint: str

        :ivar \*\*parameters: Additional parameters passed to the API.
    """

    def __init__(self, response, entrypoint, **parameters):
        try:
            response.raise_for_status()
        except HTTPError as error:
            raise DSTApiError(response.text) from error

        self.response = response
        self.entrypoint = entrypoint
        self.parameters = parameters
        for k, v in parameters.items():
            setattr(self, k, v)

    def __repr__(self):
        return "DSTResponse(entrypoint={}, {})".format(
            self.entrypoint, ", ".join(f"{k}={v}" for k, v in self.parameters.items())
        )

    def __str__(self):
        return "DSTResponse(entrypoint={}, {})".format(
            self.entrypoint, ", ".join(f"{k}={v}" for k, v in self.parameters.items())
        )

    @property
    def status_code(self):
        """ Get the response status code """
        return self.response.status_code

    @property
    def text(self):
        """ Get raw text data of response. """
        return self.response.text

    def json(self):
        """ Get JSON data of response. """
        return self.response.json()


def to_dataframe(dstresponse):
    """ Get dataframe from csv format data 

        :param dstresponse: DSTResponse from the data entrypoint.
        :type dstresponse: pydst.utils.DSTResponse

        :return: A pandas dataframe containing the values.
        :rtype: pd.DataFrame

        Usage::

            >>> from pydst.utils import to_dataframe
            >>> from pydst import get_data
            >>> r = get_data('FOLK1A', 
            >>>              variables = {'OMRÅDE':'*', 'Tid':'*'}, 
            >>>              fmt = 'csv')
            >>> df = to_dataframe(r)
    """
    if dstresponse.entrypoint != "data":
        raise ValueError(f"entrypoint {dstresponse.entrypoint} cannot be read as csv.")
    if dstresponse.fmt != "csv":
        raise NotImplementedError(f"response has format {dstresponse.fmt}, only csv is supported.")
    return read_csv(StringIO(dstresponse.text), sep=";")

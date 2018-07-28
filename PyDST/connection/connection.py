
# This file contains the class data_retriever, which is able to interface with
# the DST api to retrieve data and return them as pandas dataframes.
# The main class takes a
from PyDST.utils import connectionutils as cutils
from PyDST.connection.return_classes import (data_return,
                                             metadata_return,
                                             topic_return,
                                             table_return)
import pandas as pd
import requests

# ------------------------------------------------------------------------------
# see http://api.statbank.dk/console#subjects for more examples of usage.
# ------------------------------------------------------------------------------

class connection:
    """ Retrieves data, metadata and table overviews from the DST service
    """
    # For devs: this class must only do the following: take user input for cons-
    # tructing a string URL, which can be used to GET (not POST) the data from
    # the DST API. The requests.response must then be immediatly checked for
    # status, and if ok, passed on to a return_classes class to handle cleaning
    # of raw data.
    # In short: here we handle getting home good data, nothing more.

    def __init__(self, language = 'en',
                       store = False,
                       retrn = True,
                       verbose = True):
        """ Initiate datagetter
        Args:
            - language (str): language (options are 'da','en')
            - store (bool): should the retrieved data be stored in an internal
                            list? default: False
            - retrn (bool) Should the retrieved data be returned? default: True
            - verbose (bool): Should the connection be verbose about what it's
                              doing? default: True
        """
        self.lang = cutils.validate_language(language)
        self.store_response = store
        self.return_response = retrn
        # only print if verbose is true function
        self.vprint = print if verbose else lambda *a, **k: None
        # This shouldn't be changed for now
        self.format = 'JSON'
        # for internal storage of the return values. Allows to get multiple data
        # with a single connection.
        self.topics = []
        self.tables = []
        self.metadata = []
        self.data = []

    def __repr__(self):
        return f"{self.__class__.__name__}(language = {self.lang})"

    def __str__(self):
        return f"DST API connection with language {self.lang}"

    def __len__(self):
        return len(self.data)

    def __getitem__(self, position):
        return self.data[position]

    def __call__(self):
        print(f"Number of datasets stored: {len(self.data)}")
        print(f"Total number of valid API calls made: {len(self.data + self.tables + self.metadata + self.topics)}")


    def get_topics(self, topics, **kwargs):
        """ Gets information for the topics/subtopics available

        Args:
            topics (str/list): either a string of topic ID's with one or more
                ID's separated by a comma, or a list of topic ID's, each a str

            **kwargs: any other arguments you want to pass in the url.

        Returns:
            class topic_return
        """
        topics = cutils.coerce_input_type_to_str(topics)

        self.vprint(f"Getting all topics under topic code(s) {topics}")

        base = f"https://api.statbank.dk/v1/subjects/{topics}?format={self.format}"
        base = cutils.handle_kwargs(base, **kwargs)

        # get the data
        response = requests.get(base)

        # This handles storing the data and/or returning it
        if response.ok:

            if self.store_response:
                self.topics.append(topic_return(response))
            if self.return_response:
                return topic_return(response)

        else:
            response.raise_for_status()



    def get_tables(self, topics, **kwargs):
        """ Gets information in the tables available in a given topic.

        Args:
            topics (str/list): either a string of topic ID's with one or more
                ID's separated by a comma, or a list of topic ID's, each a str

            **kwargs: any other arguments you want to pass in the url.

        Returns:
            class table_return
        """
        topics = cutils.coerce_input_type_to_str(topics)
        self.vprint("Getting all tables under topic code(s) {topics}")

        base = f"https://api.statbank.dk/v1/tables?subjects={topics}&format={self.format}"
        base = cutils.handle_kwargs(base, **kwargs)
        response = requests.get(base)

        if response.ok:

            if self.store_response:
                self.tables.append(table_return(response))
            if self.return_response:
                return table_return(response)

        else:
            response.raise_for_status()



    def get_metadata(self, table_id, **kwargs):
        """ returns a metadata request for the supplied table ID

        Args:
            table_id (str): ID of the table to get metadata on. ID's can be searched
                using the get_tables() function.
            **kwargs: other arguments to the API URL.
        """
        if isinstance(table_id, str):
            self.vprint(f"Getting metadata for table {table_id}")
            base = f"https://api.statbank.dk/v1/tableinfo/{table_id}?format={self.format}"
        else:
            raise ValueError(f"'{str(topics)}' is not a valid topics-list, it must be str.")

        base = cutils.handle_kwargs(base, **kwargs)
        response = requests.get(base)

        if response.ok:

            if self.store_response:
                self.metadata.append(metadata_return(response, table_id))
            if self.return_response:
                return metadata_return(response, table_id)

        else:
            response.raise_for_status()



    def get_data(self, table_id, variables=False, values=False, **kwargs):
        """ Send a request to DST's data retrieving API with specified parameters.

        Args:
            table_id (str): table id, a list of available id's can be gained  from
               .subjects() or the DST website.
            variables (list, optional): which variables to get in the table.
            values (dict, optional): which levels of each variable to get.
            **kwargs: other variables passed in the URL.

         example request:
         DST().get_data("FOLK1A", ["Tid","CIVILSTAND"],
         {'Tid': ["*"], 'CIVILSTAND': ["TOT","U"]})
         """
        if not isinstance(table_id, str):
            raise TypeError(f"Supplied table_id {table_id} is not of type str")
        # if vars not set, set it to ''
        #if values is not set, set it to * - meaning get all levels
        if not variables and not values:
            self.vprint("""
            No variables or values selected! Getting API default
            """)

        if not variables and values:
            self.vprint("""
            No variables selected! Using value-dictionary keys as variables
            """)
            variables = list(values.keys())

        if variables and not values:
            self.vprint("""
            No values selected! Setting values to all ('*')
            """)
            values = {}
            if isinstance(variables, list):
                for i in variables:
                    values[i] = ['*']
            elif isinstance(variables, str):
                for i in variables.split(','):
                    values[i] = ['*']
            else:
                raise ValueError('Could not construct values.')

        self.vprint(f"""Getting table {table_id}, variables are {str(variables)}
        values are {str(values)}""")
        # set the base link to get table with id = id
        base = f"http://api.statbank.dk/v1/data/{table_id}/CSV?lang={self.lang}"
        # generate the API call link
        base = cutils.link_generator_with_error_handling(base, variables, values)
        # add kwargs to link
        base = cutils.handle_kwargs(base, **kwargs)
        # get API response
        response = requests.get(base)

        if response.ok:

            if self.store_response:
                self.data.append(data_return(response, table_id, variables, values))
            if self.return_response:
                return data_return(response, table_id, variables, values)

        else:
            response.raise_for_status()

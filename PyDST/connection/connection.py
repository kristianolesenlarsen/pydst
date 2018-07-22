
# This file contains the class data_retriever, which is able to interface with
# the DST api to retrieve data and return them as pandas dataframes.
# The main class takes a
from PyDST.utils import connectionutils as cutils

import pandas as pd
import requests

from io import StringIO

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

    def __init__(self, language = 'en'):
        """ Initiate datagetter
        Args:
            - language (str): language (options are 'da','en')
        """
        self.lang = cutils.validate_language(language)

        self.format = 'JSON'    # this cannot be changed, otherwise presenting
                                # neat metadata etc. will be to much work


    def get_topics(self, topics, **kwargs):
        """ Gets information for the topics/subtopics available

        Args:
            topics (str/list): either a string of topic ID's with one or more
                ID's separated by a comma, or a list of topic ID's, each a str

            **kwargs: any other arguments you want to pass in the url.

        Returns:
            class topic_return
        """
        if isinstance(topics, str):
            base = f"https://api.statbank.dk/v1/subjects/{topics}?format={self.format}"
        elif isinstance(topics, list):
            base = f"https://api.statbank.dk/v1/subjects/{','.join(topics)}?format={self.format}"
        else:
            raise ValueError(f"'{topics}' is not a valid topics-list, it must be str of list")

        base = cutils.handle_kwargs(base, **kwargs)

        # get the data
        response = requests.get(base)

        if response.ok:
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
        if isinstance(topics, str):
            base = f"https://api.statbank.dk/v1/tables?subjects={topics}&format={self.format}"
        elif isinstance(topics, list):
            base = f"https://api.statbank.dk/v1/tables?subjects={','.join(topics)}&format={self.format}"
        else:
            raise ValueError(f"'{topics}' is not a valid topics-list, it must be str of list")

        base = cutils.handle_kwargs(base, **kwargs)
        response = requests.get(base)

        if response.ok:
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
            base = f"https://api.statbank.dk/v1/tableinfo/{table_id}?format={self.format}"
        else:
            raise ValueError(f"'{str(topics)}' is not a valid topics-list, it must be str.")

        base = cutils.handle_kwargs(base, **kwargs)
        response = requests.get(base)

        if response.ok:
            return metadata_return(response)
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
            print("""
            No variables or values selected! Getting API default
            """)

        if not variables and values:
            print("""
            No variables selected! Using value-dictionary keys as variables
            """)
            variables = list(values.keys())

        if variables and not values:
            print("""
            No values selected! Setting values to all ('*')
            """)
            values = {}
            for i in variables:
                values[i] = ['*']

        # set the base link to get table with id = id
        base = f"http://api.statbank.dk/v1/data/{table_id}/CSV?lang={self.lang}"
        # generate the API call link
        base = cutils.link_generator_with_error_handling(base, variables, values)
        # add kwargs to link
        base = cutils.handle_kwargs(base, **kwargs)
        # get API response
        response = requests.get(base)

        if response.ok:
            return data_return(response)

        else:
            response.raise_for_status()





# The following classes are containers for what the connection returns when used

class data_return:
    """ Contains a dataset

    Attributes:
        raw: raw response
        df: pandas dataframe with the returned content
    """

    def __init__(self, response):
        self.raw = response
        self.df = pd.read_csv(StringIO(self.raw.text), sep = ';')




class metadata_return:
    """ Stores returns from the metadata getter

    Attributes:
        json: json of raw data, quite usefull to look at
        id: ID of table
        description: description of table
        unit: measurement unit of table
        last_updated: last date of update of the table
        active: active status of table
        contacts: contact info on table maintainer if it exists
    """

    def __init__(self, response):
        self.raw = response
        self.json = response.json()

        self.id = self.json['id']
        self.description = self.json['text']
        self.unit = self.json['unit']
        self.last_updated = self.json['updated']
        self.active = self.json['active']

        try:
            self.contacts = self.json['contacts'][0]
        except:
            self.contacts = None

        self.variables = [idx['id'].lower() for idx in self.json['variables']]

        def get_values(self, variable):
            """ get the values for a variable in the dataset
            """
            raise NotImplementedError()




class table_return:
    """ Contains the return of a table call

    Attributes:
        info: dataframe of responses (this is the one you want to see)

        raw: raw response
        json_list: response json
        id_list: table id's
        text_list: table descriptions
        unit_list: table unit of measures
        last_updated_list: date of last updates
        first_list: earliest observation in tables
        last_list: latest observation in tables
        active_list: active status for tables
        vars_list: variables available in tables
    """

    def __init__(self, response):
        self.raw = response
        self.json_list = response.json()

        self.id_list = [json['id'] for json in self.json_list]
        self.text_list = [json['text'] for json in self.json_list]
        self.unit_list = [json['unit'] for json in self.json_list]
        self.last_updated_list = [json['updated'] for json in self.json_list]
        self.first_list = [json['firstPeriod'] for json in self.json_list]
        self.last_list = [json['latestPeriod'] for json in self.json_list]
        self.active_list = [json['active'] for json in self.json_list]
        self.vars_list = [json['variables'] for json in self.json_list]

        self.info = pd.DataFrame(
        {'ID': self.id_list,
        'Description': self.text_list,
        'Variables': self.vars_list,
        'Unit': self.unit_list,
        'Last updated': self.last_updated_list,
        'First observation': self.first_list,
        'Latest observation': self.last_list,
        'Active': self.active_list
        }
        )




class topic_return:
    """ Contains the return of a topic call.

    Attributes:

        info: dataframe of responses (this is the one you want to see)
        json_list: raw response json data
        raw: raw response

        id_list: list of querried ID's
        descriptions: list of descriptions for the ID's
        active_list: active status of each ID
        subtopic_list: list of lists of subtopics
    """

    def __init__(self, response):
        """ Storage for topic returns
        """
        self.raw = response
        self.json_list = response.json()

        self.id_list = [json['id'] for json in self.json_list]
        self.descriptions = [json['description'] for json in self.json_list]
        self.active_list = [json['active'] for json in self.json_list]

        self.subtopic_list = [
            [table['id'] for table in [
                    topic['subjects'] for topic in self.json_list][i]
            ] for i in range(len(self.json_list))
        ]

        self.info = pd.DataFrame({'ID': self.id_list,
                                   'Topic description': self.descriptions,
                                   'Active status': self.active_list,
                                   'Available sub-topics':self.subtopic_list})


    def search_subtopics(self, conn = None, **kwargs):
        """ Searches all the subtopics in table_list

        Args:
            conn: If you want to use an existing connection supply it here.
                  otherwise a default english connection is used
            **kwargs: any kwargs for the connection
        """

        if conn is None:
            conn = connection(language = 'en')

        return conn.get_topics(cutils.flatten(self.subtopic_list), **kwargs)

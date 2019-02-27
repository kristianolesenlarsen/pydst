import pandas as pd
from io import BytesIO, StringIO

# The following classes are containers for what the connection returns when used

class data_return:
    """ Contains a dataset

    Attributes:
        raw: raw response
        df: pandas dataframe with the returned content
    """

    def __init__(self, response, table_id, variables, values):
        self._id = table_id
        self._vars = variables
        self._vals = values
        self.raw = response
        if isinstance(response, BytesIO):
            self.df = pd.read_csv(self.raw, sep = ';')            
        else:
            self.df = pd.read_csv(StringIO(self.raw.text), sep = ';')
        self.dict = self.df.to_dict('list')

    def __repr__(self):
        return f"{self.__class__.__name__}(table_id = '{self._id}', variables = '{str(self._vars)}', values = '{str(self._vals)}')"

    def __str__(self):
        return f"Storage class for the data returned by DST"


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

    def __init__(self, response, table_id):
        self._id = table_id
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

    def __repr__(self):
        return f"{self.__class__.__name__}(table_id = '{self._id}')"

    def __str__(self):
        return f"Storage class for the metadata returned by DST"



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

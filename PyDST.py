import requests
import csv
import os



"""
see http://api.statbank.dk/console#subjects for more examples of usage.
"""


class DST():
    def __init__(self, language = 'en', form = 'JSON'):
        self.lang = language
        self.format = form

    """ getData(): sends a request to DST's API with specified parameters
     - id: table id, a list of available id's can be gained  from .subjects() or the DST website (str)
     - vars: which variables to get (list)
     - values: which levels of each variable to get (dict)
     - **kwargs: other variables passed in the URL, can be for example 'lang=en'

     example request:
     DST().getData("FOLK1A", ["Tid","CIVILSTAND"], {'Tid': ["*"], 'CIVILSTAND': ["TOT","U"]})
     """
    def getData(self, table_id, vars = False, values = False, **kwargs):
        # if vars not set, set it to ''
        #if values is not set, set it to * - meaning get all levels
        if not vars and not values:
            print("""
            No variables or values selected! Getting API deault
            """)
        if not vars and values:
            print("""
            No variables selected! Using value-dictionary keys as variables
            """)
            vars = list(values.keys())
        if vars and not values:
            print("""
            No values selected! Setting values to all ('*')
            """)
            values = {}
            for i in vars:
                values[i] = ['*']

        #set the base link to get table with id = id
        base = 'http://api.statbank.dk/v1/data/{}/CSV?lang={}'.format(table_id, self.lang)
        # generate the API call link
        base = Internals.link_generator_with_error_handling(base, vars, values)
        # add kwargs to link
        link_final = Internals.handle_kwargs(base, **kwargs)
        # get API response
        resp = requests.get(link_final)
        #if we dont succeed print the http error, otherwise spit out data
        return Internals.raise_or_none(resp, 'csv')


    """ table(): get table id's related to the subjects queried
    - subjects: a list of subjects given by their subject id
    """
    def table(self, subjects, **kwargs):
        if type(subjects) == str:
            subjects = [subjects]
        base = 'http://api.statbank.dk/v1/tables?lang={}&format={}&subjects='.format(self.lang, self.format)
        # add subjects to link and optional URL params
        link_final = Internals.handle_kwargs(''.join([base, ','.join(subjects)]), **kwargs)
        # get API response and return
        resp = requests.get(link_final)
        return Internals.raise_or_none(resp, 'json')


    """ subject(): get broad subject category information
     - id: subject area ID (usually a two digit number) (str)
     - **kwargs: other parameters to be passed in the URL like 'format', 'lang','recursive' etc
    """
    def subject(self, id, **kwargs):
        base = 'http://api.statbank.dk/v1/subjects/'
        form = '?lang={}&format={}'.format(self.lang, self.format)
        # base URL
        link = base + id + form
        # add kwargs to link and get it
        link = Internals.handle_kwargs(link, **kwargs)
        resp = requests.get(link)
        return Internals.raise_or_none(link, 'json')


    """ metadata(): Acces metadata about tables
     - id: table id, for example 'folk1a' (str)
     - output_format: how much metadata do you want? opions are full, variables and values
     - **kwargs: URL variables.
    """
    def metadata(self, id, output_format = 'full', **kwargs):
        base = 'http://api.statbank.dk/v1/tableinfo/'
        form = '?lang={}&format={}'.format(self.lang, self.format)
        # gen baselink and add kwargs
        link = base + id + form
        link = Internals.handle_kwargs(link, **kwargs)

        respJSON = requests.get(link).json()

        # give full output
        if output_format == 'full':
            return respJSON

        # give variables
        elif output_format == 'variables':
            output = {'variables': []}
            for i in range(0,len(x['variables']) - 1):
                output['variables'].append(x['variables'][i]['id'])
            return output

        # give variable-value dict
        elif output_format == 'values':
            output = {}
            for i in range(0,len(x['variables']) - 1):
                ID = x['variables'][i]['id']
                values = []
                for j in range(0, len( x['variables'][i]['values']) - 1):
                    values.append(x['variables'][i]['values'][j]['id'])
                output[ID] = values
            return output
        # if you dont select you get nothing
        else:
            print("""
            Bad output format
            """)
            return None


    """ toCSV(): you guessed it.
     - table: output from table()
     - name: intended filename [without '.csv'!]
    """
    def toCSV(self, table, name):
        table = table.text.replace(",","-")

        fileName = name +".csv"
        if not os.path.exists(fileName):
            open(fileName,'w+').close()

        with open(fileName,'w') as curCSV:
            writer = csv.writer(curCSV, delimiter = ',', lineterminator = "\n")
            for row in table[1:].split("\r\n"):
                writer.writerow([row])
            print("Finished saving files from",name ,"to drive")



""" Internals():
    is a class purely created to have storage for functions that are used repeatedly in the DST() class
"""
class Internals():
    """ raise_or_none(): handles http errors
     - response: a resquests.get() answer
     - output: 'csv' or 'json'
    """
    @staticmethod
    def raise_or_none(response, output):
        try:
            response.raise_for_status()
            if output == 'csv':
                return response.text
            if output == 'json':
                return response.json()
        except requests.exceptions.HTTPError as err:
            print(err)
            return None


    """ handleKwargs(): simply adds optional parameters to the URL
     - link: a link to add params to
     - **kwargs
    """
    @staticmethod
    def handle_kwargs(link, **kwargs):
        for k, v in kwargs.items():
            link = link + '&{}={}'.format(k, v)
        return link

    @staticmethod
    def link_generator_with_error_handling(base, vars, values):
        # if neither vars or values, do nothing
        if not vars and not values:
            return base
        # otherwise produce the link
        else:
            for i in vars:
                base = base + "&" + i + "="
                try:
                    for j in values[i]:
                        base = base + j + ','
                except KeyError:
                    base = base + "*,"
                    print("No values at", i,"setting values to all")
                base = base[:-1]
        return base

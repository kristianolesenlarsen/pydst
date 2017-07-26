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
#        super().__init__()
    """ getData(): sends a request to DST's API with specified parameters
     - id: table id, a list of available id's can be gained  from .subjects() or the DST website (str)
     - vars: which variables to get (list)
     - values: which levels of each variable to get (dict)
     - **kwargs: other variables passed in the URL, can be for example 'lang=en'

     example request:
     dst.getData("FOLK1A", ["Tid","CIVILSTAND"], {'Tid': ["*"], 'CIVILSTAND': ["TOT","U"]})
     """
    def getData(self, id, vars = False, values = False, **kwargs):
        # TODO: tolower alt
        # if vars not set, set it to ''
        if not vars:
            print('''
            no variables selected - choose variables with dst.metadata()
            Setting vars to API default
            ''')
            vars = ''
        #if values is not set, set it to * - meaning get all levels
        if not values:
            print('''
            No values selected - setting values to all
            ''')
            values = {}
            for i in vars:
                values[i] = ['*']
        #set the base link to get table with id = id
        base = 'http://api.statbank.dk/v1/data/'
        form = '/CSV?lang={}'.format(self.lang)

        baseLink = base + id + form
        # generate the API call link
        baseLink = self.linkGenerator_withErrorHandling(baseLink, vars, values)
        # add kwargs to link
        baseLink = Internals.handleKwargs(baseLink, **kwargs)
        # get API response
        resp = requests.get(baseLink)
        #if we dont succeed print the http error, otherwise spit out data
        return Internals.raiseOrNone(resp, 'csv')
        """
        try:
            resp.raise_for_status()
            return resp.text

        except requests.exceptions.HTTPError as err:
            print(err)
            return None
        """

    """ table(): get table id's related to the subjects queried
    - subjects: a list of subjects given by their subject id
    """
    def table(self, subjects, **kwargs):
        if type(subjects) == str:
            subjects = [subjects]
        base = 'http://api.statbank.dk/v1/tables?lang={}&format={}&subjects='.format(self.lang, self.format)
        for i in subjects:
            base = base + i + ','
        base = base[:-1]
        #optional URL params
        for i in kwargs.items():
            base = base + '&{}={}'.format(i[0],i[1])

        return requests.get(base).json()


    """ linkGenerator_withErrorHandling(): generates valid URL's from vars and values.
     - base: baselink (str)
     - vars: variables to be requested (list)
     - values: values of each variable (dict)
    failing to specify vars is caught by the initial error check in table(), however this captures partial mistakes in values specification. Used internally.
    """
    def linkGenerator_withErrorHandling(self, base, vars, values):
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



    """ subject(): get broad subject category information
     - id: subject area ID (usually a two digit number) (str)
     - **kwargs: other parameters to be passed in the URL like 'format', 'lang','recursive' etc
    """
    def subject(self, id, **kwargs):
        base = 'http://api.statbank.dk/v1/subjects/'
        form = '?lang={}&format={}'.format(self.lang, self.format)

        link = base + id + form

        for i in kwargs.items():
            link = link + '&{}={}'.format(i[0],i[1])

        return requests.get(link).json()


    """ metadata(): Acces metadata about tables
     - id: table id, for example 'folk1a' (str)
     - **kwargs: URL variables.
    """
    def metadata(self, id, **kwargs):
        base = 'http://api.statbank.dk/v1/tableinfo/'
        form = '?lang={}&format={}'.format(self.lang, self.format)

        link = base + id + form

        for i in kwargs.items():
            link = link + '&{}={}'.format(i[0],i[1])

        respJSON = requests.get(link).json()['variables']
        print("There are ", len(respJSON), "variables in ", id, "- acces them with [n]")

        return respJSON

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



class Internals():
    """ raiseOrNone(): handles http errors
     - response: a resquests.get() answer
     - output: 'csv' or 'json'
    """
    @staticmethod
    def raiseOrNone(response, output):
        try:
            response.raise_for_status()
            if output == 'csv':
                return response.text
            if output == 'json':
                return response.json()
        except requests.exceptions.HTTPError as err:
            print(err)
            return None


    """
    """
    @staticmethod
    def handleKwargs(link, **kwargs):
        for i in kwargs.items():
            link = link + '&{}={}'.format(i[0],i[1])
        return link





""" helpers(): small helper functions that make it easier to take full advantage of the API
"""
class helpers():
    def generateSum(sumDict, text = 'sum', code = False):
        sumList = []
        for i in sumDict:
            sumstr = 'sum({}='.format(i)
            for j in sumDict[i]:
                sumstr = sumstr + j + ';'
            sumstr = sumstr[:-1] + ')'
            sumList.append(sumstr)

        out = ','.join(sumList)
        return out

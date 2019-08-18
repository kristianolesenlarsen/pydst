
''' 
This is the base class for the interface with the 
Statistics Denmark API. 

This class does not handle converting the results 
to pandas DataFrames. Instead it either a requests
response object or a bytes object, in the case of 
streaming download.
'''

import io
import requests

from .query import prepare_request, send_request


class StatBank:

    def __init__(self,
                 fmt = 'json', 
                 lang = 'en', 
                 session = None,
                 stream = False,
                 chunk_size = 2048,
                 ):
        ''' 
        An interface to the API of Statistics Denmark.

        Parameters
        ----------
        fmt 
            The format to retrieve data in. Defaults to JSON.
        lang
            Language of retrieved material (da/en): Defaults to english (en).

        session
            A requests session to be used for making all requests. Is left as 
            None by default in which case a session is created automatically.

        stream
            Should the data be streamed, defaults to False.

        chunk_size
            The chunk size to use if streaming. Defaults to 2048.
        '''
        self.fmt = fmt 
        self.lang = lang 
        self.baseopts = {'lang': self.lang, 'format': self.fmt}

        self.stream = stream
        if self.fmt.lower() == 'bulk':
            self.stream = True 
        self.csize = chunk_size

        if session is None:
            self.session = requests.Session()
        else:
            self.session = session


    def __repr__(self):
        return f'{self.__class__.__name__}(fmt={self.fmt}, lang={self.lang}, stream={self.stream}, chunk_size={self.csize})'


    def __str__(self):
        return f"{self.__class__.__name__}, streaming is {'on' if self.stream else 'off'}"


    def data(self, table, variables, **options):
        ''' 
        Retrieve data from the /data endpoint of the DST api.

        Parameters
        ----------
        table str  
            ID of the table to pull data from. E.g. ``'FOLK1A'``

        variables dict
            A dictionary with variable names as keys and the values to select as
            values. For example ``{'Tid': ['2008k1', '2008k2']}`` selects only 
            observations where ``Tid`` is either of the two values in the 
            supplied list.

        **options
            See below.

        Keyword Arguments
        -----------------
            delimiter str
                Delimiter to use (only valid if ``format=csv``)
            valuePresentation str 
                Presentation of values as codes or values. Valid options are 
                ``'Code'``, ``'Value'`` and ``'CodeAndValue'``.
            timeOrder str:
                Time order of observations. Either Ascending or Descending

        Returns 
        -------
        Union[requests.models.Response, io.BytesIO]
            Either a requests response or BytesIO (if streaming is set to True)        
        '''
        fmt = 'jsonstat' if self.fmt == 'json' else self.fmt

        request = prepare_request('data', table, fmt, **{'lang': self.lang, **options ,**variables})
        response = send_request(self.session, request, self.stream, self.csize)

        return response


    def subjects(self, subjects, **options):
        ''' Retrieve data from the /subjects endpoint of the 
            DST api.

        Parameters
        ----------
        Subjects list/str
            Either a single subject code supplied as a string (e.g. ``02``) or a
            sequence of such subject codes supplied as a list.
        
        **options
            See below.

        Keyword Arguments
        -----------------
            recursive bool
                Set true to recursively get sub-subjects.
            omitSubjectsWithoutTables bool 
                Set True to omit subjects without any tables.
            includeTables bool
                Include table IDs in the result set.

        Returns 
        -------
        requests.models.Response
            A requests response object.
        '''
        subs = ','.join(subjects) if type(subjects) == list else subjects
        request = prepare_request('subjects', subs, **{**self.baseopts, **options})
        response = send_request(self.session, request, False)
        
        return response


    def tables(self, subjects, **options):
        ''' Retrieve data from the /tables endpoint of the DST api.   

        Parameters
        ----------
        Subjects list/str
            Either a single subject code supplied as a string (e.g. ``02``)
            or a sequence of such subject codes supplied as a list.
        
        **options
            See below.

        Keyword Arguments
        -----------------
            pastDays int
                Set True to only include tables updated since pastDays.
            includeInactive bool 
                Set True to include discontinued tables.

        Returns 
        -------
        requests.models.Response
            A requests response object.
        '''
        subs = {'subjects': ','.join(subjects) if type(subjects) == list else subjects}
        request = prepare_request('tables', **{**subs, **options, **self.baseopts})
        response = send_request(self.session, request, False)

        return response


    def metadata(self, table):
        ''' Retrieve data from the /tableinfo endpoint of the DST api.

        Parameters
        ----------
        table str  
            ID of the table to pull data from. E.g. ``'FOLK1A'``

        Returns
        -------
        requests.models.Response
            A requests response object.        
        '''

        request = prepare_request('tableinfo', table, **{'format':self.fmt})
        response = send_request(self.session, request, False)

        return response
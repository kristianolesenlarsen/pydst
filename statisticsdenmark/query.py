
''' 
This module constructs and sends queries to the DST api. Most users should not 
need to use any functionality directly from this module - instead they can 
interface with the DST API through the StatBank class.
'''

import io 
from requests import Request
from urllib.parse import urljoin


def prepare_request(*path, **params):
    ''' Prepare a request to the API.

    Parameters
    ----------
    *path str[]
        Any number of _ordered_ path elements to append to the base url. The 
        base is https://api.statbank.dk/v1/, so to access the /data/tableid 
        endpoint you sould call `prepare_request('data', 'tableid')`.

    **params
        Any number of key-value pairs of parameters to pass in the url. For 
        instance `prepare_request(a=1,b=2)` results in an url with appended 
        options `'a=1&b=2'`.

    Returns
    -------
    requests.models.PreparedRequest
        A prepared request ready to be send via `send_request()`.
    '''
    url = urljoin('https://api.statbank.dk/v1/', '/'.join(path))
        
    if params:
        url = Request('GET', url, params = params).prepare()
    else:
        url = Request('GET', url).prepare()
        
    return url
    
    
def send_request(session, 
                 request, 
                 stream = False, 
                 chunk_size = 2048):
    ''' Send a previously prepared request to the api.

    Parameters
    ----------
    session
        A requests `Session()` instance used to send the requests.
    
    request
        A prepared request manufactured either directly by requests, or more 
        commonly by `prepare_request()`

    stream bool
        Should the data be retrieved over a streaming connection? This is useful
         when retrieving large datasets.

    chunk_size:
        Chunk size to use if streaming.

    Returns
    -------
    Union[requests.models.Response, io.BytesIO]
        Either a requests response or BytesIO (if streaming is set to True)        
    '''
    if stream:
        with session.send(request, stream = stream) as response:
            response.raise_for_status()
            with io.BytesIO() as mem_obj:
                for chunk in response.iter_content(chunk_size):
                    mem_obj.write(chunk)
                mem_obj.seek(0)
            return mem_obj
    else:
        response = session.send(request)
        response.raise_for_status()
        return response

import requests
import io 

from requests import Session, Request
from urllib.parse import urljoin


def prepare_request(*path, **params):
    ''' Prepare a request to the API.
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
    ''' Send a previously prepared request to
        the api.
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

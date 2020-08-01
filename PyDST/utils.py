
def coerce_input_to_str(data):
    ''' Coerce url data to a comma separated string.
        e.g. ['a','b'] becomes 'a,b' while 'c,d' is
        unchanged.

        Parameters
        ----------
        data (str/list/tuple): input data to coerce.

        Returns:
        --------
        str
    '''
    if isinstance(data, str):
        return data
    elif isinstance(data, (list, tuple)):
        return ','.join(data)
    raise ValueError(f'{data} is not a valid input.')


def list_from_comma_separated_string(s):
    ''' Convert a comma separated string such
        as '1,2,3' to a list.

        Parameters
        ----------
        s (str): string.

        Returns
        -------
        list
    '''
    return s.replace(' ', '').split(',')



def add_url_parameters(url, **parameters):
    ''' Add url parameters to the base url.

        Parameters
        ----------
        url (str): base url.

        Keyword Arguments
        -----------------
        **parameters: key-value pairs of the 
            url parameters to add. If the value
            is None, the pair is not added.
        
        Returns
        -------
        str
    '''
    parameters = {k:v for k,v in parameters.items() if v is not None}
    if len(parameters) == 0:
        return url
    parameters = '&'.join([f'{k}={v}' for k,v in parameters.items()])
    return f'{url}?{parameters}'
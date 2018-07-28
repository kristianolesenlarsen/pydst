import requests
import pandas



flatten = lambda l: list(set([item for sublist in l for item in sublist]))



def coerce_input_type_to_str(input):
    """ Checks if a input is string or can be coerced to one.
    """
    if isinstance(input, str):
        output = input
    elif isinstance(input, list):
        output = ','.join(input)
    else:
        raise ValueError(f"'{topics}' is not a valid topics-list, it must be str of list")
    return output


def raise_or_none(response, output):
    """ handle http errors
     - response: a resquests.get() answer
     - output: 'csv' or 'json'
    """
    try:
        response.raise_for_status()
        if output == 'csv':
            return response.text
        if output == 'json':
            return response.json()
    except requests.exceptions.HTTPError as err:
        print(err)
        return None



def handle_kwargs(link, **kwargs):
    """ Add optional parameters to a URL

     - link: a link to add params to
     - **kwargs
    """
    for k, v in kwargs.items():
        link = link + '&{}={}'.format(k, v)
    return link



def list_from_comma_separated_string(s, error):
    """ Tries to split a string at the commas. Raises an error if this is not
    possible.
    """
    try:
        s = [var.strip() for var in s.split(',')]
    except AttributeError:
        raise AttributeError(error)
    return s


def link_generator_with_error_handling(base, vars, values):
    """ Generate urls to send of to DST

    the error handling part simply takes care of missing vars or values
    """
    # if neither vars or values, do nothing
    if not vars and not values:
        return base
    # otherwise produce the link
    else:

        # first lets allow both 'a,b,c' and ['a','b','c'] for variables
        if not isinstance(vars, list):
            vars = list_from_comma_separated_string(vars, f"{str(vars)} is not a valid variable list. Must be str separated by commas or list.")

        if not isinstance(values, dict):
            raise TypeError('Values must be suplied as a dict.')

        # Then make sure all values are supplied as lists
        for var,value in values.items():
            if not isinstance(value, list):
                values[var] = list_from_comma_separated_string(value, f"{str(value)} is not a valid sequence of values.")


        for i in [var.lower() for var in vars]:
            base = base + "&" + i + "="
            try:
                for j in {k.lower(): v for k, v in values.items()}[i]:
                    base = base + j + ','
            except KeyError:
                base = base + "*,"
                print("No values specificed for", i,"setting values to all ('*')")
            base = base[:-1]
    return base



def validate_language(language):
    """ Is the language valid?
    """
    if language in ['da', 'en']:
        return language
    else:
        raise ValueError("Language '{l}' is not a valid language. Use 'da' or 'en'".format(language))

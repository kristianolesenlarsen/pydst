import requests
import pandas



flatten = lambda l: list(set([item for sublist in l for item in sublist]))


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



def link_generator_with_error_handling(base, vars, values):
    """ Generate urls to send of to DST

    the error handling part simply takes care of missing vars or values
    """
    # if neither vars or values, do nothing
    if not vars and not values:
        return base
    # otherwise produce the link
    else:
        for i in [var.lower() for var in vars]:
            base = base + "&" + i + "="
            try:
                for j in {k.lower(): v for k, v in values.items()}[i]:
                    base = base + j + ','
            except KeyError:
                base = base + "*,"
                print("No values at", i,"setting values to all")
            base = base[:-1]
    return base



def validate_language(language):
    """ Is the language valid?
    """
    if language in ['da', 'en']:
        return language
    else:
        raise ValueError("Language '{l}' is not a valid language. Use 'da' or 'en'".format(language))

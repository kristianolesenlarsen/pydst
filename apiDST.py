import requests
import csv
import os

# table(): sends a request to DST's API with specified parameters
# example request:
# dst.table("FOLK1A", ["Tid","CIVILSTAND"], {'Tid': ["*"], 'CIVILSTAND': ["TOT","U"]})



def table(id, vars = False, values = False, **kwargs):
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
    form = '/CSV?lang=en'

    baseLink = base + id + form

    for i in kwargs.items():
        baseLink = baseLink + '&{}={}'.format(i[0],i[1])

    # generate the final API call link and print it, return what the API sends back
    baseLink = linkGenerator_withErrorHandling(baseLink, vars, values)
    print(baseLink)
    return requests.get(baseLink)

# failing to specify vars is caught by the initial error check in table(),
#this captures partial mistakes in values specification
def linkGenerator_withErrorHandling(base, vars, values):
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


def subject(id, **kwargs):
    base = 'http://api.statbank.dk/v1/subjects/'
    form = '?lang=en&format=JSON'

    link = base + id + form

    for i in kwargs.items():
        link = link + '&{}={}'.format(i[0],i[1])

    return requests.get(link).json()

def metadata(id, **kwargs):
    base = 'http://api.statbank.dk/v1/tableinfo/'
    form = '?lang=en&format=JSON'

    link = base + id + form

    for i in kwargs.items():
        link = link + '&{}={}'.format(i[0],i[1])

    respJSON = requests.get(link).json()['variables']
    print("There are ", len(respJSON), "variables in ", id, "- acces them with [n]")

    return respJSON


def toCSV(table, name):
    table = table.text.replace(",","-")

    fileName = name +".csv"
    if not os.path.exists(fileName):
        open(fileName,'w+').close()

    with open(fileName,'w') as curCSV:
        writer = csv.writer(curCSV, delimiter = ',', lineterminator = "\n")
        for row in table[1:].split("\r\n"):
            writer.writerow([row])
        print("Finished saving files from",name ,"to drive")

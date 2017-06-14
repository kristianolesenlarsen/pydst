import requests
import csv
import os

# table(): sends a request to DST's API with specified parameters
# example request:
# dst.table("FOLK1A", ["Tid","CIVILSTAND"], {'Tid': ["*"], 'CIVILSTAND': ["TOT","U"]})

def table(id, vars = False, values = False):
        # TOdo: tolower alt

    if not vars:
        print('''
        no variables selected - choose variables with dst.metadata()
        Setting vars to API default
        ''')
        vars = ''

    if not values:
        print('''
        No values selected - setting values to API default
        ''')
        values = {}
        for i in vars:
            values[i] = ['*']

    base = 'http://api.statbank.dk/v1/data/'
    form = '/CSV?lang=en'

    baseLink = base + id + form

    for i in vars:
        baseLink = baseLink + "&" + i + "="
        for j in values[i]:
             baseLink = baseLink + j + ','
        baseLink = baseLink[:-1]
    print(baseLink)
    return requests.get(baseLink)


def subject(id):
    base = 'http://api.statbank.dk/v1/subjects/'
    form = '?lang=en&format=JSON'

    link = base + id + form
    respJSON = requests.get(link).json()

    return respJSON

def metadata(id):
    base = 'http://api.statbank.dk/v1/tableinfo/'
    form = '?lang=en&format=JSON'

    link = base + id + form
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
        print("Finished saving files to drive")

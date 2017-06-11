import requests
import csv
import os

class dst():

    def table(id, vars = False):

        if not vars:
            print("no variables selected - choose variables with dst.metadata()")
            return False

        base = 'http://api.statbank.dk/v1/data/'
        form = '/CSV?lang=en'

        baseLink = base + id + form
        for i in vars:
            baseLink = baseLink + "&" + i + "=*"

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
        fileName = name +".csv"
        if not os.path.exists(fileName):
            open(fileName,'w+').close()

        with open(fileName,'w') as curCSV:
            writer = csv.writer(curCSV, delimiter = ',', lineterminator = "\n")
            for row in table.split("\r\n"):
                writer.writerow([row])



getList = [["name", ["varlist"]],
           ["name", ["varlist"]],
           ["name", ["varlist"]],
           ["name", ["varlist"]],
          ]


for i in getList:
    dstReturn = dst.table(i[0],i[1])
    dst.toCSV(dstreturn, i[0])

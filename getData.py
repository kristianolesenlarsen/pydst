import requests
import csv
import os

class dst():

    def table(id, vars = False, values = False):
        if not values:
            print('''
            No values selected - setting values to all
            ''')
            for i in values:
                i = ["*"]

        if not vars:
            print('''
            no variables selected - choose variables with dst.metadata()
            Setting vars to API default
            ''')
            vars = ''

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


getList = [["NAN1", ["TRANSAKT","PRISENHED","Tid"]],
           ["FOLK1A", ["varlist"]]
          ]

dst.table("FOLK1A", ["Tid","CIVILSTAND"], {'Tid': ["*"], 'CIVILSTAND': ["TOT","U"]})

dst.metadata("FOLK1A")

#st.metadata("FOLK1A")

for i in getList:
    dstReturn = dst.table(i[0],i[1])
    dst.toCSV(dstReturn, i[0])

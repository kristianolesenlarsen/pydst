import schedule
import time
import sys
import os
sys.path.append(os.getcwd())

import getData as dst


#define list of vars to get
getList = [["NAN1", ["TRANSAKT","PRISENHED","Tid"], {'Tid': ['*'], 'TRANSAKT': ['B1GQK', 'P7K'], 'PRISENHED': ['V_M','LAN_M']}],
           ["FOLK1A", ["Tid","KØN"]],
           ['AKU100',['Tid', 'BESKSTATUS','ALDER'], {'Tid': ['*'], 'BESKSTATUS': ['BESTOT','AKUL', 'UARBST'], 'ALDER': ['1524','3544','5564']}],
           ['PRIS112', ['Tid','HOVED'], {'Tid': ['*'], 'HOVED': ['1005']}]
          ]

update_all(getList)

# update all datasets with with the code currently tested in getData
def update_all(get_list):
    for i in get_list:
        try:
            i1 = i[1]
        except IndexError:
            i1 = False
        try:
            i2 = i[2]
        except IndexError:
            i2 = False
        dstReturn = dst.table(i[0],i1,i2)
        dst.toCSV(dstReturn, i[0])

# run update_all once every month/whatever
schedule.every().day.at("14:40").do(update_all, getList)

while True:
    schedule.run_pending()
    time.sleep(1)

#TODO: get this script to time the run of a Rmd file as well, which is pushed to github.io

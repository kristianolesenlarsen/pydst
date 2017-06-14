import schedule

import sys
import os
sys.path.append(os.getcwd())

import getData as dst


#define list of vars to get
getList = [["NAN1", ["TRANSAKT","PRISENHED","Tid"]],
           ["FOLK1A", ["Tid","KØN"]]
          ]

# update all datasets with with the code currently tested in getData
def update_all(list):
    for i in list:
        dstReturn = dst.table(i[0],i[1])
        dst.toCSV(dstReturn, i[0])

#update_all(getList)
# run update_all once every month/whatever
schedule.every.day.at("13:00").do(update_all, getList)


#TODO: get this script to time the run of a Rmd file as well, which is pushed to github.io

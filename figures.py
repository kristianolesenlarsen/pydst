import pandas as pd
import matplotlib.pyplot as plt
import numpy as np
import matplotlib as mpl


nan1 = pd.read_csv("NAN1.csv", sep = ";", na_values = "..", dtype = {'TRANSAKT': str, 'PRISENHED': str,  'INDHOLD': float}, parse_dates = ['TID'])
aku100 = pd.read_csv("AKU100.csv", sep = ";", na_values = "..", dtype = {'BESKSTATUS': str, 'ALDER': str, 'INDHOLD': float},parse_dates = ['TID'])
pris112 = pd.read_csv("PRIS112.csv", sep = ";", na_values = "..", dtype = {'HOVED': str, 'ALDER': str, 'INDHOLD': float},parse_dates = ['TID'])


replacements_NAN1_TRANS = {
'TRANSAKT': {'B.1*g Gross domestic product': 'GDP',
           'P.7 Imports of goods and services': 'ImpGoodsServices'}}

replacements_NAN1_PRIS = {
'PRISENHED': {'Current prices- (bill. DKK.)': 'currentPrices',
       '2010-prices- chained values- (bill. dkk.)': 'chainedPrices'}}

#replace some of the column values
nan1 = nan1.replace(replacements_NAN1_TRANS).replace(replacements_NAN1_PRIS)
#drop unnessecary rows in column TRANSAKT

'''
PLOT GDP
'''
dat_gdp = nan1[nan1.TRANSAKT == 'GDP']
dat_gdp = dat_gdp[(dat_gdp.PRISENHED == 'chainedPrices') | (dat_gdp.PRISENHED == 'currentPrices')]

for key, grp in dat_gdp.groupby(['PRISENHED']):
    plt.plot( grp['TID'], grp['INDHOLD'], label=key)
plt.legend(loc='best')
plt.title("GDP")

plt.savefig('gdp.png')
plt.show()

'''
GDP + CPI
'''

mergeNANPRIS = pd.merge(dat_gdp[dat_gdp.PRISENHED == 'currentPrices'], pris112, on='TID', how='left')


fig, ax1 = plt.subplots()
ax2 = ax1.twinx()
#plt.axis('normal')
ax1.plot(mergeNANPRIS.TID, mergeNANPRIS.INDHOLD_x)
ax2.plot(mergeNANPRIS.TID, mergeNANPRIS.INDHOLD_y, color = 'g')
ax1.set_ylabel('CPI', color='g')
ax2.set_ylabel('GDP current prices', color='b')

plt.show()




'''
PLOT AKU
'''
# by age
for i in aku100.ALDER.unique():
    for key, grp in aku100[aku100.ALDER == i].groupby(['BESKSTATUS']):
        plt.plot(grp['TID'], grp['INDHOLD'], label = key)
        plt.legend(loc = 'best')
        plt.title("Employment status " + i)
    plt.show()


# by employment state
for i in aku100.BESKSTATUS.unique():
    for key, grp in aku100[aku100.BESKSTATUS == i].groupby(['ALDER','BESKSTATUS']):
        plt.plot(grp['TID'], grp['INDHOLD'], label = key)
        plt.legend(loc = 'best')
    plt.show()

import pandas as pd
import matplotlib.pyplot as plt
import numpy as np

nan1 = pd.read_csv("NAN1.csv", sep = ";", na_values = "..", dtype = {'TRANSAKT': str, 'PRISENHED': str, 'TID': int, 'INDHOLD': float})

replacements_TRANS = {
'TRANSAKT': {'B.1*g Gross domestic product': 'f_GDP',
           'P.7 Imports of goods and services': 'f_ImpGoodsServices',
           'Supply': 'f_supply',
           'P.6 Exports of goods and services': 'f_expGoodsServices',
           'P.31 Private consumption': 'f_privConsumption',
           'P.31 Household consumption expenditure': 'f_hhConsumption',
           'Purchase of vehicles': 'f_impVehicles',
           'P.3 Government consumption expenditure': 'f_govExpenditure',
           'P.5g Gross capital formation': 'f_grossCapitalForm',
           'N.117 Intellectual property products': 'f_interlectProp',
           'P.52 Changes in inventories': 'f_inventoryChanges',
           'Final domestic demand': 'f_domestDemand',
           'Final demand': 'f_demand',
           'Total actual hours worked (million hours)': 'f_hoursWorked',
           'Total employment (1-000 persons)': 'f_employment'} }

replacements_PRIS = {
'PRISENHED': {'Current prices- (bill. DKK.)': 'curPrices',
       '2010-prices- chained values- (bill. dkk.)': 'chainPrices',
       'Period-to-period real growth in per cent': 'P2PGrowth',
       'Pr. capita. Current prices- (1000 DKK.)': 'capitaCurPrices',
       'Contribution to GDP growth- (percentage point)': 'GDPcontribution',
       'Pr. capita- 2010-prices- chained values- (1000 DKK.)': 'capitaChainedPrices'}}


#replace some of the column values
nan1 = nan1.replace(replacements_TRANS)
nan1 = nan1.replace(replacements_PRIS)
#drop unnessecary rows in column TRANSAKT
nan1 = nan1[nan1.TRANSAKT.str.contains("f_") == True]

'''
PLOT GDP
'''
dat_gdp = nan1[nan1.TRANSAKT == 'f_GDP']
dat_gdp = dat_gdp[(dat_gdp.PRISENHED == 'capitaChainedPrices') | (dat_gdp.PRISENHED == 'capitaCurPrices')]

dat_gdp.groupby('PRISENHED')

for key, grp in dat_gdp.groupby(['PRISENHED']):
    plt.plot( grp['TID'], grp['INDHOLD'], label=key)
plt.legend(loc='best')
plt.show()


plt.plot()

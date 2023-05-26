# -*- coding: utf-8 -*-
"""
Created on Tue Jun 15 13:29:17 2021

@author: ZKS0291
"""

from selenium import webdriver
from selenium.webdriver.support.select import Select
import numpy as np
import matplotlib.pyplot as plt
import pandas as pd
import time
import os
os.chdir('//tedfil01/datadropdev/PythonPOC')
import VaRStats as vs
from HistoricalImpVol import OptionVols
import streamlit as st
from io import BytesIO
from datetime import datetime

now = datetime.now()
current_time = now.strftime("%H:%M:%S")
current_time = datetime.strptime(current_time, '%H:%M:%S')

firstTime = datetime.strptime('08:00:00', '%H:%M:%S')
lastTime = datetime.strptime('13:30:00', '%H:%M:%S')

if current_time > firstTime and current_time < lastTime:

    st.title('Option Vol Curves')
    
    websiteList = ['https://www.barchart.com/futures/quotes/ZC*0/options', 'https://www.barchart.com/futures/quotes/ZSQ21/options/aug-21', 
                   'https://www.barchart.com/futures/quotes/KEU21/options', 'https://www.barchart.com/futures/quotes/ZWU21/options']
    expirationMonth = [['Aug 2021','Sep 2021','Dec 2021','Mar 2022','May 2022','Jul 2022','Sep 2022','Dec 2022','Jul 2023','Dec 2023'],
                      ['Aug 2021','Sep 2021','Nov 2021','Jan 2022','Mar 2022','May 2022','Jul 2022','Aug 2022','Nov 2022'], 
                      ['Aug 2021','Sep 2021','Dec 2021','Mar 2022','May 2022','Jul 2022'], ['Aug 2021','Sep 2021','Dec 2021','Mar 2022','May 2022','Jul 2022']]
    commodityList = ['Corn','Soybeans','Hard Wheat','Soft Red Wheat']
    
    for x in range(len(expirationMonth)):
    
        finalOptionsDF = pd.DataFrame()
        
        for expiration in expirationMonth[x]:
        
            driver = webdriver.Edge('D:/WebDrivers/msedgedriver.exe')
            driver.set_window_position(0,0)
            driver.set_window_size(1800,768)
            URL = websiteList[x]
            driver.get(URL)
            
            selectorExpiration = driver.find_elements_by_xpath("//*[@id='bc-options-toolbar__dropdown-month']")
            selectExpiration = Select(selectorExpiration[0])
            selectExpiration.select_by_visible_text(expiration)
            
            time.sleep(2)
            
            selectorStrike = driver.find_elements_by_xpath("//*[@class='bc-dropdown styled in-the-money']/select")
            selectorStrike = Select(selectorStrike[0])
            selectorStrike.select_by_visible_text("Show All")
            
            time.sleep(4)
            
            optionsTable = driver.find_elements_by_xpath("//*[@class='bc-table-scrollable']")
            optionsTable = optionsTable[0].text.split("\n")
            optionsTable = optionsTable[2:-1]
            
            commodity = driver.find_elements_by_xpath("//*[@id='bc-options-toolbar__dropdown-month']")
            selectExpiration = Select(commodity[0])
            commodity = selectExpiration.first_selected_option
            commodity = commodity.text
            
            futurePrice = driver.find_elements_by_xpath("//*[@class='pricechangerow']/span")
            futurePrice = futurePrice[0].text
        
            element = driver.find_elements_by_xpath("//*[@class='column small-12 medium-4']/div/strong")
            expiration = element[1].text
            dte = element[0].text
                
            driver.quit()
            
            optionsList = []
            
            for i in range(0,len(optionsTable),11):
                temp = []
                for j in range(i,i+11):
                   temp.append(optionsTable[j])
                temp.insert(0, commodity)
                temp.append(futurePrice)
                temp.append(expiration)
                temp.append(dte)
                optionsList.append(temp)
            
            optionsDF = pd.DataFrame(optionsList)
            optionsColumns = ['Description','Strike','High','Low','Last','Change','Bid','Ask','Volume','Open Int','Premium','Last Trade','Future Price','Expiration','DTE']
            optionsDF.columns = optionsColumns
            
            finalOptionsDF = pd.concat([finalOptionsDF, optionsDF])
            
        del finalOptionsDF['High']
        del finalOptionsDF['Low']
        del finalOptionsDF['Change']
        del finalOptionsDF['Premium']
        
        finalOptionsDF = finalOptionsDF[finalOptionsDF['Bid'] != "N/A"]
        finalOptionsDF = finalOptionsDF[finalOptionsDF['Ask'] != "N/A"]
        
        finalOptionsDF[['Strike','PriceType']] = finalOptionsDF['Strike'].str.split('-', expand=True)
        finalOptionsDF['PriceType'] = finalOptionsDF['PriceType'].str[1:]
        
        finalOptionsDF[['Last1','Last2']] = finalOptionsDF['Last'].str.split('-', expand=True)
        finalOptionsDF['Last2'] = finalOptionsDF['Last2'].apply(lambda x: x[:-1] if 's' in x else x)
        finalOptionsDF['Last2'] = pd.to_numeric(finalOptionsDF['Last2']) / 8
        finalOptionsDF['Last2'] = finalOptionsDF['Last2'].astype(str)
        finalOptionsDF['Last2'] = finalOptionsDF['Last2'].str[1:]
        finalOptionsDF['Last'] = finalOptionsDF['Last1'] + finalOptionsDF['Last2']
        del finalOptionsDF['Last1']
        del finalOptionsDF['Last2']
        
        finalOptionsDF[['Bid1','Bid2']] = finalOptionsDF['Bid'].str.split('-', expand=True)
        finalOptionsDF['Bid2'] = pd.to_numeric(finalOptionsDF['Bid2']) / 8
        finalOptionsDF['Bid2'] = finalOptionsDF['Bid2'].astype(str)
        finalOptionsDF['Bid2'] = finalOptionsDF['Bid2'].str[1:]
        finalOptionsDF['Bid'] = finalOptionsDF['Bid1'] + finalOptionsDF['Bid2'].astype(str)
        del finalOptionsDF['Bid1']
        del finalOptionsDF['Bid2']
        
        finalOptionsDF[['Ask1','Ask2']] = finalOptionsDF['Ask'].str.split('-', expand=True)
        finalOptionsDF['Ask2'] = pd.to_numeric(finalOptionsDF['Ask2']) / 8
        finalOptionsDF['Ask2'] = finalOptionsDF['Ask2'].astype(str)
        finalOptionsDF['Ask2'] = finalOptionsDF['Ask2'].str[1:]
        finalOptionsDF['Ask'] = finalOptionsDF['Ask1'] + finalOptionsDF['Ask2'].astype(str)
        del finalOptionsDF['Ask1']
        del finalOptionsDF['Ask2']
        
        finalOptionsDF[['Future1','Future2']] = finalOptionsDF['Future Price'].str.split('-', expand=True)
        finalOptionsDF['Future2'] = finalOptionsDF['Future2'].apply(lambda x: x[:-1] if 's' in x else x)
        finalOptionsDF['Future2'] = pd.to_numeric(finalOptionsDF['Future2']) / 8
        finalOptionsDF['Future2'] = finalOptionsDF['Future2'].astype(str)
        finalOptionsDF['Future2'] = finalOptionsDF['Future2'].str[1:]
        finalOptionsDF['Future Price'] = finalOptionsDF['Future1'] + finalOptionsDF['Future2']
        del finalOptionsDF['Future1']
        del finalOptionsDF['Future2']
        
        finalOptionsDF['intrate'] = .0001
        finalOptionsDF['DTE'] = finalOptionsDF['DTE'].apply(lambda x: int(x.split()[0]))
        finalOptionsDF['Strike'] = finalOptionsDF['Strike'].astype(float)
        finalOptionsDF['Future Price'] = finalOptionsDF['Future Price'].astype(float)
        finalOptionsDF['Last'] = finalOptionsDF['Last'].astype(float)
        finalOptionsDF['Bid'] = finalOptionsDF['Bid'].astype(float)
        finalOptionsDF['Ask'] = finalOptionsDF['Ask'].astype(float)
        
        finalOptionsDF['Midpoint'] = round((finalOptionsDF['Bid'] + finalOptionsDF['Ask']) / 2, 3)
        finalOptionsDF['Future Price'] = finalOptionsDF['Future Price'] / 100
        finalOptionsDF['Strike'] = finalOptionsDF['Strike'] / 100
        finalOptionsDF['Midpoint'] = finalOptionsDF['Midpoint'] / 100
        finalOptionsDF['ImpVol']= finalOptionsDF.apply(lambda row: vs.impvol(row['PriceType'],row['Midpoint'], row['Future Price'], row['Strike'], row['DTE'], row['intrate']),axis=1)
        
        finalOptionsDF = finalOptionsDF.sort_values(['Description','PriceType','Strike'])
        finalOptionsDF = finalOptionsDF.astype({'Expiration':'datetime64[ns]'})
        
        expirationList = np.unique(finalOptionsDF['Expiration'])
        historic = OptionVols()
        historic = historic[historic['Symbol'] == commodityList[x]]
        
        finalOptionsDF = finalOptionsDF.reset_index()
        del finalOptionsDF['index']
        
        volTable = pd.DataFrame()
        fig,ax = plt.subplots(3, 3, figsize=(10,8))
        count = 0
        
        for i in range(len(expirationList)):
            
            tempDF = finalOptionsDF[finalOptionsDF['Expiration'] == expirationList[i]]
            strikeList = np.unique(tempDF['Strike'])
        
            for strike in strikeList:
                strikeDF = tempDF[tempDF['Strike'] == strike]
        
                if len(strikeDF) > 1:
                    if abs(strikeDF[:1]['ImpVol'].values[0] - strikeDF[1:2]['ImpVol'].values[0]) > .1:
                        finalOptionsDF = finalOptionsDF.drop(strikeDF.index.tolist()) 
            
            if len(finalOptionsDF[finalOptionsDF['Expiration'] == expirationList[i]]) > 20:
                
                missingStrikes = finalOptionsDF[finalOptionsDF['Expiration'] == expirationList[i]]
                futurePrice = np.unique(missingStrikes['Future Price'])[0]
                missingStrikes = missingStrikes.iloc[(missingStrikes['Strike'] - futurePrice).abs().argsort()[:1]]
                tableDescription = missingStrikes[:1]['Description'].values[0]
                missingStrikes = missingStrikes[(missingStrikes['Strike'] - futurePrice).abs() < .10]
        
                if len(missingStrikes) > 0:
                    strike = missingStrikes[:1]['Strike'].values[0]
        
                    tempStrikes = finalOptionsDF[finalOptionsDF['Expiration'] == expirationList[i]]
                    tempStrikes = missingStrikes[missingStrikes['Strike'] == strike]
                    
                    if len(tempStrikes) > 1:
                        tempStrikes = tempStrikes[['Strike','ImpVol']]
                        tempStrikes = tempStrikes.groupby('Strike').mean()
                        todayVol = tempStrikes['ImpVol'][strike]
                    else:
                        todayVol = missingStrikes[:1]['ImpVol'].values[0]
        
                    historicVol = historic[historic['ExpDate'] == expirationList[i]]
                    historicVol = historicVol[historicVol['Strike'] == strike]
                    
                    if len(historicVol) > 1:
                        historicVol = historicVol[['Strike','ImpVol']]
                        historicVol = historicVol.groupby('Strike').mean()
                        historicVol = historicVol['ImpVol'][strike]
                    else:
                        historicVol = historicVol[:1]['ImpVol'].values[0]
        
                    temp = []
                    temp.append(tableDescription)
                    temp.append(round(todayVol, 3))
                    temp.append(round(historicVol, 3))
                    temp.append(round((todayVol - historicVol), 3))
                    
                    tempVolEntry = pd.DataFrame(temp)
                    tempVolEntry = tempVolEntry.transpose()
                    tempVolEntry.columns = ['Description','Today Vol','Yesterday Vol','Change']
                    volTable = pd.concat([volTable,tempVolEntry])
                
                else:
                    
                    temp = []
                    temp.append(tableDescription)
                    temp.append('N/A')
                    temp.append('N/A')
                    temp.append('N/A')
            
                    tempVolEntry = pd.DataFrame(temp)
                    tempVolEntry = tempVolEntry.transpose()
                    tempVolEntry.columns = ['Description','Today Vol','Yesterday Vol','Change']
                    volTable = pd.concat([volTable,tempVolEntry])
        
                missingStrikes = finalOptionsDF[finalOptionsDF['Expiration'] == expirationList[i]]
                description = np.unique(missingStrikes['Description'])[0]
                missingStrikes = missingStrikes[['Strike','ImpVol']]
                missingStrikes = missingStrikes.groupby(by='Strike').mean()
        
                allStrikes = historic[historic['ExpDate'] == expirationList[i]]
                allStrikes = allStrikes[['Strike','ImpVol']]
                allStrikes = allStrikes.groupby(by='Strike').mean()
        
                historicLine = allStrikes.copy()
                
                del allStrikes['ImpVol']
                
                mergedDF = allStrikes.join(missingStrikes, on='Strike', how='left')
                interpolated = mergedDF.interpolate(method='index')
                
                if commodityList[x] == 'Corn':
                    interpolated = interpolated[interpolated.index  >= 4.0]
                    interpolated = interpolated[interpolated.index  <= 10.0]
            
                    historicLine = historicLine[historicLine.index >= 4.0]
                    historicLine = historicLine[historicLine.index <= 10.0]
                    
                elif commodityList[x] == 'Soybeans':
                    interpolated = interpolated[interpolated.index  >= 10.0]
                    interpolated = interpolated[interpolated.index  <= 20.0]
                    
                    historicLine = historicLine[historicLine.index >= 10.0]
                    historicLine = historicLine[historicLine.index <= 20.0]
                    
                elif commodityList[x] == 'Hard Wheat':
                    interpolated = interpolated[interpolated.index  >= 4.0]
                    interpolated = interpolated[interpolated.index  <= 9.0]
            
                    historicLine = historicLine[historicLine.index >= 4.0]
                    historicLine = historicLine[historicLine.index <= 9.0]
                    
                else:
                    interpolated = interpolated[interpolated.index  >= 4.0]
                    interpolated = interpolated[interpolated.index  <= 12.0]
            
                    historicLine = historicLine[historicLine.index >= 4.0]
                    historicLine = historicLine[historicLine.index <= 12.0]
                
                if count <= 2:
                    ax[0, count].plot(interpolated.index.tolist(), interpolated['ImpVol'], label = 'Intraday')
                    ax[0, count].plot(historicLine.index.tolist(), historicLine['ImpVol'], label = 'Yesterday')
                    ax[0, count].set_title(description)
                    
                elif count > 2 and count <= 5:
                    ax[1, count % 3].plot(interpolated.index.tolist(), interpolated['ImpVol'], label = 'Intraday')
                    ax[1, count % 3].plot(historicLine.index.tolist(), historicLine['ImpVol'], label = 'Yesterday')
                    ax[1, count % 3].set_title(description)
                
                else:
                    ax[2, count % 3].plot(interpolated.index.tolist(), interpolated['ImpVol'], label = 'Intraday')
                    ax[2, count % 3].plot(historicLine.index.tolist(), historicLine['ImpVol'], label = 'Yesterday')
                    ax[2, count % 3].set_title(description)
    
    #            ax[i].title(description)
    #            ax[i].legend()
                
                count  += 1
                
            else:
                missingStrikes = finalOptionsDF[finalOptionsDF['Expiration'] == expirationList[i]]
                futurePrice = np.unique(missingStrikes['Future Price'])[0]
                missingStrikes = missingStrikes.iloc[(missingStrikes['Strike'] - futurePrice).abs().argsort()[:1]]
                tableDescription = missingStrikes[:1]['Description'].values[0]
                missingStrikes = missingStrikes[(missingStrikes['Strike'] - futurePrice).abs() < .10]
                
                if len(missingStrikes) > 0:
                    strike = missingStrikes[:1]['Strike'].values[0]
                    
                    tempStrikes = finalOptionsDF[finalOptionsDF['Expiration'] == expirationList[i]]
                    tempStrikes = missingStrikes[missingStrikes['Strike'] == strike]
                    
                    if len(tempStrikes) > 1:
                        tempStrikes = tempStrikes[['Strike','ImpVol']]
                        tempStrikes = tempStrikes.groupby('Strike').mean()
                        todayVol = tempStrikes['ImpVol'][strike]
                    else:
                        todayVol = missingStrikes[:1]['ImpVol'].values[0]
        
                    historicVol = historic[historic['ExpDate'] == expirationList[i]]
                    historicVol = historicVol[historicVol['Strike'] == strike]
                    
                    if len(historicVol) > 1:
                        historicVol = historicVol[['Strike','ImpVol']]
                        historicVol = historicVol.groupby('Strike').mean()
                        historicVol = historicVol['ImpVol'][strike]
                    else:
                        historicVol = historicVol[:1]['ImpVol'].values[0]
        
                    temp = []
                    temp.append(tableDescription)
                    temp.append(round(todayVol, 3))
                    temp.append(round(historicVol, 3))
                    temp.append(round((todayVol - historicVol), 3))
                    
                    tempVolEntry = pd.DataFrame(temp)
                    tempVolEntry = tempVolEntry.transpose()
                    tempVolEntry.columns = ['Description','Today Vol','Yesterday Vol','Change']
                    volTable = pd.concat([volTable,tempVolEntry])
                
                else:
                    
                    temp = []
                    temp.append(tableDescription)
                    temp.append('N/A')
                    temp.append('N/A')
                    temp.append('N/A')
            
                    tempVolEntry = pd.DataFrame(temp)
                    tempVolEntry = tempVolEntry.transpose()
                    tempVolEntry.columns = ['Description','Today Vol','Yesterday Vol','Change']
                    volTable = pd.concat([volTable,tempVolEntry])
        
        fig.tight_layout()
        st.subheader(commodityList[x])
    
        buf = BytesIO()
        fig.savefig(buf, format="png")
        st.image(buf)
    
        st.dataframe(volTable)

else:
    
    st.title("Market Closed")
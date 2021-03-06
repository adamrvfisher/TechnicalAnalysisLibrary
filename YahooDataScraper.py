# -*- coding: utf-8 -*-
"""

@author: Adam Reinhold Von Fisher - https://www.linkedin.com/in/adamrvfisher/

"""

#This is a HTML scraper and techincal analysis tool -- Yahoo server side changes to API will yield 405 errors
#Run FolderFramework.py to set up folder directory
#Also, download and place in respective folders (or assign  to variables) UniverseList.csv and NASDAQData.csv
#Be sure to assign Directory Location as specified in FolderFramework.py
#Yahoo sourcing for monthlies, weeklies, dailies, dividend, and qualitative data
#As it runs, Directory Location folder will populate

#Import modules
import numpy as np
from pandas import read_csv 
import requests
import pandas as pd
import os
import time
from io import StringIO
from CrumbCatcher import CrumbCatcher
from pandas.parser import CParserError
from requests.exceptions import ConnectionError
import pandas.io.common

#Define function to save daily time series CSVs
def TickerToDailyCSV(Ticker):
    #Get crumb for daily download url
    DailyCrumb = str(CrumbCatcher(str(Ticker)))

    #Generate daily download url
    DailyDownloadURL = ("https://query1.finance.yahoo.com/v7/finance/download/" + Ticker 
    + "?period1=-631123200&period2=1598374000&interval=1d&events=history&crumb=" + DailyCrumb)

    #Download // capture response from post request
    DailyResponse = requests.post(DailyDownloadURL)

    #Formatting
    DailyResponseText = DailyResponse.text
    
    #More formatting..
    FormattedDailyResponse = StringIO(DailyResponseText)
    
    #Put Response in Dataframe
    DailyResponseDataFrame = pd.read_csv(FormattedDailyResponse, sep = ',')
    
    #Error detection
    if DailyResponseDataFrame.columns[0] == '{"chart":{"result":null':
        print('The URL failed for ' + Ticker + '.')
        pass

    #Set up date as primary key/Index for preprocess storage
    DailyResponseDataFrame = DailyResponseDataFrame.set_index('Date')
    
    #Change date to datetime data type
    DailyResponseDataFrame.index = pd.to_datetime(DailyResponseDataFrame.index, format = "%Y/%m/%d") 
    
    #Save to preprocess storage
    DailyResponseDataFrame.to_csv(DL + "\\DataSources\\YahooSource\\TimeSeriesData\\DAY-" + Ticker + ".csv")
    
    print(Ticker + ' Dailies saved.')    
    
    return
    
def TickerToWeeklyCSV(Ticker):
    #Get crumb for weekly download url
    WeeklyCrumb = str(CrumbCatcher(str(Ticker)))
    
    #Generate weekly download URL
    WeeklyDownloadURL = ("https://query1.finance.yahoo.com/v7/finance/download/" + Ticker 
    + "?period1=-631123200&period2=1598374000&interval=1wk&events=history&crumb=" + WeeklyCrumb)
    
    #Download // capture response from post request
    WeeklyResponse = requests.post(WeeklyDownloadURL)

    #Formatting
    WeeklyResponseText = WeeklyResponse.text
    
    #More formatting..
    FormattedWeeklyResponse = StringIO(WeeklyResponseText)
    
    #Put Response in Dataframe
    WeeklyResponseDataFrame = pd.read_csv(FormattedWeeklyResponse, sep = ',')
    
    if WeeklyResponseDataFrame.columns[0] == '{"chart":{"result":null':
        print('The URL failed for ' + Ticker + '.')
        pass

    #Set up date as primary key/Index for preprocess storage
    WeeklyResponseDataFrame = WeeklyResponseDataFrame.set_index('Date')
    
    #Change date to datetime data type
    WeeklyResponseDataFrame.index = pd.to_datetime(WeeklyResponseDataFrame.index, format = "%Y/%m/%d")
    
    #Save to preprocess storage
    WeeklyResponseDataFrame.to_csv((DL + "\\DataSources\\YahooSource\\TimeSeriesData\\WEK-" + Ticker + ".csv"))
    
    print(Ticker + ' Weeklies saved.')    
    
    return 
    
def TickerToMonthlyCSV(Ticker):
    #Get crumb for monthly download url
    MonthlyCrumb = str(CrumbCatcher(str(Ticker)))

    #Generate monthly download URL
    MonthlyDownloadURL = ("https://query1.finance.yahoo.com/v7/finance/download/" + Ticker 
    + "?period1=-631123200&period2=1598374000&interval=1mo&events=history&crumb=" + MonthlyCrumb)

    #Download // capture response from post request
    MonthlyResponse = requests.post(MonthlyDownloadURL)

    #Formatting
    MonthlyResponseText = MonthlyResponse.text
    
    #More formatting..
    FormattedMonthlyResponse = StringIO(MonthlyResponseText)
    
    #Put Response in Dataframe
    MonthlyResponseDataFrame = pd.read_csv(FormattedMonthlyResponse, sep = ',')
    
    #Error detection
    if MonthlyResponseDataFrame.columns[0] == '{"chart":{"result":null':
        print('The URL failed for ' + Ticker + '.')
        pass

    #Set up date as primary key/Index for preprocess storage
    MonthlyResponseDataFrame = MonthlyResponseDataFrame.set_index('Date')
    
    #Change date to datetime data type
    MonthlyResponseDataFrame.index = pd.to_datetime(MonthlyResponseDataFrame.index, format = "%Y/%m/%d") 
    
    #Save to preprocess storage
    MonthlyResponseDataFrame.to_csv((DL + "\\DataSources\\YahooSource\\TimeSeriesData\\MON-" + Ticker + ".csv"))
    
    print(Ticker + ' Monthlies saved.')    
    
    return 
    
def TickerToDividendCSV(Ticker):
    #Get crumb for dividend download url
    DividendCrumb = str(CrumbCatcher(str(Ticker)))

    #Generate dividend download URL
    DividendDownloadURL = ("https://query1.finance.yahoo.com/v7/finance/download/" + Ticker 
    + "?period1=-631123200&period2=1598374000&interval=1d&events=div&crumb=" + DividendCrumb)

    #Download // capture response from post request
    DividendResponse = requests.post(DividendDownloadURL)

    #Formatting
    DividendResponseText = DividendResponse.text
    
    #More formatting..
    FormattedDividendResponse = StringIO(DividendResponseText)
    
    #Put Response in Dataframe
    DividendResponseDataFrame = pd.read_csv(FormattedDividendResponse, sep = ',')
    
    #Error detection
    if DividendResponseDataFrame.columns[0] == '{"chart":{"result":null':
        print('The URL failed for ' + Ticker + ' dividends.')
        pass    
    
    #Set up date as primary key/Index for preprocess storage
    DividendResponseDataFrame = DividendResponseDataFrame.set_index('Date')
    
    #Change date to datetime data type
    DividendResponseDataFrame.index = pd.to_datetime(DividendResponseDataFrame.index, format = "%Y/%m/%d")  
    
    #Save to preprocess storage
    DividendResponseDataFrame.to_csv((DL + "\\DataSources\\YahooSource\\DividendData\\DIV-" + Ticker + ".csv"))
    
    print(Ticker + ' Dividends saved.')    
    
    return 

#No indexing view vs copy warning during dividend processing
pd.options.mode.chained_assignment = None 

start = time.time()

#Use directory location from FolderFramework.py
DL = "Z:\\Users\\UserName\\YahooDatabase"

#Place CSV in folder / load in Universe CSV from next line
#https://github.com/adamrvfisher/CondensedLibrary/blob/master/UniverseList.csv
UniverseListCSV = pd.read_csv(DL + '\\DataSources\\NASDAQSource\\UniverseLists\\UniverseList.csv', sep = ',')
UniverseList =  UniverseListCSV['Ticker']

#Custom Universe assignment; to add to Universe manually
#UniverseList = ['SPY', 'GLD', 'TQQQ', 'SQQQ', 'VXXB', 'SLV']#, '''''']

#Modify size
UniverseList = UniverseList[:10]

#Place CSV in folder / load in the NASDAQ CSV from next line 
#https://github.com/adamrvfisher/CondensedLibrary/blob/master/NASDAQData.csv
NASDAQData = pd.read_csv(DL + '\\DataSources\\NASDAQSource\\QualitativeData\\NASDAQData.csv', sep = ',')
NASDAQDataTickers = list(NASDAQData['Symbol'])

#Ticker Finder
#UniverseList.index('A')
#trim and reset index if interrupted
#df = df.reset_index(drop=True)

#Iterable range, one per issue
NumIssues = range(0,len(UniverseList))
#For every issue
for n in NumIssues:
    try: 
        #Take the symbol from the UniverseList
        Ticker = str(UniverseList[n])
        
        #Rest before daily crumb request
        time.sleep(2)
        
        #Request data
        while True: 
            try:
                TickerToDailyCSV(Ticker)            
            except CParserError:
                continue
            break  
        
        #Rest before weekly crumb request
        time.sleep(2)

        #Request data
        while True: 
            try:
                TickerToWeeklyCSV(Ticker)            
            except CParserError:
                continue
            break  
        
        #Rest before weekly crumb request
        time.sleep(2)

        #Request data
        while True: 
            try:
                TickerToMonthlyCSV(Ticker)            
            except CParserError:
                continue
            break  
        
        #Rest before dividend crumb request
        time.sleep(2)

        #Request data
        while True: 
            try:
                TickerToDividendCSV(Ticker)            
            except CParserError:
                continue
            break  
        
        print(Ticker + ' completed.')   
        
        continue
    
    except KeyError:
        print('KeyError for ' +  Ticker + ', likely unlisted.')

    except CParserError:
        print('Parser failed for ' + Ticker + ', skipping to next ticker.')
        continue

    except ConnectionError:
        try:
            #Sleep, then retry last ticker, continue loop.
            print('ConnectionError on ' + str(Ticker) + '.')
            print('Sleeping for 5 min.')        
            time.sleep(301)
            #Retrying parse
            print('Parsing for ' + Ticker + '.')
            
            #Request data
            while True: 
                try:
                    TickerToDailyCSV(Ticker)            
                except CParserError:
                    continue
                break  
            
            #Rest before weekly crumb request
            time.sleep(2)
    
            #Request data
            while True: 
                try:
                    TickerToWeeklyCSV(Ticker)            
                except CParserError:
                    continue
                break  
            
            #Rest before weekly crumb request
            time.sleep(2)
    
            #Request data
            while True: 
                try:
                    TickerToMonthlyCSV(Ticker)            
                except CParserError:
                    continue
                break  
            
            #Rest before dividend crumb request
            time.sleep(2)
    
            #Request data
            while True: 
                try:
                    TickerToDividendCSV(Ticker)            
                except CParserError:
                    continue
                break  
            
            print(Ticker + ' completed.')  
            
            continue
        
        except CParserError:
            print('Parser failed for ' + Ticker + '.')
            continue

        except requests.exceptions.SSLError:
            try:
                print('SSLError after Connection Error for ' + Ticker + '.')
                #Sleep, then retry last ticker, continue loop.
                print('Sleeping for 61 seconds.')        
                time.sleep(61)
                #Retrying parse
                print('Parsing for ' + Ticker + '.')
                
                #Request data
                while True: 
                    try:
                        TickerToDailyCSV(Ticker)            
                    except CParserError:
                        continue
                    break  
                
                #Rest before weekly crumb request
                time.sleep(2)
        
                #Request data
                while True: 
                    try:
                        TickerToWeeklyCSV(Ticker)            
                    except CParserError:
                        continue
                    break  
                
                #Rest before weekly crumb request
                time.sleep(2)
        
                #Request data
                while True: 
                    try:
                        TickerToMonthlyCSV(Ticker)            
                    except CParserError:
                        continue
                    break  
                
                #Rest before dividend crumb request
                time.sleep(2)
        
                #Request data
                while True: 
                    try:
                        TickerToDividendCSV(Ticker)            
                    except CParserError:
                        continue
                    break  
                
                print(Ticker + ' completed.')  
                
                continue   
            except CParserError:
                print('Parser failed for ' + Ticker + '.')
                continue
            except requests.exceptions.SSLError:
                print('Double SSLError after ConnectionError for ' + Ticker + '.')
                continue            
            except ConnectionError:
                print('Double ConnectionError for ' + Ticker + '.')
                continue

    except requests.exceptions.SSLError:
        try:
            #Sleep, then retry last ticker, continue loop.
            print('SSLError on ' + str(Ticker) + '.')
            print('Sleeping for 61 seconds.')        
            time.sleep(61)
            #Retrying parse
            print('Parsing for ' + Ticker + '.')

            #Request data
            while True: 
                try:
                    TickerToDailyCSV(Ticker)            
                except CParserError:
                    continue
                break  
            
            #Rest before weekly crumb request
            time.sleep(2)
    
            #Request data
            while True: 
                try:
                    TickerToWeeklyCSV(Ticker)            
                except CParserError:
                    continue
                break  
            
            #Rest before weekly crumb request
            time.sleep(2)
    
            #Request data
            while True: 
                try:
                    TickerToMonthlyCSV(Ticker)            
                except CParserError:
                    continue
                break  
            
            #Rest before dividend crumb request
            time.sleep(2)
    
            #Request data
            while True: 
                try:
                    TickerToDividendCSV(Ticker)            
                except CParserError:
                    continue
                break  
            
            print(Ticker + ' completed.')  
               
            continue   

        except CParserError:
            print('Parser failed for ' + Ticker + '.')
            continue

        except requests.exceptions.SSLError:
            print('Double SSLError for ' + Ticker + '.')
            continue

        except ConnectionError:
            #Sleep, then retry last ticker, continue loop.
            print('ConnectionError after SSLError on ' + str(Ticker) + '.')
            print('Sleeping for 61 seconds.')        
            time.sleep(61)
            #Retrying parse
            print('Parsing for ' + Ticker + '.')
            
            #Request data
            while True: 
                try:
                    TickerToDailyCSV(Ticker)            
                except CParserError:
                    continue
                break  
            
            #Rest before weekly crumb request
            time.sleep(2)
    
            #Request data
            while True: 
                try:
                    TickerToWeeklyCSV(Ticker)            
                except CParserError:
                    continue
                break  
            
            #Rest before weekly crumb request
            time.sleep(2)
    
            #Request data
            while True: 
                try:
                    TickerToMonthlyCSV(Ticker)            
                except CParserError:
                    continue
                break  
            
            #Rest before dividend crumb request
            time.sleep(2)
    
            #Request data
            while True: 
                try:
                    TickerToDividendCSV(Ticker)            
                except CParserError:
                    continue
                break  
            
            print(Ticker + ' completed.')
            
            continue

print('All source data is in preprocess storage as CSV; ready for processing.')

#Processed data will be stored as FREQ-TICKER-YYYYMMDD(Timestamp??? Daily is smallest frequency for this source.)            
#CSV list for TimeSeries Data to put into processing
TimeSeries = os.listdir(DL + '\\DataSources\\YahooSource\\TimeSeriesData\\')
TimeSeriesTickers = [s[4:-4] for s in TimeSeries]
#Iterable for every freqxstock
ranger = range(0,len(TimeSeries))

for i in ranger:
    try:
        temp = read_csv(DL + '\\DataSources\\YahooSource\\TimeSeriesData\\' +
                         (TimeSeries[i]), sep = ',')
        print('Basic time series processing for ' + TimeSeries[i] +'.')
        #Make index for frequency concatenation; ProcessedDataIndex            
        FSList = []
        for ii in temp['Date'].index:
            FSList.append(temp['Date'][ii].replace('-',''))
            FSSeries = pd.Series(FSList) 
        temp['FrequencySuffix'] = pd.Series(FSSeries)
        temp['FrequencyPrefix'] = TimeSeries[i][:3]
        temp['Ticker'] = TimeSeries[i][4:-4]
        temp['ProcessedDataIndex'] = temp['FrequencyPrefix'] + temp['Ticker'] + temp['FrequencySuffix']
        #Until further notice, use Date as index regardless of frequency for this source..       
        temp = temp.set_index('Date')
        #Formatting
        temp.index = pd.to_datetime(temp.index, format = "%Y/%m/%d") 
        #Erase duplicate columns
        temp = temp.loc[:,~temp.columns.duplicated()]
        #Erase duplicate rows
        temp = temp[~temp.index.duplicated(keep='first')]
        #Make HLOCV data all numerical
        for x in temp.columns[:6]:
            temp[x] =  pd.to_numeric(temp[x], errors='coerce')
        #Basic Date information
        temp['Age'] = len(temp['Adj Close'])
        temp['Year'] = temp.index.year
        temp['Month'] = temp.index.month
        temp['Day'] = temp.index.day
        temp['DayOfWeek'] = temp.index.dayofweek
        #Dividends
        temp['Dividends'] = np.nan
        #Addition of NASDAQSource data; its stored as CSV - NASDAQ data will have to be populated already.
        NASDAQDataRow = NASDAQData[NASDAQData['Symbol'] == temp['Ticker'][0]]  
        temp['Name'] = NASDAQDataRow.iloc[0][1]
        temp['LastSale'] = float(NASDAQDataRow.iloc[0][2])
        temp['GivenMarketCap'] = NASDAQDataRow.iloc[0][3]
        temp['IPOyear'] = NASDAQDataRow.iloc[0][5]
        temp['Sector'] = NASDAQDataRow.iloc[0][6]
        temp['Industry'] = NASDAQDataRow.iloc[0][7]
        temp['SharesOutstanding'] = temp['GivenMarketCap']/temp['LastSale']
        temp['MarketCap'] = (temp['SharesOutstanding'] * temp['Adj Close'])/10**9          
        #Make folders inside quarternary folders - Choose frequency and save in frequency folder; For time series data
        if not os.path.exists(DL + '\\DataSources\\YahooSource\\ProcessedData\\' +
                         temp['FrequencyPrefix'][0] + '\\' + TimeSeries[i][:-4]):
            os.makedirs(DL + '\\DataSources\\YahooSource\\ProcessedData\\' +
                         temp['FrequencyPrefix'][0] + '\\' + TimeSeries[i][:-4])
        pd.to_pickle(temp, DL + '\\DataSources\\YahooSource\\ProcessedData\\' +
            temp['FrequencyPrefix'][0] + '\\' + TimeSeries[i][:-4] + '\\' + TimeSeries[i][:-4])
        print(temp['Ticker'][0] + ' time series pickles saved.')
    except OSError:
        continue
    except IndexError: #If there is no qualitative data for given ticker
                       #Fill N/A to missing data from Remote Source
        temp['Name'] = np.nan
        temp['LastSale'] = np.nan
        temp['GivenMarketCap'] = np.nan
        temp['IPOyear'] = np.nan
        temp['Sector'] = np.nan
        temp['Industry'] = np.nan
        temp['SharesOutstanding'] = np.nan
        #Perhaps make a proxy for market cap and insert here
        temp['MarketCap'] = np.nan
        #Make folders inside quarternary folders - Choose frequency and save in frequency folder; For time series data
        if not os.path.exists(DL + '\\DataSources\\YahooSource\\ProcessedData\\' +
                         temp['FrequencyPrefix'][0] + '\\' + TimeSeries[i][:-4]):
            os.makedirs(DL + '\\DataSources\\YahooSource\\ProcessedData\\' +
                         temp['FrequencyPrefix'][0] + '\\' + TimeSeries[i][:-4])
        pd.to_pickle(temp, DL + '\\DataSources\\YahooSource\\ProcessedData\\' +
            temp['FrequencyPrefix'][0] + '\\' + TimeSeries[i][:-4] + '\\' + TimeSeries[i][:-4])

print('Time series data stored in ProcessedData')

#Contents of dividend parse
Dividends = os.listdir(DL + '\\DataSources\\YahooSource\\DividendData\\')
DividendsTickers = [s[4:-4] for s in Dividends]
#Iterable for every divxstock
ranger = range(0,len(Dividends))
for i in ranger:
    try:
        temp = read_csv(DL + '\\DataSources\\YahooSource\\DividendData\\' +
                         (Dividends[i]), sep = ',')
        print('Basic dividend processing for ' + DividendsTickers[i] +'.')
        #Make index for frequency concatenation; ProcessedDataIndex            
        FSList = []
        for ii in temp['Date'].index:
            FSList.append(temp['Date'][ii].replace('-',''))
            FSSeries = pd.Series(FSList) 
        temp['FrequencySuffix'] = pd.Series(FSSeries)
        temp['FrequencyPrefix'] = Dividends[i][:3]
        temp['Ticker'] = Dividends[i][4:-4]
        temp['ProcessedDataIndex'] = temp['FrequencyPrefix'] + temp['Ticker'] + temp['FrequencySuffix']
        #Until further notice, use Date as index regardless of frequency for this source..       
        temp = temp.set_index('Date')
        #Formatting
        temp.index = pd.to_datetime(temp.index, format = "%Y/%m/%d") 
        #Sort DIV by index..
        temp = temp.sort_index()
        #Erase duplicate columns
        temp = temp.loc[:,~temp.columns.duplicated()]
        #Erase duplicate rows
        temp = temp[~temp.index.duplicated(keep='first')]
        #Make dividend info numerical
        for xx in temp.columns[:1]:
            temp[xx] =  pd.to_numeric(temp[xx], errors='coerce') 
        #Basic Date information
        temp['Age'] = len(temp['Dividends'])
        temp['Year'] = temp.index.year
        temp['Month'] = temp.index.month
        temp['Day'] = temp.index.day
        temp['DayOfWeek'] = temp.index.dayofweek
        #Addition of NASDAQSource data; its stored as CSV - NASDAQ data will have to be populated already.
        NASDAQDataRow = NASDAQData[NASDAQData['Symbol'] == temp['Ticker'][0]]  
        temp['Name'] = NASDAQDataRow.iloc[0][1]
        temp['LastSale'] = float(NASDAQDataRow.iloc[0][2])
        temp['GivenMarketCap'] = NASDAQDataRow.iloc[0][3]
        temp['IPOyear'] = NASDAQDataRow.iloc[0][5]
        temp['Sector'] = NASDAQDataRow.iloc[0][6]
        temp['Industry'] = NASDAQDataRow.iloc[0][7]
        temp['SharesOutstanding'] = temp['GivenMarketCap']/temp['LastSale']         
        #Make folders inside quarternary folders - Choose frequency and save in frequency folder; For time series data
        if not os.path.exists(DL + '\\DataSources\\YahooSource\\ProcessedData\\' +
                         temp['FrequencyPrefix'][0] + '\\' + Dividends[i][:-4]):
            os.makedirs(DL + '\\DataSources\\YahooSource\\ProcessedData\\' +
                         temp['FrequencyPrefix'][0] + '\\' + Dividends[i][:-4])
        pd.to_pickle(temp, DL + '\\DataSources\\YahooSource\\ProcessedData\\' +
            temp['FrequencyPrefix'][0] + '\\' + Dividends[i][:-4] + '\\' + Dividends[i][:-4])
        print(temp['Ticker'][0] + ' time series pickles saved.')
    except pandas.io.common.EmptyDataError:
        continue
    except OSError:
        continue
    except IndexError: #If there is no qualitative data for given ticker
                       #Fill N/A to missing data from Remote Source
        temp['Name'] = np.nan
        temp['LastSale'] = np.nan
        temp['GivenMarketCap'] = np.nan
        temp['IPOyear'] = np.nan
        temp['Sector'] = np.nan
        temp['Industry'] = np.nan
        temp['SharesOutstanding'] = np.nan
        #Make folders inside quarternary folders - Choose frequency and save in frequency folder; For time series data
        if not os.path.exists(DL + '\\DataSources\\YahooSource\\ProcessedData\\' +
                         temp['FrequencyPrefix'][0] + '\\' + Dividends[i][:-4]):
            os.makedirs(DL + '\\DataSources\\YahooSource\\ProcessedData\\' +
                         temp['FrequencyPrefix'][0] + '\\' + Dividends[i][:-4])
        pd.to_pickle(temp, DL + '\\DataSources\\YahooSource\\ProcessedData\\' +
            temp['FrequencyPrefix'][0] + '\\' + Dividends[i][:-4] + '\\' + Dividends[i][:-4])

print('Dividend data stored in DividendData')
#Yahoo source HLOC data is stored and cleaned in pickles for addition of dividend, div yield, and technical analysis data. 

print('Adding dividend info to daily time series.')
#Find all stocks with dividend information and technical data // delete duplicates list(set()) might be redundant.
DividendAndTechnicalList = list(set([i for i in DividendsTickers if i in TimeSeriesTickers]))
#For all stocks with div + dailies: Dividend based modifications made here. 
for d in DividendAndTechnicalList:
#    try:
        #Get DAY time series
        DAY = pd.read_pickle(DL + '\\DataSources\\'
        + 'YahooSource\\ProcessedData\\' + 'DAY' + '\\' + 'DAY-' + d + '\\' + 'DAY-' + d)    
        #Get DIV 
        DIV = pd.read_pickle(DL + '\\DataSources\\'
        + 'YahooSource\\ProcessedData\\' + 'DIV' + '\\' + 'DIV-' + d + '\\' + 'DIV-' + d)
        #For every dividend entry, populate daily TS['Dividends'] from DIV.T
        TimeStamps = [i for i in DAY.index if i in DIV.index]
        DAY.loc[(TimeStamps,'Dividends')] = DIV['Dividends']
        DAY['LastDividend'] = DAY['Dividends']
        #Bfill to use for yield calculation
        DAY['LastDividend'][DAY['LastDividend'] == 0] = np.nan
        DAY['LastDividend'] = DAY['LastDividend'].ffill()
        #Fill nans with 0 for no dividends on given day
        DAY['Dividends'] = DAY['Dividends'].fillna(0) 
        #Div Yield by unspecified frequency // Be aware of assumptions using AdjClose
        DAY['DividendYield'] = DAY['LastDividend']/DAY['Adj Close']
        pd.to_pickle(DAY, DL +'\\DataSources\\' +
            'YahooSource\\ProcessedData\\' + 'DAY' + '\\' + 'DAY-' + d + '\\' + 'DAY-' + d)
        print('Dividends added to ' + d + ' dailies.')       
#Populate set - DAY, WEK, MO - with custom database modifications for TA data.
#Start with Yahoo dailies TA mod
print('Processing for dailies.')
#Get list to process
ProcessedDailies = os.listdir(DL + '\\DataSources\\'
        + 'YahooSource\\ProcessedData\\DAY\\')
for p in ProcessedDailies:
    #Access data
    temp = pd.read_pickle(DL + '\\DataSources\\'
        + 'YahooSource\\ProcessedData\\DAY\\' + p + '\\' + p)
            #Daily Log Returns (subtract 1!!!)
    temp['LogRet'] = np.log(temp['Adj Close']/temp['Adj Close'].shift(1)) 
    temp['LogRet'] = temp['LogRet'].fillna(0)
    
    #Technical data 
    temp['HigherOpen'] = (np.where(temp['Open'] > temp['Open'].shift(1), 1,0))
    temp['LowerOpen'] = (np.where(temp['Open'] < temp['Open'].shift(1), 1,0))
    temp['HigherHigh'] = (np.where(temp['High'] > temp['High'].shift(1), 1,0))
    temp['LowerHigh'] = (np.where(temp['High'] < temp['High'].shift(1), 1,0))
    temp['HigherLow'] = (np.where(temp['Low'] > temp['Low'].shift(1), 1,0))
    temp['LowerLow'] = (np.where(temp['Low'] < temp['Low'].shift(1), 1,0))
    temp['HigherClose'] = (np.where(temp['Adj Close'] > temp['Adj Close'].shift(1), 1,0))
    temp['LowerClose'] = (np.where(temp['Adj Close'] < temp['Adj Close'].shift(1), 1,0))
    
    #Gap Up % > 0 
    temp['GapUp'] = (temp['High'].shift(1) - temp['Low']) / temp['Adj Close'].shift(1)
    temp['GapUp'] = temp['GapUp'][temp['GapUp'] < 0]
    temp['GapUp'] = temp['GapUp'].fillna(0)
    temp['GapUp'] = np.where(temp['GapUp'] == 0 , 0, (-1*temp['GapUp']))

    #Gap Down % > 0 
    temp['GapDown'] = (temp['Low'].shift(1) - temp['High']) / temp['Adj Close'].shift(1)
    temp['GapDown'] = temp['GapDown'][temp['GapDown'] > 0]
    temp['GapDown'] = temp['GapDown'].fillna(0)
    
    #Min/Max & RangePoints/RangePercent
    temp['AllTimeLow'] = temp['Adj Close'].min()
    temp['AllTimeHigh'] = temp['Adj Close'].max()
    temp['100wkLow'] = temp['Adj Close'].rolling(500).min()
    temp['100wkHigh'] = temp['Adj Close'].rolling(500).max()
    temp['100wkRangePoints'] = temp['100wkHigh'] - temp['100wkLow']
    temp['100wkRangePercent'] = temp['100wkRangePoints'] / temp['Adj Close']
    temp['90wkLow'] = temp['Adj Close'].rolling(450).min()
    temp['90wkHigh'] = temp['Adj Close'].rolling(450).max()
    temp['90wkRangePoints'] = temp['90wkHigh'] - temp['90wkLow']
    temp['90wkRangePercent'] = temp['90wkRangePoints'] / temp['Adj Close']
    temp['80wkLow'] = temp['Adj Close'].rolling(400).min()
    temp['80wkHigh'] = temp['Adj Close'].rolling(400).max()
    temp['80wkRangePoints'] = temp['80wkHigh'] - temp['80wkLow']
    temp['80wkRangePercent'] = temp['80wkRangePoints'] / temp['Adj Close']
    temp['70wkLow'] = temp['Adj Close'].rolling(350).min()
    temp['70wkHigh'] = temp['Adj Close'].rolling(350).max()
    temp['70wkRangePoints'] = temp['70wkHigh'] - temp['70wkLow']
    temp['70wkRangePercent'] = temp['70wkRangePoints'] / temp['Adj Close']
    temp['65wkLow'] = temp['Adj Close'].rolling(325).min()
    temp['65wkHigh'] = temp['Adj Close'].rolling(325).max()
    temp['65wkRangePoints'] = temp['65wkHigh'] - temp['65wkLow']
    temp['65wkRangePercent'] = temp['65wkRangePoints'] / temp['Adj Close']
    temp['60wkLow'] = temp['Adj Close'].rolling(300).min()
    temp['60wkHigh'] = temp['Adj Close'].rolling(300).max()
    temp['60wkRangePoints'] = temp['60wkHigh'] - temp['60wkLow']
    temp['60wkRangePercent'] = temp['60wkRangePoints'] / temp['Adj Close']
    temp['55wkLow'] = temp['Adj Close'].rolling(275).min()
    temp['55wkHigh'] = temp['Adj Close'].rolling(275).max()
    temp['55wkRangePoints'] = temp['55wkHigh'] - temp['55wkLow']
    temp['55wkRangePercent'] = temp['55wkRangePoints'] / temp['Adj Close']
    temp['52wkLow'] = temp['Adj Close'].rolling(252).min()
    temp['52wkHigh'] = temp['Adj Close'].rolling(252).max()
    temp['52wkRangePoints'] = temp['52wkHigh'] - temp['52wkLow']
    temp['52wkRangePercent'] = temp['52wkRangePoints'] / temp['Adj Close']
    temp['45wkLow'] = temp['Adj Close'].rolling(225).min()
    temp['45wkHigh'] = temp['Adj Close'].rolling(225).max()
    temp['45wkRangePoints'] = temp['45wkHigh'] - temp['45wkLow']
    temp['45wkRangePercent'] = temp['45wkRangePoints'] / temp['Adj Close']
    temp['40wkLow'] = temp['Adj Close'].rolling(200).min()
    temp['40wkHigh'] = temp['Adj Close'].rolling(200).max()
    temp['40wkRangePoints'] = temp['40wkHigh'] - temp['40wkLow']
    temp['40wkRangePercent'] = temp['40wkRangePoints'] / temp['Adj Close']
    temp['35wkLow'] = temp['Adj Close'].rolling(175).min()
    temp['35wkHigh'] = temp['Adj Close'].rolling(175).max()
    temp['35wkRangePoints'] = temp['35wkHigh'] - temp['35wkLow']
    temp['35wkRangePercent'] = temp['35wkRangePoints'] / temp['Adj Close']
    temp['30wkLow'] = temp['Adj Close'].rolling(150).min()
    temp['30wkHigh'] = temp['Adj Close'].rolling(150).max()
    temp['30wkRangePoints'] = temp['30wkHigh'] - temp['30wkLow']
    temp['30wkRangePercent'] = temp['30wkRangePoints'] / temp['Adj Close']
    temp['25wkLow'] = temp['Adj Close'].rolling(125).min()
    temp['25wkHigh'] = temp['Adj Close'].rolling(125).max()
    temp['25wkRangePoints'] = temp['25wkHigh'] - temp['25wkLow']
    temp['25wkRangePercent'] = temp['25wkRangePoints'] / temp['Adj Close']
    temp['20wkLow'] = temp['Adj Close'].rolling(100).min()
    temp['20wkHigh'] = temp['Adj Close'].rolling(100).max()
    temp['20wkRangePoints'] = temp['20wkHigh'] - temp['20wkLow']
    temp['20wkRangePercent'] = temp['20wkRangePoints'] / temp['Adj Close']
    temp['15wkLow'] = temp['Adj Close'].rolling(75).min()
    temp['15wkHigh'] = temp['Adj Close'].rolling(75).max()
    temp['15wkRangePoints'] = temp['15wkHigh'] - temp['15wkLow']
    temp['15wkRangePercent'] = temp['15wkRangePoints'] / temp['Adj Close']
    temp['12wkLow'] = temp['Adj Close'].rolling(60).min()
    temp['12wkHigh'] = temp['Adj Close'].rolling(60).max()
    temp['12wkRangePoints'] = temp['12wkHigh'] - temp['12wkLow']
    temp['12wkRangePercent'] = temp['12wkRangePoints'] / temp['Adj Close']
    temp['11wkLow'] = temp['Adj Close'].rolling(55).min()
    temp['11wkHigh'] = temp['Adj Close'].rolling(55).max()
    temp['11wkRangePoints'] = temp['11wkHigh'] - temp['11wkLow']
    temp['11wkRangePercent'] = temp['11wkRangePoints'] / temp['Adj Close']
    temp['10wkLow'] = temp['Adj Close'].rolling(50).min()
    temp['10wkHigh'] = temp['Adj Close'].rolling(50).max()
    temp['10wkRangePoints'] = temp['10wkHigh'] - temp['10wkLow']
    temp['10wkRangePercent'] = temp['10wkRangePoints'] / temp['Adj Close']
    temp['9wkLow'] = temp['Adj Close'].rolling(45).min()
    temp['9wkHigh'] = temp['Adj Close'].rolling(45).max()
    temp['9wkRangePoints'] = temp['9wkHigh'] - temp['9wkLow']
    temp['9wkRangePercent'] = temp['9wkRangePoints'] / temp['Adj Close']
    temp['8wkLow'] = temp['Adj Close'].rolling(40).min()
    temp['8wkHigh'] = temp['Adj Close'].rolling(40).max()
    temp['8wkRangePoints'] = temp['8wkHigh'] - temp['8wkLow']
    temp['8wkRangePercent'] = temp['8wkRangePoints'] / temp['Adj Close']
    temp['7wkLow'] = temp['Adj Close'].rolling(35).min()
    temp['7wkHigh'] = temp['Adj Close'].rolling(35).max()
    temp['7wkRangePoints'] = temp['7wkHigh'] - temp['7wkLow']
    temp['7wkRangePercent'] = temp['7wkRangePoints'] / temp['Adj Close']
    temp['6wkLow'] = temp['Adj Close'].rolling(30).min()
    temp['6wkHigh'] = temp['Adj Close'].rolling(30).max()
    temp['6wkRangePoints'] = temp['6wkHigh'] - temp['6wkLow']
    temp['6wkRangePercent'] = temp['6wkRangePoints'] / temp['Adj Close']
    temp['5wkLow'] = temp['Adj Close'].rolling(25).min()
    temp['5wkHigh'] = temp['Adj Close'].rolling(25).max()
    temp['5wkRangePoints'] = temp['5wkHigh'] - temp['5wkLow']
    temp['5wkRangePercent'] = temp['5wkRangePoints'] / temp['Adj Close']
    temp['4wkLow'] = temp['Adj Close'].rolling(20).min()
    temp['4wkHigh'] = temp['Adj Close'].rolling(20).max()
    temp['4wkRangePoints'] = temp['4wkHigh'] - temp['4wkLow']
    temp['4wkRangePercent'] = temp['4wkRangePoints'] / temp['Adj Close']   
    temp['3wkLow'] = temp['Adj Close'].rolling(15).min()
    temp['3wkHigh'] = temp['Adj Close'].rolling(15).max()
    temp['3wkRangePoints'] = temp['3wkHigh'] - temp['3wkLow']
    temp['3wkRangePercent'] = temp['3wkRangePoints'] / temp['Adj Close']
    temp['2wkLow'] = temp['Adj Close'].rolling(10).min()
    temp['2wkHigh'] = temp['Adj Close'].rolling(10).max()
    temp['2wkRangePoints'] = temp['2wkHigh'] - temp['2wkLow']
    temp['2wkRangePercent'] = temp['2wkRangePoints'] / temp['Adj Close']
    temp['1wkLow'] = temp['Adj Close'].rolling(5).min()
    temp['1wkHigh'] = temp['Adj Close'].rolling(5).max()
    temp['1wkRangePoints'] = temp['1wkHigh'] - temp['1wkLow']
    temp['1wkRangePercent'] = temp['1wkRangePoints'] / temp['Adj Close']
    temp['4dayLow'] = temp['Adj Close'].rolling(4).min()
    temp['4dayHigh'] = temp['Adj Close'].rolling(4).max()
    temp['4dayRangePoints'] = temp['4dayHigh'] - temp['4dayLow']
    temp['4dayRangePercent'] = temp['4dayRangePoints'] / temp['Adj Close']
    temp['3dayLow'] = temp['Adj Close'].rolling(3).min()
    temp['3dayHigh'] = temp['Adj Close'].rolling(3).max()
    temp['3dayRangePoints'] = temp['3dayHigh'] - temp['3dayLow']
    temp['3dayRangePercent'] = temp['3dayRangePoints'] / temp['Adj Close']
    temp['2dayLow'] = temp['Adj Close'].rolling(2).min()
    temp['2dayHigh'] = temp['Adj Close'].rolling(2).max()
    temp['2dayRangePoints'] = temp['2dayHigh'] - temp['2dayLow']
    temp['2dayRangePercent'] = temp['2dayRangePoints'] / temp['Adj Close']
    
    #STATIC Average Range
    temp['100wkTotalAverageRange'] = temp['100wkRangePercent'].mean() * 500
    temp['90wkTotalAverageRange'] = temp['90wkRangePercent'].mean() * 450
    temp['80wkTotalAverageRange'] = temp['80wkRangePercent'].mean() * 400
    temp['70wkTotalAverageRange'] = temp['70wkRangePercent'].mean() * 350
    temp['65wkTotalAverageRange'] = temp['65wkRangePercent'].mean() * 325
    temp['60wkTotalAverageRange'] = temp['60wkRangePercent'].mean() * 300
    temp['55wkTotalAverageRange'] = temp['55wkRangePercent'].mean() * 275
    temp['52wkTotalAverageRange'] = temp['52wkRangePercent'].mean() * 252
    temp['45wkTotalAverageRange'] = temp['45wkRangePercent'].mean() * 225
    temp['40wkTotalAverageRange'] = temp['40wkRangePercent'].mean() * 200
    temp['35wkTotalAverageRange'] = temp['35wkRangePercent'].mean() * 175
    temp['30wkTotalAverageRange'] = temp['30wkRangePercent'].mean() * 150
    temp['25wkTotalAverageRange'] = temp['25wkRangePercent'].mean() * 125
    temp['20wkTotalAverageRange'] = temp['20wkRangePercent'].mean() * 100
    temp['15wkTotalAverageRange'] = temp['15wkRangePercent'].mean() * 75
    temp['12wkTotalAverageRange'] = temp['12wkRangePercent'].mean() * 60
    temp['11wkTotalAverageRange'] = temp['11wkRangePercent'].mean() * 55
    temp['10wkTotalAverageRange'] = temp['10wkRangePercent'].mean() * 50
    temp['9wkTotalAverageRange'] = temp['9wkRangePercent'].mean() * 45
    temp['8wkTotalAverageRange'] = temp['8wkRangePercent'].mean() * 40
    temp['7wkTotalAverageRange'] = temp['7wkRangePercent'].mean() * 35
    temp['6wkTotalAverageRange'] = temp['6wkRangePercent'].mean() * 30
    temp['5wkTotalAverageRange'] = temp['5wkRangePercent'].mean() * 25
    temp['4wkTotalAverageRange'] = temp['4wkRangePercent'].mean() * 20
    temp['3wkTotalAverageRange'] = temp['3wkRangePercent'].mean() * 15
    temp['2wkTotalAverageRange'] = temp['2wkRangePercent'].mean() * 10
    temp['1wkTotalAverageRange'] = temp['1wkRangePercent'].mean() * 5
    temp['4dayTotalAverageRange'] = temp['4dayRangePercent'].mean() * 4
    temp['3dayTotalAverageRange'] = temp['3dayRangePercent'].mean() * 3
    temp['2dayTotalAverageRange'] = temp['2dayRangePercent'].mean() * 2
    
    #DYNAMIC Rolling Average Range
    temp['100wkRollingAverageRange'] = temp['100wkRangePercent'].rolling(
                                     center=False, window = 500).mean()
    temp['90wkRollingAverageRange'] = temp['90wkRangePercent'].rolling(
                                     center=False, window = 450).mean()
    temp['80wkRollingAverageRange'] = temp['80wkRangePercent'].rolling(
                                     center=False, window = 400).mean()                                     
    temp['70wkRollingAverageRange'] = temp['70wkRangePercent'].rolling(
                                     center=False, window = 350).mean()
    temp['65wkRollingAverageRange'] = temp['65wkRangePercent'].rolling(
                                     center=False, window = 325).mean()
    temp['60wkRollingAverageRange'] = temp['60wkRangePercent'].rolling(
                                     center=False, window = 300).mean()                                     
    temp['55wkRollingAverageRange'] = temp['55wkRangePercent'].rolling(
                                     center=False, window = 275).mean()
    temp['52wkRollingAverageRange'] = temp['52wkRangePercent'].rolling(
                                     center=False, window = 252).mean()
    temp['45wkRollingAverageRange'] = temp['45wkRangePercent'].rolling(
                                     center=False, window = 225).mean()
    temp['40wkRollingAverageRange'] = temp['40wkRangePercent'].rolling(
                                     center=False, window = 200).mean()
    temp['35wkRollingAverageRange'] = temp['35wkRangePercent'].rolling(
                                     center=False, window = 175).mean()                                     
    temp['30wkRollingAverageRange'] = temp['30wkRangePercent'].rolling(
                                     center=False, window = 150).mean()
    temp['25wkRollingAverageRange'] = temp['25wkRangePercent'].rolling(
                                     center=False, window = 125).mean()
    temp['20wkRollingAverageRange'] = temp['20wkRangePercent'].rolling(
                                     center=False, window = 100).mean()
    temp['15wkRollingAverageRange'] = temp['15wkRangePercent'].rolling(
                                     center=False, window = 75).mean()
    temp['12wkRollingAverageRange'] = temp['12wkRangePercent'].rolling(
                                     center=False, window = 60).mean()
    temp['11wkRollingAverageRange'] = temp['11wkRangePercent'].rolling(
                                     center=False, window = 55).mean()
    temp['10wkRollingAverageRange'] = temp['10wkRangePercent'].rolling(
                                     center=False, window = 50).mean()
    temp['9wkRollingAverageRange'] = temp['9wkRangePercent'].rolling(
                                     center=False, window = 45).mean()
    temp['8wkRollingAverageRange'] = temp['8wkRangePercent'].rolling(
                                     center=False, window = 40).mean()
    temp['7wkRollingAverageRange'] = temp['7wkRangePercent'].rolling(
                                     center=False, window = 35).mean()
    temp['6wkRollingAverageRange'] = temp['6wkRangePercent'].rolling(
                                     center=False, window = 30).mean()
    temp['5wkRollingAverageRange'] = temp['5wkRangePercent'].rolling(
                                     center=False, window = 25).mean()
    temp['4wkRollingAverageRange'] = temp['4wkRangePercent'].rolling(
                                     center=False, window = 20).mean()
    temp['3wkRollingAverageRange'] = temp['3wkRangePercent'].rolling(
                                     center=False, window = 15).mean()
    temp['2wkRollingAverageRange'] = temp['2wkRangePercent'].rolling(
                                     center=False, window = 10).mean()
    temp['1wkRollingAverageRange'] = temp['1wkRangePercent'].rolling(
                                     center=False, window = 5).mean()
    temp['4dayRollingAverageRange'] = temp['4dayRangePercent'].rolling(
                                     center=False, window = 4).mean()
    temp['3dayRollingAverageRange'] = temp['4dayRangePercent'].rolling(
                                     center=False, window = 3).mean()
    temp['2dayRollingAverageRange'] = temp['2dayRangePercent'].rolling(
                                     center=False, window = 2).mean()

    #DYNAMIC (Rolling Average Range / Average Range) - 1
    temp['100wkRARtoTAR'] = (temp['100wkRollingAverageRange']/temp['100wkTotalAverageRange']) - 1
    temp['90wkRARtoTAR'] = (temp['90wkRollingAverageRange']/temp['90wkTotalAverageRange']) - 1
    temp['80wkRARtoTAR'] = (temp['80wkRollingAverageRange']/temp['80wkTotalAverageRange']) - 1
    temp['70wkRARtoTAR'] = (temp['70wkRollingAverageRange']/temp['70wkTotalAverageRange']) - 1
    temp['65wkRARtoTAR'] = (temp['65wkRollingAverageRange']/temp['65wkTotalAverageRange']) - 1
    temp['60wkRARtoTAR'] = (temp['60wkRollingAverageRange']/temp['60wkTotalAverageRange']) - 1
    temp['55wkRARtoTAR'] = (temp['55wkRollingAverageRange']/temp['55wkTotalAverageRange']) - 1
    temp['52wkRARtoTAR'] = (temp['52wkRollingAverageRange']/temp['52wkTotalAverageRange']) - 1
    temp['45wkRARtoTAR'] = (temp['45wkRollingAverageRange']/temp['45wkTotalAverageRange']) - 1
    temp['40wkRARtoTAR'] = (temp['40wkRollingAverageRange']/temp['40wkTotalAverageRange']) - 1
    temp['35wkRARtoTAR'] = (temp['35wkRollingAverageRange']/temp['35wkTotalAverageRange']) - 1
    temp['30wkRARtoTAR'] = (temp['30wkRollingAverageRange']/temp['30wkTotalAverageRange']) - 1
    temp['25wkRARtoTAR'] = (temp['25wkRollingAverageRange']/temp['25wkTotalAverageRange']) - 1    
    temp['20wkRARtoTAR'] = (temp['20wkRollingAverageRange']/temp['20wkTotalAverageRange']) - 1
    temp['15wkRARtoTAR'] = (temp['15wkRollingAverageRange']/temp['15wkTotalAverageRange']) - 1
    temp['12wkRARtoTAR'] = (temp['12wkRollingAverageRange']/temp['12wkTotalAverageRange']) - 1
    temp['11wkRARtoTAR'] = (temp['11wkRollingAverageRange']/temp['11wkTotalAverageRange']) - 1
    temp['10wkRARtoTAR'] = (temp['10wkRollingAverageRange']/temp['10wkTotalAverageRange']) - 1
    temp['9wkRARtoTAR'] = (temp['9wkRollingAverageRange']/temp['9wkTotalAverageRange']) - 1
    temp['8wkRARtoTAR'] = (temp['8wkRollingAverageRange']/temp['8wkTotalAverageRange']) - 1    
    temp['7wkRARtoTAR'] = (temp['7wkRollingAverageRange']/temp['7wkTotalAverageRange']) - 1
    temp['6wkRARtoTAR'] = (temp['6wkRollingAverageRange']/temp['6wkTotalAverageRange']) - 1
    temp['5wkRARtoTAR'] = (temp['5wkRollingAverageRange']/temp['5wkTotalAverageRange']) - 1
    temp['4wkRARtoTAR'] = (temp['4wkRollingAverageRange']/temp['4wkTotalAverageRange']) - 1
    temp['3wkRARtoTAR'] = (temp['3wkRollingAverageRange']/temp['3wkTotalAverageRange']) - 1
    temp['2wkRARtoTAR'] = (temp['2wkRollingAverageRange']/temp['2wkTotalAverageRange']) - 1
    temp['1wkRARtoTAR'] = (temp['1wkRollingAverageRange']/temp['1wkTotalAverageRange']) - 1
    temp['4dayRARtoTAR'] = (temp['4dayRollingAverageRange']/temp['4dayTotalAverageRange']) - 1
    temp['3dayRARtoTAR'] = (temp['3dayRollingAverageRange']/temp['3dayTotalAverageRange']) - 1
    temp['2dayRARtoTAR'] = (temp['2dayRollingAverageRange']/temp['2dayTotalAverageRange']) - 1
    
    #B/O, B/D ratio
    temp['100wkBreakOutRatio'] = temp['High']/temp['100wkHigh'] #If > 1, then moving higher
    temp['100wkBreakDownRatio'] = temp['Low']/temp['100wkLow'] #If > 1, then moving lower
    temp['90wkBreakOutRatio'] = temp['High']/temp['90wkHigh'] #If > 1, then moving higher
    temp['90wkBreakDownRatio'] = temp['Low']/temp['90wkLow'] #If > 1, then moving lower
    temp['80wkBreakOutRatio'] = temp['High']/temp['80wkHigh'] #If > 1, then moving higher
    temp['80wkBreakDownRatio'] = temp['Low']/temp['80wkLow'] #If > 1, then moving lower
    temp['70wkBreakOutRatio'] = temp['High']/temp['70wkHigh'] #If > 1, then moving higher
    temp['70wkBreakDownRatio'] = temp['Low']/temp['70wkLow'] #If > 1, then moving lower
    temp['65wkBreakOutRatio'] = temp['High']/temp['65wkHigh'] #If > 1, then moving higher
    temp['65wkBreakDownRatio'] = temp['Low']/temp['65wkLow'] #If > 1, then moving lower
    temp['60wkBreakOutRatio'] = temp['High']/temp['60wkHigh'] #If > 1, then moving higher
    temp['60wkBreakDownRatio'] = temp['Low']/temp['60wkLow'] #If > 1, then moving lower
    temp['55wkBreakOutRatio'] = temp['High']/temp['55wkHigh'] #If > 1, then moving higher
    temp['55wkBreakDownRatio'] = temp['Low']/temp['55wkLow'] #If > 1, then moving lower
    temp['52wkBreakOutRatio'] = temp['High']/temp['52wkHigh'] #If > 1, then moving higher
    temp['52wkBreakDownRatio'] = temp['Low']/temp['52wkLow'] #If > 1, then moving lower
    temp['45wkBreakOutRatio'] = temp['High']/temp['45wkHigh'] #If > 1, then moving higher
    temp['45wkBreakDownRatio'] = temp['Low']/temp['45wkLow'] #If > 1, then moving lower
    temp['40wkBreakOutRatio'] = temp['High']/temp['40wkHigh'] #If > 1, then moving higher
    temp['40wkBreakDownRatio'] = temp['Low']/temp['40wkLow'] #If > 1, then moving lower
    temp['35wkBreakOutRatio'] = temp['High']/temp['35wkHigh'] #If > 1, then moving higher
    temp['35wkBreakDownRatio'] = temp['Low']/temp['35wkLow'] #If > 1, then moving lower
    temp['30wkBreakOutRatio'] = temp['High']/temp['30wkHigh'] #If > 1, then moving higher
    temp['30wkBreakDownRatio'] = temp['Low']/temp['30wkLow'] #If > 1, then moving lower
    temp['25wkBreakOutRatio'] = temp['High']/temp['25wkHigh'] #If > 1, then moving higher
    temp['25wkBreakDownRatio'] = temp['Low']/temp['25wkLow'] #If > 1, then moving lower
    temp['20wkBreakOutRatio'] = temp['High']/temp['20wkHigh'] #If > 1, then moving higher
    temp['20wkBreakDownRatio'] = temp['Low']/temp['20wkLow'] #If > 1, then moving lower
    temp['15wkBreakOutRatio'] = temp['High']/temp['15wkHigh'] #If > 1, then moving higher
    temp['15wkBreakDownRatio'] = temp['Low']/temp['15wkLow'] #If > 1, then moving lower
    temp['12wkBreakOutRatio'] = temp['High']/temp['12wkHigh'] #If > 1, then moving higher
    temp['12wkBreakDownRatio'] = temp['Low']/temp['12wkLow'] #If > 1, then moving lower
    temp['11wkBreakOutRatio'] = temp['High']/temp['11wkHigh'] #If > 1, then moving higher
    temp['11wkBreakDownRatio'] = temp['Low']/temp['11wkLow'] #If > 1, then moving lower
    temp['10wkBreakOutRatio'] = temp['High']/temp['10wkHigh'] #If > 1, then moving higher
    temp['10wkBreakDownRatio'] = temp['Low']/temp['10wkLow'] #If > 1, then moving lower
    temp['9wkBreakOutRatio'] = temp['High']/temp['9wkHigh'] #If > 1, then moving higher
    temp['9wkBreakDownRatio'] = temp['Low']/temp['9wkLow'] #If > 1, then moving lower
    temp['8wkBreakOutRatio'] = temp['High']/temp['8wkHigh'] #If > 1, then moving higher
    temp['8wkBreakDownRatio'] = temp['Low']/temp['8wkLow'] #If > 1, then moving lower
    temp['7wkBreakOutRatio'] = temp['High']/temp['7wkHigh'] #If > 1, then moving higher
    temp['7wkBreakDownRatio'] = temp['Low']/temp['7wkLow'] #If > 1, then moving lower
    temp['6wkBreakOutRatio'] = temp['High']/temp['6wkHigh'] #If > 1, then moving higher
    temp['6wkBreakDownRatio'] = temp['Low']/temp['6wkLow'] #If > 1, then moving lower
    temp['5wkBreakOutRatio'] = temp['High']/temp['5wkHigh'] #If > 1, then moving higher
    temp['5wkBreakDownRatio'] = temp['Low']/temp['5wkLow'] #If > 1, then moving lower
    temp['4wkBreakOutRatio'] = temp['High']/temp['4wkHigh'] #If > 1, then moving higher
    temp['4wkBreakDownRatio'] = temp['Low']/temp['4wkLow'] #If > 1, then moving lower
    temp['3wkBreakOutRatio'] = temp['High']/temp['3wkHigh'] #If > 1, then moving higher
    temp['3wkBreakDownRatio'] = temp['Low']/temp['3wkLow'] #If > 1, then moving lower
    temp['2wkBreakOutRatio'] = temp['High']/temp['2wkHigh'] #If > 1, then moving higher
    temp['2wkBreakDownRatio'] = temp['Low']/temp['2wkLow'] #If > 1, then moving lower
    temp['1wkBreakOutRatio'] = temp['High']/temp['1wkHigh'] #If > 1, then moving higher
    temp['1wkBreakDownRatio'] = temp['Low']/temp['1wkLow'] #If > 1, then moving lower
    temp['4dayBreakOutRatio'] = temp['High']/temp['4dayHigh'] #If > 1, then moving higher
    temp['4dayBreakDownRatio'] = temp['Low']/temp['4dayLow'] #If > 1, then moving lower
    temp['3dayBreakOutRatio'] = temp['High']/temp['3dayHigh'] #If > 1, then moving higher
    temp['3dayBreakDownRatio'] = temp['Low']/temp['3dayLow'] #If > 1, then moving lower
    temp['2dayBreakOutRatio'] = temp['High']/temp['2dayHigh'] #If > 1, then moving higher
    temp['2dayBreakDownRatio'] = temp['Low']/temp['2dayLow'] #If > 1, then moving lower

    #Over all time, the average return per period & average Std Dev per period; STATIC
    temp['100wkTotalAverageReturn'] = temp['LogRet'].mean() * 500 
    temp['100wkTotalAverageStdDev'] = temp['LogRet'].std()*np.sqrt(500)
    temp['90wkTotalAverageReturn'] = temp['LogRet'].mean() * 450
    temp['90wkTotalAverageStdDev'] = temp['LogRet'].std()*np.sqrt(450)
    temp['80wkTotalAverageReturn'] = temp['LogRet'].mean() * 400
    temp['80wkTotalAverageStdDev'] = temp['LogRet'].std()*np.sqrt(400)
    temp['70wkTotalAverageReturn'] = temp['LogRet'].mean() * 350
    temp['70wkTotalAverageStdDev'] = temp['LogRet'].std()*np.sqrt(350)
    temp['65wkTotalAverageReturn'] = temp['LogRet'].mean() * 325
    temp['65wkTotalAverageStdDev'] = temp['LogRet'].std()*np.sqrt(325)        
    temp['60wkTotalAverageReturn'] = temp['LogRet'].mean() * 300
    temp['60wkTotalAverageStdDev'] = temp['LogRet'].std()*np.sqrt(300)
    temp['55wkTotalAverageReturn'] = temp['LogRet'].mean() * 275
    temp['55wkTotalAverageStdDev'] = temp['LogRet'].std()*np.sqrt(275)
    temp['52wkTotalAverageReturn'] = temp['LogRet'].mean() * 252
    temp['52wkTotalAverageStdDev'] = temp['LogRet'].std()*np.sqrt(252)
    temp['45wkTotalAverageReturn'] = temp['LogRet'].mean() * 225
    temp['45wkTotalAverageStdDev'] = temp['LogRet'].std()*np.sqrt(225)
    temp['40wkTotalAverageReturn'] = temp['LogRet'].mean() * 200
    temp['40wkTotalAverageStdDev'] = temp['LogRet'].std()*np.sqrt(200)
    temp['35wkTotalAverageReturn'] = temp['LogRet'].mean() * 175
    temp['35wkTotalAverageStdDev'] = temp['LogRet'].std()*np.sqrt(175)
    temp['30wkTotalAverageReturn'] = temp['LogRet'].mean() * 150
    temp['30wkTotalAverageStdDev'] = temp['LogRet'].std()*np.sqrt(150)
    temp['25wkTotalAverageReturn'] = temp['LogRet'].mean() * 125
    temp['25wkTotalAverageStdDev'] = temp['LogRet'].std()*np.sqrt(125)
    temp['20wkTotalAverageReturn'] = temp['LogRet'].mean() * 100
    temp['20wkTotalAverageStdDev'] = temp['LogRet'].std()*np.sqrt(100)
    temp['15wkTotalAverageReturn'] = temp['LogRet'].mean() * 75
    temp['15wkTotalAverageStdDev'] = temp['LogRet'].std()*np.sqrt(75)
    temp['12wkTotalAverageReturn'] = temp['LogRet'].mean() * 60
    temp['12wkTotalAverageStdDev'] = temp['LogRet'].std()*np.sqrt(60)
    temp['11wkTotalAverageReturn'] = temp['LogRet'].mean() * 55
    temp['11wkTotalAverageStdDev'] = temp['LogRet'].std()*np.sqrt(55)
    temp['10wkTotalAverageReturn'] = temp['LogRet'].mean() * 50
    temp['10wkTotalAverageStdDev'] = temp['LogRet'].std()*np.sqrt(50)
    temp['9wkTotalAverageReturn'] = temp['LogRet'].mean() * 45
    temp['9wkTotalAverageStdDev'] = temp['LogRet'].std()*np.sqrt(45)
    temp['8wkTotalAverageReturn'] = temp['LogRet'].mean() * 40
    temp['8wkTotalAverageStdDev'] = temp['LogRet'].std()*np.sqrt(40)
    temp['7wkTotalAverageReturn'] = temp['LogRet'].mean() * 35
    temp['7wkTotalAverageStdDev'] = temp['LogRet'].std()*np.sqrt(35)
    temp['6wkTotalAverageReturn'] = temp['LogRet'].mean() * 30
    temp['6wkTotalAverageStdDev'] = temp['LogRet'].std()*np.sqrt(30)
    temp['5wkTotalAverageReturn'] = temp['LogRet'].mean() * 25
    temp['5wkTotalAverageStdDev'] = temp['LogRet'].std()*np.sqrt(25)
    temp['4wkTotalAverageReturn'] = temp['LogRet'].mean() * 20
    temp['4wkTotalAverageStdDev'] = temp['LogRet'].std()*np.sqrt(20)
    temp['3wkTotalAverageReturn'] = temp['LogRet'].mean() * 15
    temp['3wkTotalAverageStdDev'] = temp['LogRet'].std()*np.sqrt(15)
    temp['2wkTotalAverageReturn'] = temp['LogRet'].mean() * 10
    temp['2wkTotalAverageStdDev'] = temp['LogRet'].std()*np.sqrt(10)
    temp['1wkTotalAverageReturn'] = temp['LogRet'].mean() * 5
    temp['1wkTotalAverageStdDev'] = temp['LogRet'].std()*np.sqrt(5)
    temp['4dayTotalAverageReturn'] = temp['LogRet'].mean() * 4
    temp['4dayTotalAverageStdDev'] = temp['LogRet'].std()*np.sqrt(4)
    temp['3dayTotalAverageReturn'] = temp['LogRet'].mean() * 3
    temp['3dayTotalAverageStdDev'] = temp['LogRet'].std()*np.sqrt(3)
    temp['2dayTotalAverageReturn'] = temp['LogRet'].mean() * 2
    temp['2dayTotalAverageStdDev'] = temp['LogRet'].std()*np.sqrt(2)
    
    #CV IS STATIC = not rolling
    temp['100wkCoefficientOfVaration'] = (
            temp['100wkTotalAverageStdDev']/temp['100wkTotalAverageReturn'])
    temp['90wkCoefficientOfVaration'] = (
            temp['90wkTotalAverageStdDev']/temp['90wkTotalAverageReturn'])
    temp['80wkCoefficientOfVaration'] = (
            temp['80wkTotalAverageStdDev']/temp['80wkTotalAverageReturn'])
    temp['70wkCoefficientOfVaration'] = (
            temp['70wkTotalAverageStdDev']/temp['70wkTotalAverageReturn'])
    temp['65wkCoefficientOfVaration'] = (
            temp['65wkTotalAverageStdDev']/temp['65wkTotalAverageReturn'])
    temp['60wkCoefficientOfVaration'] = (
            temp['60wkTotalAverageStdDev']/temp['60wkTotalAverageReturn'])
    temp['55wkCoefficientOfVaration'] = (
            temp['55wkTotalAverageStdDev']/temp['55wkTotalAverageReturn'])
    temp['52wkCoefficientOfVaration'] = (
            temp['52wkTotalAverageStdDev']/temp['52wkTotalAverageReturn'])
    temp['45wkCoefficientOfVaration'] = (
            temp['45wkTotalAverageStdDev']/temp['45wkTotalAverageReturn'])
    temp['40wkCoefficientOfVaration'] = (
            temp['40wkTotalAverageStdDev']/temp['40wkTotalAverageReturn'])
    temp['35wkCoefficientOfVaration'] = (
            temp['35wkTotalAverageStdDev']/temp['35wkTotalAverageReturn'])
    temp['30wkCoefficientOfVaration'] = (
            temp['30wkTotalAverageStdDev']/temp['30wkTotalAverageReturn'])
    temp['25wkCoefficientOfVaration'] = (
            temp['25wkTotalAverageStdDev']/temp['25wkTotalAverageReturn'])
    temp['20wkCoefficientOfVaration'] = (
            temp['20wkTotalAverageStdDev']/temp['20wkTotalAverageReturn'])
    temp['15wkCoefficientOfVaration'] = (
            temp['15wkTotalAverageStdDev']/temp['15wkTotalAverageReturn'])
    temp['12CoefficientOfVaration'] = (
            temp['12wkTotalAverageStdDev']/temp['12wkTotalAverageReturn'])
    temp['11wkCoefficientOfVaration'] = (
            temp['11wkTotalAverageStdDev']/temp['11wkTotalAverageReturn'])
    temp['10wkCoefficientOfVaration'] = (
            temp['10wkTotalAverageStdDev']/temp['10wkTotalAverageReturn'])
    temp['9wkCoefficientOfVaration'] = (
            temp['9wkTotalAverageStdDev']/temp['9wkTotalAverageReturn'])
    temp['8wkCoefficientOfVaration'] = (
            temp['8wkTotalAverageStdDev']/temp['8wkTotalAverageReturn'])
    temp['7wkCoefficientOfVaration'] = (
            temp['7wkTotalAverageStdDev']/temp['7wkTotalAverageReturn'])
    temp['6wkCoefficientOfVaration'] = (
            temp['6wkTotalAverageStdDev']/temp['6wkTotalAverageReturn'])
    temp['5wkCoefficientOfVaration'] = (
            temp['5wkTotalAverageStdDev']/temp['5wkTotalAverageReturn'])
    temp['4wkCoefficientOfVaration'] = (
            temp['4wkTotalAverageStdDev']/temp['4wkTotalAverageReturn'])
    temp['3wkCoefficientOfVaration'] = (
            temp['3wkTotalAverageStdDev']/temp['3wkTotalAverageReturn'])
    temp['2wkCoefficientOfVaration'] = (
            temp['2wkTotalAverageStdDev']/temp['2wkTotalAverageReturn'])
    temp['1wkCoefficientOfVaration'] = (
            temp['1wkTotalAverageStdDev']/temp['1wkTotalAverageReturn'])
    temp['4dayCoefficientOfVaration'] = (
            temp['4dayTotalAverageStdDev']/temp['4dayTotalAverageReturn'])
    temp['3dayCoefficientOfVaration'] = (
            temp['3dayTotalAverageStdDev']/temp['3dayTotalAverageReturn'])
    temp['2dayCoefficientOfVaration'] = (
            temp['2dayTotalAverageStdDev']/temp['2dayTotalAverageReturn'])
            
    #Over rolling period, Average return during period; DYNAMIC
    temp['100wkRollingAverageReturn'] = temp['LogRet'].rolling(
                                     center=False, window = 500).mean()
    temp['90wkRollingAverageReturn'] = temp['LogRet'].rolling(
                                     center=False, window = 450).mean()                                         
    temp['80wkRollingAverageReturn'] = temp['LogRet'].rolling(
                                     center=False, window = 400).mean()
    temp['70wkRollingAverageReturn'] = temp['LogRet'].rolling(
                                     center=False, window = 350).mean()
    temp['65wkRollingAverageReturn'] = temp['LogRet'].rolling(
                                     center=False, window = 325).mean()   
    temp['60wkRollingAverageReturn'] = temp['LogRet'].rolling(
                                     center=False, window = 300).mean()
    temp['55wkRollingAverageReturn'] = temp['LogRet'].rolling(
                                     center=False, window = 275).mean()
    temp['52wkRollingAverageReturn'] = temp['LogRet'].rolling(
                                     center=False, window = 252).mean()
    temp['45wkRollingAverageReturn'] = temp['LogRet'].rolling(
                                     center=False, window = 225).mean()
    temp['40wkRollingAverageReturn'] = temp['LogRet'].rolling(
                                     center=False, window = 200).mean()
    temp['35wkRollingAverageReturn'] = temp['LogRet'].rolling(
                                     center=False, window = 175).mean()
    temp['30wkRollingAverageReturn'] = temp['LogRet'].rolling(
                                     center=False, window = 150).mean()
    temp['25wkRollingAverageReturn'] = temp['LogRet'].rolling(
                                     center=False, window = 125).mean()
    temp['20wkRollingAverageReturn'] = temp['LogRet'].rolling(
                                     center=False, window = 100).mean()
    temp['15wkRollingAverageReturn'] = temp['LogRet'].rolling(
                                     center=False, window = 75).mean()
    temp['12wkRollingAverageReturn'] = temp['LogRet'].rolling(
                                     center=False, window = 60).mean()
    temp['11wkRollingAverageReturn'] = temp['LogRet'].rolling(
                                     center=False, window = 55).mean()
    temp['10wkRollingAverageReturn'] = temp['LogRet'].rolling(
                                     center=False, window = 50).mean()
    temp['9wkRollingAverageReturn'] = temp['LogRet'].rolling(
                                     center=False, window = 45).mean()
    temp['8wkRollingAverageReturn'] = temp['LogRet'].rolling(
                                     center=False, window = 40).mean()
    temp['7wkRollingAverageReturn'] = temp['LogRet'].rolling(
                                     center=False, window = 35).mean()
    temp['6wkRollingAverageReturn'] = temp['LogRet'].rolling(
                                     center=False, window = 30).mean()
    temp['5wkRollingAverageReturn'] = temp['LogRet'].rolling(
                                     center=False, window = 25).mean()                                         
    temp['4wkRollingAverageReturn'] = temp['LogRet'].rolling(
                                     center=False, window = 20).mean()
    temp['3wkRollingAverageReturn'] = temp['LogRet'].rolling(
                                     center=False, window = 15).mean()
    temp['2wkRollingAverageReturn'] = temp['LogRet'].rolling(
                                     center=False, window = 10).mean()
    temp['1wkRollingAverageReturn'] = temp['LogRet'].rolling(
                                     center=False, window = 5).mean()
    temp['4dayRollingAverageReturn'] = temp['LogRet'].rolling(
                                     center=False, window = 4).mean()
    temp['3dayRollingAverageReturn'] = temp['LogRet'].rolling(
                                     center=False, window = 3).mean()
    temp['2dayRollingAverageReturn'] = temp['LogRet'].rolling(
                                     center=False, window = 2).mean()                                         
        
    #Over rolling period, Average Std Dev during period; DYNAMIC
    temp['100wkRollingStdDev'] = temp['LogRet'].rolling(
                                     center=False, window = 500).std()
    temp['90wkRollingStdDev'] = temp['LogRet'].rolling(
                                     center=False, window = 450).std()                                         
    temp['80wkRollingStdDev'] = temp['LogRet'].rolling(
                                     center=False, window = 400).std()
    temp['70wkRollingStdDev'] = temp['LogRet'].rolling(
                                     center=False, window = 350).std()
    temp['65wkRollingStdDev'] = temp['LogRet'].rolling(
                                     center=False, window = 325).std()   
    temp['60wkRollingStdDev'] = temp['LogRet'].rolling(
                                     center=False, window = 300).std()
    temp['55wkRollingStdDev'] = temp['LogRet'].rolling(
                                     center=False, window = 275).std()
    temp['52wkRollingStdDev'] = temp['LogRet'].rolling(
                                     center=False, window = 252).std()
    temp['45wkRollingStdDev'] = temp['LogRet'].rolling(
                                     center=False, window = 225).std()
    temp['40wkRollingStdDev'] = temp['LogRet'].rolling(
                                     center=False, window = 200).std()
    temp['35wkRollingStdDev'] = temp['LogRet'].rolling(
                                     center=False, window = 175).std()
    temp['30wkRollingStdDev'] = temp['LogRet'].rolling(
                                     center=False, window = 150).std()
    temp['25wkRollingStdDev'] = temp['LogRet'].rolling(
                                     center=False, window = 125).std()
    temp['20wkRollingStdDev'] = temp['LogRet'].rolling(
                                     center=False, window = 100).std()
    temp['15wkRollingStdDev'] = temp['LogRet'].rolling(
                                     center=False, window = 75).std()
    temp['12wkRollingStdDev'] = temp['LogRet'].rolling(
                                     center=False, window = 60).std()
    temp['11wkRollingStdDev'] = temp['LogRet'].rolling(
                                     center=False, window = 55).std()
    temp['10wkRollingStdDev'] = temp['LogRet'].rolling(
                                     center=False, window = 50).std()
    temp['9wkRollingStdDev'] = temp['LogRet'].rolling(
                                     center=False, window = 45).std()
    temp['8wkRollingStdDev'] = temp['LogRet'].rolling(
                                     center=False, window = 40).std()
    temp['7wkRollingStdDev'] = temp['LogRet'].rolling(
                                     center=False, window = 35).std()
    temp['6wkRollingStdDev'] = temp['LogRet'].rolling(
                                     center=False, window = 30).std()
    temp['5wkRollingStdDev'] = temp['LogRet'].rolling(
                                     center=False, window = 25).std()                                         
    temp['4wkRollingStdDev'] = temp['LogRet'].rolling(
                                     center=False, window = 20).std()
    temp['3wkRollingStdDev'] = temp['LogRet'].rolling(
                                     center=False, window = 15).std()
    temp['2wkRollingStdDev'] = temp['LogRet'].rolling(
                                     center=False, window = 10).std()
    temp['1wkRollingStdDev'] = temp['LogRet'].rolling(
                                     center=False, window = 5).std()
    temp['4dayRollingStdDev'] = temp['LogRet'].rolling(
                                     center=False, window = 4).std()
    temp['3dayRollingStdDev'] = temp['LogRet'].rolling(
                                     center=False, window = 3).std()
    temp['2dayRollingStdDev'] = temp['LogRet'].rolling(
                                     center=False, window = 2).std()
    
    #Rate of Change (ROC) in %
    temp['100wkRateOfChange'] = (temp['Adj Close'] - temp['Adj Close'].shift(500)
                                      ) / temp['Adj Close'].shift(500)  
    temp['100wkRateOfChange'] = temp['100wkRateOfChange'].fillna(0)
    temp['90wkRateOfChange'] = (temp['Adj Close'] - temp['Adj Close'].shift(450)
                                      ) / temp['Adj Close'].shift(450)  
    temp['90wkRateOfChange'] = temp['90wkRateOfChange'].fillna(0)
    temp['80wkRateOfChange'] = (temp['Adj Close'] - temp['Adj Close'].shift(400)
                                      ) / temp['Adj Close'].shift(400)  
    temp['80wkRateOfChange'] = temp['80wkRateOfChange'].fillna(0)
    temp['70wkRateOfChange'] = (temp['Adj Close'] - temp['Adj Close'].shift(350)
                                      ) / temp['Adj Close'].shift(350)  
    temp['70wkRateOfChange'] = temp['70wkRateOfChange'].fillna(0)
    temp['65wkRateOfChange'] = (temp['Adj Close'] - temp['Adj Close'].shift(325)
                                      ) / temp['Adj Close'].shift(325)  
    temp['65wkRateOfChange'] = temp['65wkRateOfChange'].fillna(0)
    temp['60wkRateOfChange'] = (temp['Adj Close'] - temp['Adj Close'].shift(300)
                                      ) / temp['Adj Close'].shift(300)  
    temp['60wkRateOfChange'] = temp['60wkRateOfChange'].fillna(0)
    temp['55wkRateOfChange'] = (temp['Adj Close'] - temp['Adj Close'].shift(275)
                                      ) / temp['Adj Close'].shift(275)  
    temp['55wkRateOfChange'] = temp['55wkRateOfChange'].fillna(0)
    temp['52wkRateOfChange'] = (temp['Adj Close'] - temp['Adj Close'].shift(252)
                                      ) / temp['Adj Close'].shift(252)  
    temp['52wkRateOfChange'] = temp['52wkRateOfChange'].fillna(0)
    temp['45wkRateOfChange'] = (temp['Adj Close'] - temp['Adj Close'].shift(225)
                                      ) / temp['Adj Close'].shift(225)  
    temp['45wkRateOfChange'] = temp['45wkRateOfChange'].fillna(0)
    temp['40wkRateOfChange'] = (temp['Adj Close'] - temp['Adj Close'].shift(200)
                                      ) / temp['Adj Close'].shift(200)  
    temp['40wkRateOfChange'] = temp['40wkRateOfChange'].fillna(0)
    temp['35wkRateOfChange'] = (temp['Adj Close'] - temp['Adj Close'].shift(175)
                                      ) / temp['Adj Close'].shift(175)  
    temp['35wkRateOfChange'] = temp['35wkRateOfChange'].fillna(0)
    temp['30wkRateOfChange'] = (temp['Adj Close'] - temp['Adj Close'].shift(150)
                                      ) / temp['Adj Close'].shift(150)  
    temp['30wkRateOfChange'] = temp['30wkRateOfChange'].fillna(0)
    temp['25wkRateOfChange'] = (temp['Adj Close'] - temp['Adj Close'].shift(125)
                                      ) / temp['Adj Close'].shift(125)  
    temp['25wkRateOfChange'] = temp['25wkRateOfChange'].fillna(0)
    temp['20wkRateOfChange'] = (temp['Adj Close'] - temp['Adj Close'].shift(100)
                                      ) / temp['Adj Close'].shift(100)  
    temp['20wkRateOfChange'] = temp['20wkRateOfChange'].fillna(0)
    temp['15wkRateOfChange'] = (temp['Adj Close'] - temp['Adj Close'].shift(75)
                                      ) / temp['Adj Close'].shift(75)  
    temp['15wkRateOfChange'] = temp['15wkRateOfChange'].fillna(0)
    temp['12wkRateOfChange'] = (temp['Adj Close'] - temp['Adj Close'].shift(60)
                                      ) / temp['Adj Close'].shift(60)  
    temp['12wkRateOfChange'] = temp['12wkRateOfChange'].fillna(0)
    temp['11wkRateOfChange'] = (temp['Adj Close'] - temp['Adj Close'].shift(55)
                                      ) / temp['Adj Close'].shift(55)  
    temp['11wkRateOfChange'] = temp['11wkRateOfChange'].fillna(0)
    temp['10wkRateOfChange'] = (temp['Adj Close'] - temp['Adj Close'].shift(50)
                                      ) / temp['Adj Close'].shift(50)  
    temp['10wkRateOfChange'] = temp['10wkRateOfChange'].fillna(0)
    temp['9wkRateOfChange'] = (temp['Adj Close'] - temp['Adj Close'].shift(45)
                                      ) / temp['Adj Close'].shift(45)  
    temp['9wkRateOfChange'] = temp['9wkRateOfChange'].fillna(0)
    temp['8wkRateOfChange'] = (temp['Adj Close'] - temp['Adj Close'].shift(40)
                                      ) / temp['Adj Close'].shift(40)  
    temp['8wkRateOfChange'] = temp['8wkRateOfChange'].fillna(0)
    temp['7wkRateOfChange'] = (temp['Adj Close'] - temp['Adj Close'].shift(35)
                                      ) / temp['Adj Close'].shift(35)  
    temp['7wkRateOfChange'] = temp['7wkRateOfChange'].fillna(0)
    temp['6wkRateOfChange'] = (temp['Adj Close'] - temp['Adj Close'].shift(30)
                                      ) / temp['Adj Close'].shift(30)  
    temp['6wkRateOfChange'] = temp['6wkRateOfChange'].fillna(0)
    temp['5wkRateOfChange'] = (temp['Adj Close'] - temp['Adj Close'].shift(25)
                                      ) / temp['Adj Close'].shift(25)  
    temp['5wkRateOfChange'] = temp['5wkRateOfChange'].fillna(0)
    temp['4wkRateOfChange'] = (temp['Adj Close'] - temp['Adj Close'].shift(20)
                                      ) / temp['Adj Close'].shift(20)  
    temp['4wkRateOfChange'] = temp['4wkRateOfChange'].fillna(0)
    temp['3wkRateOfChange'] = (temp['Adj Close'] - temp['Adj Close'].shift(15)
                                      ) / temp['Adj Close'].shift(15)  
    temp['3wkRateOfChange'] = temp['3wkRateOfChange'].fillna(0)
    temp['2wkRateOfChange'] = (temp['Adj Close'] - temp['Adj Close'].shift(10)
                                      ) / temp['Adj Close'].shift(10)  
    temp['2wkRateOfChange'] = temp['2wkRateOfChange'].fillna(0)        
    temp['1wkRateOfChange'] = (temp['Adj Close'] - temp['Adj Close'].shift(5)
                                      ) / temp['Adj Close'].shift(5)  
    temp['1wkRateOfChange'] = temp['1wkRateOfChange'].fillna(0)
    temp['4dayRateOfChange'] = (temp['Adj Close'] - temp['Adj Close'].shift(4)
                                      ) / temp['Adj Close'].shift(4)  
    temp['4dayRateOfChange'] = temp['4dayRateOfChange'].fillna(0)
    temp['3dayRateOfChange'] = (temp['Adj Close'] - temp['Adj Close'].shift(3)
                                      ) / temp['Adj Close'].shift(3)  
    temp['3dayRateOfChange'] = temp['3dayRateOfChange'].fillna(0)        
    temp['2dayRateOfChange'] = (temp['Adj Close'] - temp['Adj Close'].shift(2)
                                      ) / temp['Adj Close'].shift(2)  
    temp['2dayRateOfChange'] = temp['2dayRateOfChange'].fillna(0)

    #Over rolling period Average volume in period
    temp['100wkRollingAverageVolume'] = temp['Volume'].rolling(
                                       center=False, window=500).mean()
    temp['90wkRollingAverageVolume'] = temp['Volume'].rolling(
                                       center=False, window=450).mean()
    temp['80wkRollingAverageVolume'] = temp['Volume'].rolling(
                                       center=False, window=400).mean()
    temp['70wkRollingAverageVolume'] = temp['Volume'].rolling(
                                       center=False, window=350).mean()
    temp['65wkRollingAverageVolume'] = temp['Volume'].rolling(
                                       center=False, window=325).mean()
    temp['60wkRollingAverageVolume'] = temp['Volume'].rolling(
                                       center=False, window=300).mean()
    temp['55wkRollingAverageVolume'] = temp['Volume'].rolling(
                                       center=False, window=275).mean()
    temp['52wkRollingAverageVolume'] = temp['Volume'].rolling(
                                       center=False, window=252).mean()
    temp['45wkRollingAverageVolume'] = temp['Volume'].rolling(
                                       center=False, window=225).mean()
    temp['40wkRollingAverageVolume'] = temp['Volume'].rolling(
                                       center=False, window=200).mean()
    temp['35wkRollingAverageVolume'] = temp['Volume'].rolling(
                                       center=False, window=175).mean()
    temp['30wkRollingAverageVolume'] = temp['Volume'].rolling(
                                       center=False, window=150).mean()
    temp['25wkRollingAverageVolume'] = temp['Volume'].rolling(
                                       center=False, window=125).mean()
    temp['20wkRollingAverageVolume'] = temp['Volume'].rolling(
                                       center=False, window=100).mean()
    temp['15wkRollingAverageVolume'] = temp['Volume'].rolling(
                                       center=False, window=75).mean()
    temp['12wkRollingAverageVolume'] = temp['Volume'].rolling(
                                       center=False, window=60).mean()
    temp['11wkRollingAverageVolume'] = temp['Volume'].rolling(
                                       center=False, window=55).mean()
    temp['10wkRollingAverageVolume'] = temp['Volume'].rolling(
                                       center=False, window=50).mean()
    temp['9wkRollingAverageVolume'] = temp['Volume'].rolling(
                                       center=False, window=45).mean()
    temp['8wkRollingAverageVolume'] = temp['Volume'].rolling(
                                       center=False, window=40).mean()
    temp['7wkRollingAverageVolume'] = temp['Volume'].rolling(
                                       center=False, window=35).mean()
    temp['6wkRollingAverageVolume'] = temp['Volume'].rolling(
                                       center=False, window=30).mean()
    temp['5wkRollingAverageVolume'] = temp['Volume'].rolling(
                                       center=False, window=25).mean()
    temp['4wkRollingAverageVolume'] = temp['Volume'].rolling(
                                       center=False, window=20).mean()
    temp['3wkRollingAverageVolume'] = temp['Volume'].rolling(
                                       center=False, window=15).mean()
    temp['2wkRollingAverageVolume'] = temp['Volume'].rolling(
                                       center=False, window=10).mean()
    temp['1wkRollingAverageVolume'] = temp['Volume'].rolling(
                                       center=False, window=5).mean()   
    temp['4dayRollingAverageVolume'] = temp['Volume'].rolling(
                                       center=False, window=4).mean()  
    temp['3dayRollingAverageVolume'] = temp['Volume'].rolling(
                                       center=False, window=3).mean()  
    temp['2dayRollingAverageVolume'] = temp['Volume'].rolling(
                                       center=False, window=2).mean()                                             
                                       
    #Front period over Average Return
    temp['100wkRollingReturnOverAverage'] = (temp['100wkRollingAverageReturn']/ 
                                            temp['100wkTotalAverageReturn'])
    temp['90wkRollingReturnOverAverage'] = (temp['90wkRollingAverageReturn']/ 
                                            temp['90wkTotalAverageReturn'])
    temp['80wkRollingReturnOverAverage'] = (temp['80wkRollingAverageReturn']/ 
                                            temp['80wkTotalAverageReturn'])
    temp['70wkRollingReturnOverAverage'] = (temp['70wkRollingAverageReturn']/ 
                                            temp['70wkTotalAverageReturn'])
    temp['65wkRollingReturnOverAverage'] = (temp['65wkRollingAverageReturn']/ 
                                            temp['65wkTotalAverageReturn'])
    temp['60wkRollingReturnOverAverage'] = (temp['60wkRollingAverageReturn']/ 
                                            temp['60wkTotalAverageReturn'])
    temp['55wkRollingReturnOverAverage'] = (temp['55wkRollingAverageReturn']/ 
                                            temp['55wkTotalAverageReturn'])
    temp['52wkRollingReturnOverAverage'] = (temp['52wkRollingAverageReturn']/ 
                                            temp['52wkTotalAverageReturn'])
    temp['45wkRollingReturnOverAverage'] = (temp['45wkRollingAverageReturn']/ 
                                            temp['45wkTotalAverageReturn'])
    temp['40wkRollingReturnOverAverage'] = (temp['40wkRollingAverageReturn']/ 
                                            temp['40wkTotalAverageReturn'])
    temp['35wkRollingReturnOverAverage'] = (temp['35wkRollingAverageReturn']/ 
                                            temp['35wkTotalAverageReturn'])
    temp['30wkRollingReturnOverAverage'] = (temp['30wkRollingAverageReturn']/ 
                                            temp['30wkTotalAverageReturn'])
    temp['25wkRollingReturnOverAverage'] = (temp['25wkRollingAverageReturn']/ 
                                            temp['25wkTotalAverageReturn'])
    temp['20wkRollingReturnOverAverage'] = (temp['20wkRollingAverageReturn']/ 
                                            temp['20wkTotalAverageReturn'])
    temp['15wkRollingReturnOverAverage'] = (temp['15wkRollingAverageReturn']/ 
                                            temp['15wkTotalAverageReturn'])
    temp['12wkRollingReturnOverAverage'] = (temp['12wkRollingAverageReturn']/ 
                                            temp['12wkTotalAverageReturn'])
    temp['11wkRollingReturnOverAverage'] = (temp['11wkRollingAverageReturn']/ 
                                            temp['11wkTotalAverageReturn'])
    temp['10wkRollingReturnOverAverage'] = (temp['10wkRollingAverageReturn']/ 
                                            temp['10wkTotalAverageReturn'])
    temp['9wkRollingReturnOverAverage'] =  (temp['9wkRollingAverageReturn']/ 
                                            temp['9wkTotalAverageReturn'])
    temp['8wkRollingReturnOverAverage'] =  (temp['8wkRollingAverageReturn']/ 
                                            temp['8wkTotalAverageReturn'])
    temp['7wkRollingReturnOverAverage'] =  (temp['7wkRollingAverageReturn']/ 
                                            temp['7wkTotalAverageReturn'])
    temp['6wkRollingReturnOverAverage'] =  (temp['6wkRollingAverageReturn']/ 
                                            temp['6wkTotalAverageReturn'])
    temp['5wkRollingReturnOverAverage'] =  (temp['5wkRollingAverageReturn']/ 
                                            temp['5wkTotalAverageReturn'])
    temp['4wkRollingReturnOverAverage'] =  (temp['4wkRollingAverageReturn']/ 
                                            temp['4wkTotalAverageReturn'])
    temp['3wkRollingReturnOverAverage'] =  (temp['3wkRollingAverageReturn']/ 
                                            temp['3wkTotalAverageReturn'])
    temp['2wkRollingReturnOverAverage'] =  (temp['2wkRollingAverageReturn']/ 
                                            temp['2wkTotalAverageReturn'])
    temp['1wkRollingReturnOverAverage'] =  (temp['1wkRollingAverageReturn']/ 
                                            temp['1wkTotalAverageReturn'])
    temp['4dayRollingReturnOverAverage'] = (temp['4dayRollingAverageReturn']/ 
                                            temp['4dayTotalAverageReturn'])
    temp['3dayRollingReturnOverAverage'] = (temp['3dayRollingAverageReturn']/ 
                                            temp['3dayTotalAverageReturn'])
    temp['2dayRollingReturnOverAverage'] = (temp['2dayRollingAverageReturn']/ 
                                            temp['2dayTotalAverageReturn'])                                                

    #Front period over Average Std Dev // These are ratios                                
    temp['100wkRollingStdDevOverAverage'] = (temp['100wkRollingStdDev']/ 
                                            temp['100wkTotalAverageStdDev'])
    temp['90wkRollingStdDevOverAverage'] = (temp['90wkRollingStdDev']/ 
                                            temp['90wkTotalAverageStdDev'])
    temp['80wkRollingStdDevOverAverage'] = (temp['80wkRollingStdDev']/ 
                                            temp['80wkTotalAverageStdDev'])
    temp['70wkRollingStdDevOverAverage'] = (temp['70wkRollingStdDev']/ 
                                            temp['70wkTotalAverageStdDev'])
    temp['65wkRollingStdDevOverAverage'] = (temp['65wkRollingStdDev']/ 
                                            temp['65wkTotalAverageStdDev'])
    temp['60wkRollingStdDevOverAverage'] = (temp['60wkRollingStdDev']/ 
                                            temp['60wkTotalAverageStdDev'])
    temp['55wkRollingStdDevOverAverage'] = (temp['55wkRollingStdDev']/ 
                                            temp['55wkTotalAverageStdDev'])
    temp['52wkRollingStdDevOverAverage'] = (temp['52wkRollingStdDev']/ 
                                            temp['52wkTotalAverageStdDev'])
    temp['45wkRollingStdDevOverAverage'] = (temp['45wkRollingStdDev']/ 
                                            temp['45wkTotalAverageStdDev'])
    temp['40wkRollingStdDevOverAverage'] = (temp['40wkRollingStdDev']/ 
                                            temp['40wkTotalAverageStdDev'])
    temp['35wkRollingStdDevOverAverage'] = (temp['35wkRollingStdDev']/ 
                                            temp['35wkTotalAverageStdDev'])
    temp['30wkRollingStdDevOverAverage'] = (temp['30wkRollingStdDev']/ 
                                            temp['30wkTotalAverageStdDev'])
    temp['25wkRollingStdDevOverAverage'] = (temp['25wkRollingStdDev']/ 
                                            temp['25wkTotalAverageStdDev'])
    temp['20wkRollingStdDevOverAverage'] = (temp['20wkRollingStdDev']/ 
                                            temp['20wkTotalAverageStdDev'])
    temp['15wkRollingStdDevOverAverage'] = (temp['15wkRollingStdDev']/ 
                                            temp['15wkTotalAverageStdDev'])
    temp['12wkRollingStdDevOverAverage'] = (temp['12wkRollingStdDev']/ 
                                            temp['12wkTotalAverageStdDev'])
    temp['11wkRollingStdDevOverAverage'] = (temp['11wkRollingStdDev']/ 
                                            temp['11wkTotalAverageStdDev'])
    temp['10wkRollingStdDevOverAverage'] = (temp['10wkRollingStdDev']/ 
                                            temp['10wkTotalAverageStdDev'])
    temp['9wkRollingStdDevOverAverage'] = (temp['9wkRollingStdDev']/ 
                                            temp['9wkTotalAverageStdDev'])
    temp['8wkRollingStdDevOverAverage'] = (temp['8wkRollingStdDev']/ 
                                            temp['8wkTotalAverageStdDev'])
    temp['7wkRollingStdDevOverAverage'] = (temp['7wkRollingStdDev']/ 
                                            temp['7wkTotalAverageStdDev'])
    temp['6wkRollingStdDevOverAverage'] = (temp['6wkRollingStdDev']/ 
                                            temp['6wkTotalAverageStdDev'])
    temp['5wkRollingStdDevOverAverage'] = (temp['5wkRollingStdDev']/ 
                                            temp['5wkTotalAverageStdDev'])
    temp['4wkRollingStdDevOverAverage'] = (temp['4wkRollingStdDev']/ 
                                            temp['4wkTotalAverageStdDev'])
    temp['3wkRollingStdDevOverAverage'] = (temp['3wkRollingStdDev']/ 
                                            temp['3wkTotalAverageStdDev'])
    temp['2wkRollingStdDevOverAverage'] = (temp['2wkRollingStdDev']/ 
                                            temp['2wkTotalAverageStdDev'])
    temp['1wkRollingStdDevOverAverage'] = (temp['1wkRollingStdDev']/ 
                                            temp['1wkTotalAverageStdDev'])
    temp['4dayRollingStdDevOverAverage'] = (temp['4dayRollingStdDev']/ 
                                            temp['4dayTotalAverageStdDev'])
    temp['3dayRollingStdDevOverAverage'] = (temp['3dayRollingStdDev']/ 
                                            temp['3dayTotalAverageStdDev'])
    temp['2dayRollingStdDevOverAverage'] = (temp['2dayRollingStdDev']/ 
                                            temp['2dayTotalAverageStdDev'])                        
    
    #N period ATR Setup
    temp['Method1'] = temp['High'] - temp['Low']
    temp['Method2'] = abs((temp['High'] - temp['Adj Close'].shift(1)))
    temp['Method3'] = abs((temp['Low'] - temp['Adj Close'].shift(1)))
    temp['Method1'] = temp['Method1'].fillna(0)
    temp['Method2'] = temp['Method2'].fillna(0)
    temp['Method3'] = temp['Method3'].fillna(0)
    temp['TrueRange'] = temp[['Method1','Method2','Method3']].max(axis = 1)

    #ATR Calculation
    temp['100wkATRPoints'] = temp['TrueRange'].rolling(window = 500, center=False).mean()        
    temp['100wkATRPercent'] = temp['100wkATRPoints'] / temp['Adj Close']
    temp['90wkATRPoints'] = temp['TrueRange'].rolling(window = 450, center=False).mean()        
    temp['90wkATRPercent'] = temp['90wkATRPoints'] / temp['Adj Close']
    temp['80wkATRPoints'] = temp['TrueRange'].rolling(window = 400, center=False).mean()        
    temp['80wkATRPercent'] = temp['80wkATRPoints'] / temp['Adj Close']
    temp['70wkATRPoints'] = temp['TrueRange'].rolling(window = 350, center=False).mean()        
    temp['70wkATRPercent'] = temp['70wkATRPoints'] / temp['Adj Close']
    temp['65wkATRPoints'] = temp['TrueRange'].rolling(window = 325, center=False).mean()        
    temp['65wkATRPercent'] = temp['65wkATRPoints'] / temp['Adj Close']
    temp['60wkATRPoints'] = temp['TrueRange'].rolling(window = 300, center=False).mean()        
    temp['60wkATRPercent'] = temp['60wkATRPoints'] / temp['Adj Close']
    temp['55wkATRPoints'] = temp['TrueRange'].rolling(window = 275, center=False).mean()        
    temp['55wkATRPercent'] = temp['55wkATRPoints'] / temp['Adj Close']
    temp['52wkATRPoints'] = temp['TrueRange'].rolling(window = 252, center=False).mean()        
    temp['52wkATRPercent'] = temp['52wkATRPoints'] / temp['Adj Close']
    temp['45wkATRPoints'] = temp['TrueRange'].rolling(window = 225, center=False).mean()        
    temp['45wkATRPercent'] = temp['45wkATRPoints'] / temp['Adj Close']
    temp['40wkATRPoints'] = temp['TrueRange'].rolling(window = 200, center=False).mean()        
    temp['40wkATRPercent'] = temp['40wkATRPoints'] / temp['Adj Close']
    temp['35wkATRPoints'] = temp['TrueRange'].rolling(window = 175, center=False).mean()        
    temp['35wkATRPercent'] = temp['35wkATRPoints'] / temp['Adj Close']
    temp['30wkATRPoints'] = temp['TrueRange'].rolling(window = 150, center=False).mean()        
    temp['30wkATRPercent'] = temp['30wkATRPoints'] / temp['Adj Close']
    temp['25wkATRPoints'] = temp['TrueRange'].rolling(window = 125, center=False).mean()        
    temp['25wkATRPercent'] = temp['25wkATRPoints'] / temp['Adj Close']
    temp['20wkATRPoints'] = temp['TrueRange'].rolling(window = 100, center=False).mean()        
    temp['20wkATRPercent'] = temp['20wkATRPoints'] / temp['Adj Close']
    temp['15wkATRPoints'] = temp['TrueRange'].rolling(window = 75, center=False).mean()        
    temp['15wkATRPercent'] = temp['15wkATRPoints'] / temp['Adj Close']
    temp['12wkATRPoints'] = temp['TrueRange'].rolling(window = 60, center=False).mean()        
    temp['12wkATRPercent'] = temp['12wkATRPoints'] / temp['Adj Close']
    temp['11wkATRPoints'] = temp['TrueRange'].rolling(window = 55, center=False).mean()        
    temp['11wkATRPercent'] = temp['11wkATRPoints'] / temp['Adj Close']
    temp['10wkATRPoints'] = temp['TrueRange'].rolling(window = 50, center=False).mean()        
    temp['10wkATRPercent'] = temp['10wkATRPoints'] / temp['Adj Close']
    temp['9wkATRPoints'] = temp['TrueRange'].rolling(window = 45, center=False).mean()        
    temp['9wkATRPercent'] = temp['9wkATRPoints'] / temp['Adj Close']
    temp['8wkATRPoints'] = temp['TrueRange'].rolling(window = 40, center=False).mean()        
    temp['8wkATRPercent'] = temp['8wkATRPoints'] / temp['Adj Close']
    temp['7wkATRPoints'] = temp['TrueRange'].rolling(window = 35, center=False).mean()        
    temp['7wkATRPercent'] = temp['7wkATRPoints'] / temp['Adj Close']
    temp['6wkATRPoints'] = temp['TrueRange'].rolling(window = 30, center=False).mean()        
    temp['6wkATRPercent'] = temp['6wkATRPoints'] / temp['Adj Close']
    temp['5wkATRPoints'] = temp['TrueRange'].rolling(window = 25, center=False).mean()        
    temp['5wkATRPercent'] = temp['5wkATRPoints'] / temp['Adj Close']
    temp['4wkATRPoints'] = temp['TrueRange'].rolling(window = 20, center=False).mean()        
    temp['4wkATRPercent'] = temp['4wkATRPoints'] / temp['Adj Close']
    temp['3wkATRPoints'] = temp['TrueRange'].rolling(window = 15, center=False).mean()        
    temp['3wkATRPercent'] = temp['3wkATRPoints'] / temp['Adj Close']
    temp['2wkATRPoints'] = temp['TrueRange'].rolling(window = 10, center=False).mean()        
    temp['2wkATRPercent'] = temp['2wkATRPoints'] / temp['Adj Close']
    temp['1wkATRPoints'] = temp['TrueRange'].rolling(window = 5, center=False).mean()        
    temp['1wkATRPercent'] = temp['1wkATRPoints'] / temp['Adj Close']
    temp['4dayATRPoints'] = temp['TrueRange'].rolling(window = 4, center=False).mean()        
    temp['4dayATRPercent'] = temp['4dayATRPoints'] / temp['Adj Close']
    temp['3dayATRPoints'] = temp['TrueRange'].rolling(window = 3, center=False).mean()        
    temp['3dayATRPercent'] = temp['3dayATRPoints'] / temp['Adj Close']
    temp['2dayATRPoints'] = temp['TrueRange'].rolling(window = 2, center=False).mean()        
    temp['2dayATRPercent'] = temp['2dayATRPoints'] / temp['Adj Close']        
   
    #STATIC Total Average ATR
    temp['100wkTotalAverageATR'] = temp['100wkATRPercent'].mean() * 500 
    temp['90wkTotalAverageATR'] = temp['90wkATRPercent'].mean() * 450 
    temp['80wkTotalAverageATR'] = temp['80wkATRPercent'].mean() * 400 
    temp['70wkTotalAverageATR'] = temp['70wkATRPercent'].mean() * 350 
    temp['65wkTotalAverageATR'] = temp['65wkATRPercent'].mean() * 325 
    temp['60wkTotalAverageATR'] = temp['60wkATRPercent'].mean() * 300 
    temp['55wkTotalAverageATR'] = temp['55wkATRPercent'].mean() * 275 
    temp['52wkTotalAverageATR'] = temp['52wkATRPercent'].mean() * 252 
    temp['45wkTotalAverageATR'] = temp['45wkATRPercent'].mean() * 225
    temp['40wkTotalAverageATR'] = temp['40wkATRPercent'].mean() * 200
    temp['35wkTotalAverageATR'] = temp['35wkATRPercent'].mean() * 175 
    temp['30wkTotalAverageATR'] = temp['30wkATRPercent'].mean() * 150 
    temp['25wkTotalAverageATR'] = temp['25wkATRPercent'].mean() * 125 
    temp['20wkTotalAverageATR'] = temp['20wkATRPercent'].mean() * 100 
    temp['15wkTotalAverageATR'] = temp['15wkATRPercent'].mean() * 75 
    temp['12wkTotalAverageATR'] = temp['12wkATRPercent'].mean() * 60 
    temp['11wkTotalAverageATR'] = temp['11wkATRPercent'].mean() * 55 
    temp['10wkTotalAverageATR'] = temp['10wkATRPercent'].mean() * 50 
    temp['9wkTotalAverageATR'] = temp['9wkATRPercent'].mean() * 45 
    temp['8wkTotalAverageATR'] = temp['8wkATRPercent'].mean() * 40 
    temp['7wkTotalAverageATR'] = temp['7wkATRPercent'].mean() * 35 
    temp['6wkTotalAverageATR'] = temp['6wkATRPercent'].mean() * 30 
    temp['5wkTotalAverageATR'] = temp['5wkATRPercent'].mean() * 25 
    temp['4wkTotalAverageATR'] = temp['4wkATRPercent'].mean() * 20 
    temp['3wkTotalAverageATR'] = temp['3wkATRPercent'].mean() * 15 
    temp['2wkTotalAverageATR'] = temp['2wkATRPercent'].mean() * 10
    temp['1wkTotalAverageATR'] = temp['1wkATRPercent'].mean() * 5 
    temp['4dayTotalAverageATR'] = temp['4dayATRPercent'].mean() * 4 
    temp['3dayTotalAverageATR'] = temp['3dayATRPercent'].mean() * 3 
    temp['2dayTotalAverageATR'] = temp['2dayATRPercent'].mean() * 2 

    #DYNAMIC Rolling Average ATR
    temp['100wkRollingAverageATR'] = temp['100wkATRPercent'].rolling(
                                     center=False, window = 500).mean()
    temp['90wkRollingAverageATR'] = temp['90wkATRPercent'].rolling(
                                     center=False, window = 450).mean()
    temp['80wkRollingAverageATR'] = temp['80wkATRPercent'].rolling(
                                     center=False, window = 400).mean()
    temp['70wkRollingAverageATR'] = temp['70wkATRPercent'].rolling(
                                     center=False, window = 350).mean()
    temp['65wkRollingAverageATR'] = temp['65wkATRPercent'].rolling(
                                     center=False, window = 325).mean()
    temp['60wkRollingAverageATR'] = temp['60wkATRPercent'].rolling(
                                     center=False, window = 300).mean()
    temp['55wkRollingAverageATR'] = temp['55wkATRPercent'].rolling(
                                     center=False, window = 275).mean()
    temp['52wkRollingAverageATR'] = temp['52wkATRPercent'].rolling(
                                     center=False, window = 252).mean()
    temp['45wkRollingAverageATR'] = temp['45wkATRPercent'].rolling(
                                     center=False, window = 225).mean()
    temp['40wkRollingAverageATR'] = temp['40wkATRPercent'].rolling(
                                     center=False, window = 200).mean()
    temp['35wkRollingAverageATR'] = temp['35wkATRPercent'].rolling(
                                     center=False, window = 175).mean()
    temp['30wkRollingAverageATR'] = temp['30wkATRPercent'].rolling(
                                     center=False, window = 150).mean()
    temp['25wkRollingAverageATR'] = temp['25wkATRPercent'].rolling(
                                     center=False, window = 125).mean()
    temp['20wkRollingAverageATR'] = temp['20wkATRPercent'].rolling(
                                     center=False, window = 100).mean()
    temp['15wkRollingAverageATR'] = temp['15wkATRPercent'].rolling(
                                     center=False, window = 75).mean()
    temp['12wkRollingAverageATR'] = temp['12wkATRPercent'].rolling(
                                     center=False, window = 60).mean()
    temp['11wkRollingAverageATR'] = temp['11wkATRPercent'].rolling(
                                     center=False, window = 55).mean()
    temp['10wkRollingAverageATR'] = temp['10wkATRPercent'].rolling(
                                     center=False, window = 50).mean()
    temp['9wkRollingAverageATR'] = temp['9wkATRPercent'].rolling(
                                     center=False, window = 45).mean()
    temp['8wkRollingAverageATR'] = temp['8wkATRPercent'].rolling(
                                     center=False, window = 40).mean()
    temp['7wkRollingAverageATR'] = temp['7wkATRPercent'].rolling(
                                     center=False, window = 35).mean()
    temp['6wkRollingAverageATR'] = temp['6wkATRPercent'].rolling(
                                     center=False, window = 30).mean()
    temp['5wkRollingAverageATR'] = temp['5wkATRPercent'].rolling(
                                     center=False, window = 25).mean()
    temp['4wkRollingAverageATR'] = temp['4wkATRPercent'].rolling(
                                     center=False, window = 20).mean()
    temp['3wkRollingAverageATR'] = temp['3wkATRPercent'].rolling(
                                     center=False, window = 15).mean()
    temp['2wkRollingAverageATR'] = temp['2wkATRPercent'].rolling(
                                     center=False, window = 10).mean()
    temp['1wkRollingAverageATR'] = temp['1wkATRPercent'].rolling(
                                     center=False, window = 5).mean()
    temp['4dayRollingAverageATR'] = temp['4dayATRPercent'].rolling(
                                     center=False, window = 4).mean()
    temp['3dayRollingAverageATR'] = temp['3dayATRPercent'].rolling(
                                     center=False, window = 3).mean()
    temp['2dayRollingAverageATR'] = temp['2dayATRPercent'].rolling(
                                     center=False, window = 2).mean()            
    
    #DYNAMIC RAATR/TAATR - 1   
    temp['100wkRAATRtoTAATR'] = (temp['100wkRollingAverageATR']/temp['100wkTotalAverageATR']) - 1
    temp['90wkRAATRtoTAATR'] = (temp['90wkRollingAverageATR']/temp['90wkTotalAverageATR']) - 1
    temp['80wkRAATRtoTAATR'] = (temp['80wkRollingAverageATR']/temp['80wkTotalAverageATR']) - 1
    temp['70wkRAATRtoTAATR'] = (temp['70wkRollingAverageATR']/temp['70wkTotalAverageATR']) - 1
    temp['65wkRAATRtoTAATR'] = (temp['65wkRollingAverageATR']/temp['65wkTotalAverageATR']) - 1
    temp['60wkRAATRtoTAATR'] = (temp['60wkRollingAverageATR']/temp['60wkTotalAverageATR']) - 1
    temp['55wkRAATRtoTAATR'] = (temp['55wkRollingAverageATR']/temp['55wkTotalAverageATR']) - 1
    temp['52wkRAATRtoTAATR'] = (temp['52wkRollingAverageATR']/temp['52wkTotalAverageATR']) - 1
    temp['45wkRAATRtoTAATR'] = (temp['45wkRollingAverageATR']/temp['45wkTotalAverageATR']) - 1
    temp['40wkRAATRtoTAATR'] = (temp['40wkRollingAverageATR']/temp['40wkTotalAverageATR']) - 1
    temp['35wkRAATRtoTAATR'] = (temp['35wkRollingAverageATR']/temp['35wkTotalAverageATR']) - 1
    temp['30wkRAATRtoTAATR'] = (temp['30wkRollingAverageATR']/temp['30wkTotalAverageATR']) - 1
    temp['25wkRAATRtoTAATR'] = (temp['25wkRollingAverageATR']/temp['25wkTotalAverageATR']) - 1
    temp['20wkRAATRtoTAATR'] = (temp['20wkRollingAverageATR']/temp['20wkTotalAverageATR']) - 1
    temp['15wkRAATRtoTAATR'] = (temp['15wkRollingAverageATR']/temp['15wkTotalAverageATR']) - 1
    temp['12wkRAATRtoTAATR'] = (temp['12wkRollingAverageATR']/temp['12wkTotalAverageATR']) - 1
    temp['11wkRAATRtoTAATR'] = (temp['11wkRollingAverageATR']/temp['11wkTotalAverageATR']) - 1
    temp['10wkRAATRtoTAATR'] = (temp['10wkRollingAverageATR']/temp['10wkTotalAverageATR']) - 1
    temp['9wkRAATRtoTAATR'] = (temp['9wkRollingAverageATR']/temp['9wkTotalAverageATR']) - 1
    temp['8wkRAATRtoTAATR'] = (temp['8wkRollingAverageATR']/temp['8wkTotalAverageATR']) - 1
    temp['7wkRAATRtoTAATR'] = (temp['7wkRollingAverageATR']/temp['7wkTotalAverageATR']) - 1
    temp['6wkRAATRtoTAATR'] = (temp['6wkRollingAverageATR']/temp['6wkTotalAverageATR']) - 1
    temp['5wkRAATRtoTAATR'] = (temp['5wkRollingAverageATR']/temp['5wkTotalAverageATR']) - 1
    temp['4wkRAATRtoTAATR'] = (temp['4wkRollingAverageATR']/temp['4wkTotalAverageATR']) - 1
    temp['3wkRAATRtoTAATR'] = (temp['3wkRollingAverageATR']/temp['3wkTotalAverageATR']) - 1
    temp['2wkRAATRtoTAATR'] = (temp['2wkRollingAverageATR']/temp['2wkTotalAverageATR']) - 1
    temp['1wkRAATRtoTAATR'] = (temp['1wkRollingAverageATR']/temp['1wkTotalAverageATR']) - 1
    temp['4dayRAATRtoTAATR'] = (temp['4dayRollingAverageATR']/temp['4dayTotalAverageATR']) - 1
    temp['3dayRAATRtoTAATR'] = (temp['3dayRollingAverageATR']/temp['3dayTotalAverageATR']) - 1    
    temp['2dayRAATRtoTAATR'] = (temp['2dayRollingAverageATR']/temp['2dayTotalAverageATR']) - 1    
               
    #DYNAMIC ATR percent / Range percent               
    temp['100wkATRtoRange'] = temp['100wkATRPercent'] / temp['100wkRangePercent']
    temp['90wkATRtoRange'] = temp['90wkATRPercent'] / temp['90wkRangePercent']
    temp['80wkATRtoRange'] = temp['80wkATRPercent'] / temp['80wkRangePercent']
    temp['70wkATRtoRange'] = temp['70wkATRPercent'] / temp['70wkRangePercent']
    temp['65wkATRtoRange'] = temp['65wkATRPercent'] / temp['65wkRangePercent']
    temp['60wkATRtoRange'] = temp['60wkATRPercent'] / temp['60wkRangePercent']
    temp['55wkATRtoRange'] = temp['55wkATRPercent'] / temp['55wkRangePercent']
    temp['52wkATRtoRange'] = temp['52wkATRPercent'] / temp['52wkRangePercent']
    temp['45wkATRtoRange'] = temp['45wkATRPercent'] / temp['45wkRangePercent']
    temp['40wkATRtoRange'] = temp['40wkATRPercent'] / temp['40wkRangePercent']
    temp['35wkATRtoRange'] = temp['35wkATRPercent'] / temp['35wkRangePercent']
    temp['30wkATRtoRange'] = temp['30wkATRPercent'] / temp['30wkRangePercent']
    temp['25wkATRtoRange'] = temp['25wkATRPercent'] / temp['25wkRangePercent']
    temp['20wkATRtoRange'] = temp['20wkATRPercent'] / temp['20wkRangePercent']
    temp['15wkATRtoRange'] = temp['15wkATRPercent'] / temp['15wkRangePercent']
    temp['12wkATRtoRange'] = temp['12wkATRPercent'] / temp['12wkRangePercent']
    temp['11wkATRtoRange'] = temp['11wkATRPercent'] / temp['11wkRangePercent']
    temp['10wkATRtoRange'] = temp['10wkATRPercent'] / temp['10wkRangePercent']
    temp['9wkATRtoRange'] = temp['9wkATRPercent'] / temp['9wkRangePercent']
    temp['8wkATRtoRange'] = temp['8wkATRPercent'] / temp['8wkRangePercent']
    temp['7wkATRtoRange'] = temp['7wkATRPercent'] / temp['7wkRangePercent']
    temp['6wkATRtoRange'] = temp['6wkATRPercent'] / temp['6wkRangePercent']
    temp['5wkATRtoRange'] = temp['5wkATRPercent'] / temp['5wkRangePercent']
    temp['4wkATRtoRange'] = temp['4wkATRPercent'] / temp['4wkRangePercent']
    temp['3wkATRtoRange'] = temp['3wkATRPercent'] / temp['3wkRangePercent']
    temp['2wkATRtoRange'] = temp['2wkATRPercent'] / temp['2wkRangePercent']
    temp['1wkATRtoRange'] = temp['1wkATRPercent'] / temp['1wkRangePercent']
    temp['4dayATRtoRange'] = temp['4dayATRPercent'] / temp['4dayRangePercent']
    temp['3dayATRtoRange'] = temp['3dayATRPercent'] / temp['3dayRangePercent']
    temp['2dayATRtoRange'] = temp['2dayATRPercent'] / temp['2dayRangePercent']
    
    #STATIC Average ATRtoRange
    temp['100wkTotalAverageATRtoRange'] = temp['100wkATRtoRange'].mean() * 500
    temp['90wkTotalAverageATRtoRange'] = temp['90wkATRtoRange'].mean() * 450
    temp['80wkTotalAverageATRtoRange'] = temp['80wkATRtoRange'].mean() * 400
    temp['70wkTotalAverageATRtoRange'] = temp['70wkATRtoRange'].mean() * 350
    temp['65wkTotalAverageATRtoRange'] = temp['65wkATRtoRange'].mean() * 325
    temp['60wkTotalAverageATRtoRange'] = temp['60wkATRtoRange'].mean() * 300
    temp['55wkTotalAverageATRtoRange'] = temp['55wkATRtoRange'].mean() * 275
    temp['52wkTotalAverageATRtoRange'] = temp['52wkATRtoRange'].mean() * 250
    temp['45wkTotalAverageATRtoRange'] = temp['45wkATRtoRange'].mean() * 225
    temp['40wkTotalAverageATRtoRange'] = temp['40wkATRtoRange'].mean() * 200
    temp['35wkTotalAverageATRtoRange'] = temp['35wkATRtoRange'].mean() * 175
    temp['30wkTotalAverageATRtoRange'] = temp['30wkATRtoRange'].mean() * 150
    temp['25wkTotalAverageATRtoRange'] = temp['25wkATRtoRange'].mean() * 125
    temp['20wkTotalAverageATRtoRange'] = temp['20wkATRtoRange'].mean() * 100    
    temp['15wkTotalAverageATRtoRange'] = temp['15wkATRtoRange'].mean() * 75
    temp['12wkTotalAverageATRtoRange'] = temp['12wkATRtoRange'].mean() * 60
    temp['11wkTotalAverageATRtoRange'] = temp['11wkATRtoRange'].mean() * 55
    temp['10wkTotalAverageATRtoRange'] = temp['10wkATRtoRange'].mean() * 50
    temp['9wkTotalAverageATRtoRange'] = temp['9wkATRtoRange'].mean() * 45
    temp['8wkTotalAverageATRtoRange'] = temp['8wkATRtoRange'].mean() * 40    
    temp['7wkTotalAverageATRtoRange'] = temp['7wkATRtoRange'].mean() * 35
    temp['6wkTotalAverageATRtoRange'] = temp['6wkATRtoRange'].mean() * 30
    temp['5wkTotalAverageATRtoRange'] = temp['5wkATRtoRange'].mean() * 25
    temp['4wkTotalAverageATRtoRange'] = temp['4wkATRtoRange'].mean() * 20    
    temp['3wkTotalAverageATRtoRange'] = temp['3wkATRtoRange'].mean() * 15    
    temp['2wkTotalAverageATRtoRange'] = temp['2wkATRtoRange'].mean() * 10    
    temp['1wkTotalAverageATRtoRange'] = temp['1wkATRtoRange'].mean() * 5
    temp['4dayTotalAverageATRtoRange'] = temp['4dayATRtoRange'].mean() * 4
    temp['3dayTotalAverageATRtoRange'] = temp['3dayATRtoRange'].mean() * 3 
    temp['2dayTotalAverageATRtoRange'] = temp['2dayATRtoRange'].mean() * 2    
    
    #DYNAMIC Rolling Average ATRtoRange
    temp['100wkRollingAverageATRtoRange'] = temp['100wkATRtoRange'].rolling(
                                     center=False, window = 500).mean()
    temp['90wkRollingAverageATRtoRange'] = temp['90wkATRtoRange'].rolling(
                                     center=False, window = 450).mean()
    temp['80wkRollingAverageATRtoRange'] = temp['80wkATRtoRange'].rolling(
                                     center=False, window = 400).mean()
    temp['70wkRollingAverageATRtoRange'] = temp['70wkATRtoRange'].rolling(
                                     center=False, window = 350).mean()
    temp['65wkRollingAverageATRtoRange'] = temp['65wkATRtoRange'].rolling(
                                     center=False, window = 325).mean()
    temp['60wkRollingAverageATRtoRange'] = temp['60wkATRtoRange'].rolling(
                                     center=False, window = 300).mean()
    temp['55wkRollingAverageATRtoRange'] = temp['55wkATRtoRange'].rolling(
                                     center=False, window = 275).mean()
    temp['52wkRollingAverageATRtoRange'] = temp['52wkATRtoRange'].rolling(
                                     center=False, window = 250).mean()
    temp['45wkRollingAverageATRtoRange'] = temp['45wkATRtoRange'].rolling(
                                     center=False, window = 225).mean()
    temp['40wkRollingAverageATRtoRange'] = temp['40wkATRtoRange'].rolling(
                                     center=False, window = 200).mean()
    temp['35wkRollingAverageATRtoRange'] = temp['35wkATRtoRange'].rolling(
                                     center=False, window = 175).mean()
    temp['30wkRollingAverageATRtoRange'] = temp['30wkATRtoRange'].rolling(
                                     center=False, window = 150).mean()
    temp['25wkRollingAverageATRtoRange'] = temp['25wkATRtoRange'].rolling(
                                     center=False, window = 125).mean()
    temp['20wkRollingAverageATRtoRange'] = temp['20wkATRtoRange'].rolling(
                                     center=False, window = 100).mean()
    temp['15wkRollingAverageATRtoRange'] = temp['15wkATRtoRange'].rolling(
                                     center=False, window = 75).mean()
    temp['12wkRollingAverageATRtoRange'] = temp['12wkATRtoRange'].rolling(
                                     center=False, window = 60).mean()
    temp['11wkRollingAverageATRtoRange'] = temp['11wkATRtoRange'].rolling(
                                     center=False, window = 55).mean()
    temp['10wkRollingAverageATRtoRange'] = temp['10wkATRtoRange'].rolling(
                                     center=False, window = 50).mean()
    temp['9wkRollingAverageATRtoRange'] = temp['9wkATRtoRange'].rolling(
                                     center=False, window = 45).mean()
    temp['8wkRollingAverageATRtoRange'] = temp['8wkATRtoRange'].rolling(
                                     center=False, window = 40).mean()
    temp['7wkRollingAverageATRtoRange'] = temp['7wkATRtoRange'].rolling(
                                     center=False, window = 35).mean()
    temp['6wkRollingAverageATRtoRange'] = temp['6wkATRtoRange'].rolling(
                                     center=False, window = 30).mean()
    temp['5wkRollingAverageATRtoRange'] = temp['5wkATRtoRange'].rolling(
                                     center=False, window = 25).mean()
    temp['4wkRollingAverageATRtoRange'] = temp['4wkATRtoRange'].rolling(
                                     center=False, window = 20).mean()
    temp['3wkRollingAverageATRtoRange'] = temp['3wkATRtoRange'].rolling(
                                     center=False, window = 15).mean()
    temp['2wkRollingAverageATRtoRange'] = temp['2wkATRtoRange'].rolling(
                                     center=False, window = 10).mean()
    temp['1wkRollingAverageATRtoRange'] = temp['1wkATRtoRange'].rolling(
                                     center=False, window = 5).mean()
    temp['4dayRollingAverageATRtoRange'] = temp['4dayATRtoRange'].rolling(
                                     center=False, window = 4).mean()
    temp['3dayRollingAverageATRtoRange'] = temp['3dayATRtoRange'].rolling(
                                     center=False, window = 3).mean()
    temp['2dayRollingAverageATRtoRange'] = temp['2dayATRtoRange'].rolling(
                                     center=False, window = 2).mean()                                     

    #Efficiency (is normalized across markets by Diff/ATR)                                          
    temp['100wkCloseDiff'] = temp['Adj Close'] - temp['Adj Close'].shift(500)
    temp['100wkEfficiency'] = temp['100wkCloseDiff'] / temp['100wkATRPoints'] 
    temp['90wkCloseDiff'] = temp['Adj Close'] - temp['Adj Close'].shift(450)
    temp['90wkEfficiency'] = temp['90wkCloseDiff'] / temp['90wkATRPoints'] 
    temp['80wkCloseDiff'] = temp['Adj Close'] - temp['Adj Close'].shift(400)
    temp['80wkEfficiency'] = temp['80wkCloseDiff'] / temp['80wkATRPoints'] 
    temp['70wkCloseDiff'] = temp['Adj Close'] - temp['Adj Close'].shift(350)
    temp['70wkEfficiency'] = temp['70wkCloseDiff'] / temp['70wkATRPoints'] 
    temp['65wkCloseDiff'] = temp['Adj Close'] - temp['Adj Close'].shift(325)
    temp['65wkEfficiency'] = temp['65wkCloseDiff'] / temp['65wkATRPoints'] 
    temp['60wkCloseDiff'] = temp['Adj Close'] - temp['Adj Close'].shift(300)
    temp['60wkEfficiency'] = temp['60wkCloseDiff'] / temp['60wkATRPoints'] 
    temp['55wkCloseDiff'] = temp['Adj Close'] - temp['Adj Close'].shift(275)
    temp['55wkEfficiency'] = temp['55wkCloseDiff'] / temp['55wkATRPoints'] 
    temp['52wkCloseDiff'] = temp['Adj Close'] - temp['Adj Close'].shift(252)
    temp['52wkEfficiency'] = temp['52wkCloseDiff'] / temp['52wkATRPoints'] 
    temp['45wkCloseDiff'] = temp['Adj Close'] - temp['Adj Close'].shift(225)
    temp['45wkEfficiency'] = temp['45wkCloseDiff'] / temp['45wkATRPoints'] 
    temp['40wkCloseDiff'] = temp['Adj Close'] - temp['Adj Close'].shift(200)
    temp['40wkEfficiency'] = temp['40wkCloseDiff'] / temp['40wkATRPoints'] 
    temp['35wkCloseDiff'] = temp['Adj Close'] - temp['Adj Close'].shift(175)
    temp['35wkEfficiency'] = temp['35wkCloseDiff'] / temp['35wkATRPoints'] 
    temp['30wkCloseDiff'] = temp['Adj Close'] - temp['Adj Close'].shift(150)
    temp['30wkEfficiency'] = temp['30wkCloseDiff'] / temp['30wkATRPoints'] 
    temp['25wkCloseDiff'] = temp['Adj Close'] - temp['Adj Close'].shift(125)
    temp['25wkEfficiency'] = temp['25wkCloseDiff'] / temp['25wkATRPoints'] 
    temp['20wkCloseDiff'] = temp['Adj Close'] - temp['Adj Close'].shift(100)
    temp['20wkEfficiency'] = temp['20wkCloseDiff'] / temp['20wkATRPoints'] 
    temp['15wkCloseDiff'] = temp['Adj Close'] - temp['Adj Close'].shift(75)
    temp['15wkEfficiency'] = temp['15wkCloseDiff'] / temp['15wkATRPoints'] 
    temp['12wkCloseDiff'] = temp['Adj Close'] - temp['Adj Close'].shift(60)
    temp['12wkEfficiency'] = temp['12wkCloseDiff'] / temp['12wkATRPoints'] 
    temp['11wkCloseDiff'] = temp['Adj Close'] - temp['Adj Close'].shift(55)
    temp['11wkEfficiency'] = temp['11wkCloseDiff'] / temp['11wkATRPoints'] 
    temp['10wkCloseDiff'] = temp['Adj Close'] - temp['Adj Close'].shift(50)
    temp['10wkEfficiency'] = temp['10wkCloseDiff'] / temp['10wkATRPoints'] 
    temp['9wkCloseDiff'] = temp['Adj Close'] - temp['Adj Close'].shift(45)
    temp['9wkEfficiency'] = temp['9wkCloseDiff'] / temp['9wkATRPoints'] 
    temp['8wkCloseDiff'] = temp['Adj Close'] - temp['Adj Close'].shift(40)
    temp['8wkEfficiency'] = temp['8wkCloseDiff'] / temp['8wkATRPoints'] 
    temp['7wkCloseDiff'] = temp['Adj Close'] - temp['Adj Close'].shift(35)
    temp['7wkEfficiency'] = temp['7wkCloseDiff'] / temp['7wkATRPoints'] 
    temp['6wkCloseDiff'] = temp['Adj Close'] - temp['Adj Close'].shift(30)
    temp['6wkEfficiency'] = temp['6wkCloseDiff'] / temp['6wkATRPoints'] 
    temp['5wkCloseDiff'] = temp['Adj Close'] - temp['Adj Close'].shift(25)
    temp['5wkEfficiency'] = temp['5wkCloseDiff'] / temp['5wkATRPoints'] 
    temp['4wkCloseDiff'] = temp['Adj Close'] - temp['Adj Close'].shift(20)
    temp['4wkEfficiency'] = temp['4wkCloseDiff'] / temp['4wkATRPoints'] 
    temp['3wkCloseDiff'] = temp['Adj Close'] - temp['Adj Close'].shift(15)
    temp['3wkEfficiency'] = temp['3wkCloseDiff'] / temp['3wkATRPoints'] 
    temp['2wkCloseDiff'] = temp['Adj Close'] - temp['Adj Close'].shift(10)
    temp['2wkEfficiency'] = temp['2wkCloseDiff'] / temp['2wkATRPoints'] 
    temp['1wkCloseDiff'] = temp['Adj Close'] - temp['Adj Close'].shift(5)
    temp['1wkEfficiency'] = temp['1wkCloseDiff'] / temp['1wkATRPoints'] 
    temp['4dayCloseDiff'] = temp['Adj Close'] - temp['Adj Close'].shift(4)
    temp['4dayEfficiency'] = temp['4dayCloseDiff'] / temp['4dayATRPoints'] 
    temp['3dayCloseDiff'] = temp['Adj Close'] - temp['Adj Close'].shift(3)
    temp['3dayEfficiency'] = temp['3dayCloseDiff'] / temp['3dayATRPoints'] 
    temp['2dayCloseDiff'] = temp['Adj Close'] - temp['Adj Close'].shift(2)
    temp['2dayEfficiency'] = temp['2dayCloseDiff'] / temp['2dayATRPoints'] 
  
    #Average rolling volume
    temp['100wkAverageRollingVolume'] = temp['Volume'].rolling(center=False, 
                                                        window=500).mean() 
    temp['90wkAverageRollingVolume'] = temp['Volume'].rolling(center=False, 
                                                        window=450).mean() 
    temp['80wkAverageRollingVolume'] = temp['Volume'].rolling(center=False, 
                                                        window=400).mean() 
    temp['70wkAverageRollingVolume'] = temp['Volume'].rolling(center=False, 
                                                        window=350).mean() 
    temp['65wkAverageRollingVolume'] = temp['Volume'].rolling(center=False, 
                                                        window=325).mean()                                                             
    temp['60wkAverageRollingVolume'] = temp['Volume'].rolling(center=False, 
                                                        window=300).mean() 
    temp['55wkAverageRollingVolume'] = temp['Volume'].rolling(center=False, 
                                                        window=275).mean() 
    temp['52wkAverageRollingVolume'] = temp['Volume'].rolling(center=False, 
                                                        window=252).mean() 
    temp['45wkAverageRollingVolume'] = temp['Volume'].rolling(center=False, 
                                                        window=225).mean() 
    temp['40wkAverageRollingVolume'] = temp['Volume'].rolling(center=False, 
                                                        window=200).mean() 
    temp['35wkAverageRollingVolume'] = temp['Volume'].rolling(center=False, 
                                                        window=175).mean() 
    temp['30wkAverageRollingVolume'] = temp['Volume'].rolling(center=False, 
                                                        window=150).mean() 
    temp['25wkAverageRollingVolume'] = temp['Volume'].rolling(center=False, 
                                                        window=125).mean()  
    temp['20wkAverageRollingVolume'] = temp['Volume'].rolling(center=False, 
                                                        window=100).mean() 
    temp['15wkAverageRollingVolume'] = temp['Volume'].rolling(center=False, 
                                                        window=75).mean() 
    temp['12wkAverageRollingVolume'] = temp['Volume'].rolling(center=False, 
                                                        window=60).mean() 
    temp['11wkAverageRollingVolume'] = temp['Volume'].rolling(center=False, 
                                                        window=55).mean()                                                             
    temp['10wkAverageRollingVolume'] = temp['Volume'].rolling(center=False, 
                                                        window=50).mean() 
    temp['9wkAverageRollingVolume'] = temp['Volume'].rolling(center=False, 
                                                        window=45).mean() 
    temp['8wkAverageRollingVolume'] = temp['Volume'].rolling(center=False, 
                                                        window=40).mean() 
    temp['7wkAverageRollingVolume'] = temp['Volume'].rolling(center=False, 
                                                        window=35).mean() 
    temp['6wkAverageRollingVolume'] = temp['Volume'].rolling(center=False, 
                                                        window=30).mean() 
    temp['5wkAverageRollingVolume'] = temp['Volume'].rolling(center=False, 
                                                        window=25).mean() 
    temp['4wkAverageRollingVolume'] = temp['Volume'].rolling(center=False, 
                                                        window=20).mean() 
    temp['3wkAverageRollingVolume'] = temp['Volume'].rolling(center=False, 
                                                        window=15).mean() 
    temp['2wkAverageRollingVolume'] = temp['Volume'].rolling(center=False, 
                                                        window=10).mean() 
    temp['1wkAverageRollingVolume'] = temp['Volume'].rolling(center=False, 
                                                        window=5).mean() 
    temp['4dayAverageRollingVolume'] = temp['Volume'].rolling(center=False, 
                                                        window=4).mean() 
    temp['3dayAverageRollingVolume'] = temp['Volume'].rolling(center=False, 
                                                        window=3).mean() 
    temp['2dayAverageRollingVolume'] = temp['Volume'].rolling(center=False, 
                                                        window=2).mean()
                                                         
    #Make also a float estimation
    temp['Float'] = 0
    
    #Simple Moving Average
    temp['100wkSMA'] = temp['Adj Close'].rolling(window=500, center=False).mean()
    temp['100wkSMA'] = temp['100wkSMA'].fillna(0)
    temp['90wkSMA'] = temp['Adj Close'].rolling(window=450, center=False).mean()
    temp['90wkSMA'] = temp['90wkSMA'].fillna(0)
    temp['80wkSMA'] = temp['Adj Close'].rolling(window=400, center=False).mean()
    temp['80wkSMA'] = temp['80wkSMA'].fillna(0)
    temp['70wkSMA'] = temp['Adj Close'].rolling(window=350, center=False).mean()
    temp['70wkSMA'] = temp['70wkSMA'].fillna(0)
    temp['65wkSMA'] = temp['Adj Close'].rolling(window=325, center=False).mean()
    temp['65wkSMA'] = temp['65wkSMA'].fillna(0)
    temp['60wkSMA'] = temp['Adj Close'].rolling(window=300, center=False).mean()
    temp['60wkSMA'] = temp['60wkSMA'].fillna(0)
    temp['55wkSMA'] = temp['Adj Close'].rolling(window=275, center=False).mean()
    temp['55wkSMA'] = temp['55wkSMA'].fillna(0)
    temp['52wkSMA'] = temp['Adj Close'].rolling(window=252, center=False).mean()
    temp['52wkSMA'] = temp['52wkSMA'].fillna(0)
    temp['45wkSMA'] = temp['Adj Close'].rolling(window=225, center=False).mean()
    temp['45wkSMA'] = temp['45wkSMA'].fillna(0)
    temp['40wkSMA'] = temp['Adj Close'].rolling(window=200, center=False).mean()
    temp['40wkSMA'] = temp['40wkSMA'].fillna(0)
    temp['35wkSMA'] = temp['Adj Close'].rolling(window=175, center=False).mean()
    temp['35wkSMA'] = temp['35wkSMA'].fillna(0)
    temp['30wkSMA'] = temp['Adj Close'].rolling(window=150, center=False).mean()
    temp['30wkSMA'] = temp['30wkSMA'].fillna(0)
    temp['25wkSMA'] = temp['Adj Close'].rolling(window=125, center=False).mean()
    temp['25wkSMA'] = temp['25wkSMA'].fillna(0)
    temp['20wkSMA'] = temp['Adj Close'].rolling(window=100, center=False).mean()
    temp['20wkSMA'] = temp['20wkSMA'].fillna(0)
    temp['15wkSMA'] = temp['Adj Close'].rolling(window=75, center=False).mean()
    temp['15wkSMA'] = temp['15wkSMA'].fillna(0)
    temp['12wkSMA'] = temp['Adj Close'].rolling(window=60, center=False).mean()
    temp['12wkSMA'] = temp['12wkSMA'].fillna(0)
    temp['11wkSMA'] = temp['Adj Close'].rolling(window=55, center=False).mean()
    temp['11wkSMA'] = temp['11wkSMA'].fillna(0)
    temp['10wkSMA'] = temp['Adj Close'].rolling(window=50, center=False).mean()
    temp['10wkSMA'] = temp['10wkSMA'].fillna(0)
    temp['9wkSMA'] = temp['Adj Close'].rolling(window=45, center=False).mean()
    temp['9wkSMA'] = temp['9wkSMA'].fillna(0)
    temp['8wkSMA'] = temp['Adj Close'].rolling(window=40, center=False).mean()
    temp['8wkSMA'] = temp['8wkSMA'].fillna(0)
    temp['7wkSMA'] = temp['Adj Close'].rolling(window=35, center=False).mean()
    temp['7wkSMA'] = temp['7wkSMA'].fillna(0)
    temp['6wkSMA'] = temp['Adj Close'].rolling(window=30, center=False).mean()
    temp['6wkSMA'] = temp['6wkSMA'].fillna(0)
    temp['5wkSMA'] = temp['Adj Close'].rolling(window=25, center=False).mean()
    temp['5wkSMA'] = temp['5wkSMA'].fillna(0)
    temp['4wkSMA'] = temp['Adj Close'].rolling(window=20, center=False).mean()
    temp['4wkSMA'] = temp['4wkSMA'].fillna(0)
    temp['3wkSMA'] = temp['Adj Close'].rolling(window=15, center=False).mean()
    temp['3wkSMA'] = temp['3wkSMA'].fillna(0)
    temp['2wkSMA'] = temp['Adj Close'].rolling(window=10, center=False).mean()
    temp['2wkSMA'] = temp['2wkSMA'].fillna(0)
    temp['1wkSMA'] = temp['Adj Close'].rolling(window=5, center=False).mean()
    temp['1wkSMA'] = temp['1wkSMA'].fillna(0)
    temp['4daySMA'] = temp['Adj Close'].rolling(window=4, center=False).mean()
    temp['4daySMA'] = temp['4daySMA'].fillna(0)
    temp['3daySMA'] = temp['Adj Close'].rolling(window=3, center=False).mean()
    temp['3daySMA'] = temp['3daySMA'].fillna(0)
    temp['2daySMA'] = temp['Adj Close'].rolling(window=2, center=False).mean()
    temp['2daySMA'] = temp['2daySMA'].fillna(0)     
    
    #Save to folder
    pd.to_pickle(temp, DL + '\\DataSources\\YahooSource\\ProcessedData\\DAY\\'
                    + p + '\\' + p)
    print(p + ' is processed and saved.')
#End timer    
end = time.time()
#Timer stats
t = round(end - start, 2)
n = round(len(os.listdir(DL + '\\DataSources\\YahooSource\\ProcessedData\\DAY\\')), 2)
#Display results
print('Yahoo processed data is full.')
print('YahooSource took ' + str(t) + ' seconds for ' + str(n) + ' tickers.')

  
# -*- coding: utf-8 -*-
"""

@author: Adam Reinhold Von Fisher - https://www.linkedin.com/in/adamrvfisher/

"""

#pandas_datareader is deprecated, use YahooGrabber
#This is the last step of a kth fold optimization tool

#Import modules
from DefRSIPredictor import DefRSIPredictor
import numpy as np
import pandas as pd
from pandas_datareader import data

#Read in data
Aggregate = pd.read_pickle('TLTAGGSHARPE023')
Aggregate = Aggregate.loc[:,~Aggregate.columns.duplicated()]
#Input ticker
ticker = 'TMF'

#Read in data
s = data.DataReader(ticker, 'yahoo', start='01/01/2007', end='01/01/2050') 
#s2 = pd.DataFrame({'Open':[1399.13],'High':[1399.13],'Low':[1386.32],'Close':[0],'Volume':[0],
#'Adj Close':[1390.72]},index = ['2017-05-03 00:00:00']) #interday
#s = pd.concat([s1,s2])
s1 = pd.read_pickle('TLTAGGAdvice07_50') # this is just for testing with a graph
s['Advice'] = s1['Advice']

#Incrementally longer time series
#ranger = range(1,len(s)+1)
#dictionary = { r : s.loc[s.index[:r],:] for r in ranger}
#triumph = []
#for r in ranger:
#    q = dictionary[r]
#    result = DefRSIPredictor(Aggregate, q)
#    triumph.append(result)
#    print(r)
#    print(result)
#TheAdvice = pd.Series(triumph, index=s.index)
#s['Advice'] = TheAdvice

#Calculate log returns
s['LogRet'] = np.log(s['Adj Close']/s['Adj Close'].shift(1)) 
s['LogRet'] = s['LogRet'].fillna(0)
#Directional methodology
s['Regime'] = np.where(s['Advice'] > .706102, 1, 0)
s['Regime'] = np.where(s['Advice'] < -.644197, -1, s['Regime'])
#Apply position to returns 
s['Strategy'] = (s['Regime']).shift(1)*s['LogRet']
s['Strategy'] = s['Strategy'].fillna(0)
#Ones
endgains = 1
endreturns = 1
#Performance metric
sharpe = (s['Strategy'].mean()-abs(s['LogRet'].mean()))/s['Strategy'].std()
#Compound returns
for g in s['LogRet']:
    slate = endreturns * (1+-g)
    endreturns = slate
for h in s['Strategy']:
    otherslate = endgains * (1+h)
    endgains = otherslate
#Graphical display
#For increased accuracy, remove first window values from TheAdvice
s[['LogRet', 'Strategy']].cumsum().apply(np.exp).plot(grid = True,
                                             figsize = (8,5))
#Display results
print(s)
print(sharpe)
print(endreturns)
print(endgains)

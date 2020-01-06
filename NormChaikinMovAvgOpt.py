# -*- coding: utf-8 -*-
"""
Created on Mon Apr  3 14:39:55 2017

@author: AmatVictoriaCuramIII
"""

import numpy as np
from pandas_datareader import data
import random as rand
import pandas as pd
import time as t
empty = [] #reusable list
#set up desired number of datasets for different period analysis
dataset = pd.DataFrame()
ticker = '^GSPC'
iterations = range(0,2500)
counter = 0
s = data.DataReader(ticker, 'yahoo', start='07/01/2013', end='12/01/2016') 
s['LogRet'] = np.log(s['Adj Close']/s['Adj Close'].shift(1)) 
s['LogRet'] = s['LogRet'].fillna(0)
s['CLV'] = (((s['Adj Close'] - s['Low']) - (s['High'] - s['Adj Close']))
                    / (s['High'] - s['Low']))

Length = len(s['LogRet'])
Range = range(0,Length)
ADI = []
index = s.index
store = 0
for i in Range:
        store = store + (s['Volume'][i] * s['CLV'][i])
        ADI.append(store)
ADISeries = pd.Series(ADI, index=index)
s['ADI'] = ADISeries
start = t.time()
for x in iterations:
    counter = counter + 1    
    aa = rand.randint(1,30)
    bb = rand.randint(2,60)
    if aa > bb:
        continue
    c = rand.randint(2,60)
    d = rand.randint(2,60)
    e = 2 - rand.random() * 4
    f = 2 - rand.random() * 4
    g = 2 - rand.random() * 4
    h = 2 - rand.random() * 4
    a = aa #number of days for moving average window
    b = bb #numer of days for moving average window
    multiplierA = (2/(a+1))
    multiplierB = (2/(b+1))
    EMAyesterdayA = s['ADI'][0] #these prices are based off the SMA values
    EMAyesterdayB = s['ADI'][0] #these prices are based off the SMA values
    smallEMA = [EMAyesterdayA]
    for i in Range:
        holder = (s['ADI'][i]*multiplierA) + (EMAyesterdayA *
                                            (1-multiplierA))
        smallEMA.append(holder)
        EMAyesterdayA = holder
    smallEMAseries = pd.Series(smallEMA[1:], index=s.index)    
    largeEMA = [EMAyesterdayB]
    for i in Range:
        holder1 = (s['ADI'][i]*multiplierB) + (EMAyesterdayB *
                                            (1-multiplierB))
        largeEMA.append(holder1)
        EMAyesterdayB = holder1
    largeEMAseries = pd.Series(largeEMA[1:], index=s.index)
    s['ADIEMAsmall'] = smallEMAseries
    s['ADIEMAlarge'] = largeEMAseries
    volumewindow = c
    s['AverageRollingVolume'] = s['Volume'].rolling(center=False,
                                window=volumewindow).mean()
    s['Chaikin'] = s['ADIEMAsmall'] - s['ADIEMAlarge']
    s['NormChaikin'] = s['Chaikin']/s['AverageRollingVolume']
    s['NormChaikinMovAvg'] = s['NormChaikin'].rolling(window=d,center=False).mean()
    s['MovAvgDivergence'] = s['NormChaikin'] - s['NormChaikinMovAvg']
    s['Touch'] = np.where(s['NormChaikin'] < e, 1,0) #long signal
    s['Touch'] = np.where(s['NormChaikin'] > f, -1, s['Touch']) #short signal
    s['Sustain'] = np.where(s['Touch'].shift(1) == 1, 1, 0) # never actually true when optimized
    s['Sustain'] = np.where(s['Sustain'].shift(1) == 1, 1, 
                                   s['Sustain']) 
    s['Sustain'] = np.where(s['Touch'].shift(1) == -1, -1, 0) #true when previous day touch is -1, and current RSI is > line 37 threshold 
    s['Sustain'] = np.where(s['Sustain'].shift(1) == -1, -1,
                                 s['Sustain']) 
    s['Sustain'] = np.where(s['NormChaikin'] > g, 0, s['Sustain']) #if RSI is greater than threshold, sustain is forced to 0
    s['Sustain'] = np.where(s['NormChaikin'] < h, 0, s['Sustain']) #never actually true when optimized
    s['Regime'] = s['Touch'] + s['Sustain']
    s['Strategy'] = (s['Regime']).shift(1)*s['LogRet']
    s['Strategy'] = s['Strategy'].fillna(0)
    if s['Strategy'].std() == 0:
        continue
    sharpe = (s['Strategy'].mean()-s['LogRet'].mean())/s['Strategy'].std()
    if sharpe < 0.001:
        continue
    print(counter)
    empty.append(a)
    empty.append(b)
    empty.append(c)
    empty.append(d)
    empty.append(e)
    empty.append(f)
    empty.append(g)
    empty.append(h)
    empty.append(sharpe)
    emptyseries = pd.Series(empty)
    dataset[x] = emptyseries.values
    empty[:] = []      
end = t.time()
z1 = dataset.iloc[8]
w1 = np.percentile(z1, 80)
v1 = [] #this variable stores the Nth percentile of top performers
DS1W = pd.DataFrame() #this variable stores your financial advisors for specific dataset
for z in z1:
    if z > w1:
      v1.append(z)
for j in v1:
      r = dataset.columns[(dataset == j).iloc[8]]    
      DS1W = pd.concat([DS1W,dataset[r]], axis = 1)
y = max(z1)
k = dataset.columns[(dataset == y).iloc[8]] #this is the column number
print(dataset[k]) #this is the dataframe index based on column number

print('Time = ',end-start)
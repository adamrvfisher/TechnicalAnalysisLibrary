# -*- coding: utf-8 -*-
"""
Spyder Editor
"""

#This is a summary statistic/technical analysis tool
#pandas_datareader is deprecated, use YahooGrabber

from pandas_datareader import data
import pandas as pd
import numpy as np
ticker1 = '^RUT'
ticker2 = '^GSPC'
window = 20
s1 = data.DataReader(ticker1, 'yahoo', start='10/1/2015', end='01/01/2050')
s2 = data.DataReader(ticker2, 'yahoo', start='10/1/2015', end='01/01/2050')
s1['LogRet'] = np.log(s1['Adj Close']/s1['Adj Close'].shift(1))
s2['LogRet'] = np.log(s2['Adj Close']/s2['Adj Close'].shift(1))
s3 = pd.DataFrame()
#s3['Correlation'] = pd.rolling_corr(s1['LogRet'],s2['LogRet'], window)
s3['Correlation'] = pd.rolling_corr(s1['Adj Close'],s2['Adj Close'], window)
s3 = s3[window:]
s3['Correlation'].plot(grid = True, figsize = (8,3))

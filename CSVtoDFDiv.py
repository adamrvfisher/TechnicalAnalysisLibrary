# -*- coding: utf-8 -*-
"""
Created on Sun May 21 11:47:12 2017

@author: AmatVictoriaCuramIII
"""
from pandas import read_csv
import pandas as pd
import os

#This file does not yet recognize files with 'Stockdiv.csv' titles
#Be aware of assignment
CSVfiles = os.listdir('F:\\Users\\AmatVictoriaCuram\\TemporaryDiv')
ranger = range(0,len(CSVfiles))
for i in ranger:
    try:
        temp = read_csv('F:\\Users\\AmatVictoriaCuram\\TemporaryDiv\\' +
                         (CSVfiles[i]), sep = ',')
        temp = temp.set_index('Date')
        temp.index = pd.to_datetime(temp.index, format = "%Y/%m/%d") 
        temp = temp.loc[:,~temp.columns.duplicated()]
        temp = temp[~temp.index.duplicated(keep='first')]
        if not os.path.exists('F:\\Users\\AmatVictoriaCuram\\Database\\' +
                          CSVfiles[i][:-7]):
            os.makedirs('F:\\Users\\AmatVictoriaCuram\\Database\\' +
                          CSVfiles[i][:-7])
        pd.to_pickle(temp, 'F:\\Users\\AmatVictoriaCuram\\Database\\' +
                          CSVfiles[i][:-7] + '\\' + CSVfiles[i][:-4])
    except OSError:
        continue
for i in ranger:
    try:
        glaze = pd.read_pickle('F:\\Users\\AmatVictoriaCuram\\Database\\' +
                         (CSVfiles[i][:-4]))
        for x in glaze.columns:
            glaze[x] =  pd.to_numeric(glaze[x], errors='coerce')
        pd.to_pickle(glaze, 'F:\\Users\\AmatVictoriaCuram\\Database\\' +
                          CSVfiles[i][:-4])
    except OSError:
        continue
#this is for testing individual CSVs
#tester = read_csv('F:\\Users\\AmatVictoriaCuram\\TemporaryCSV\\' +
#                     (df['CSVname'][0]), sep = ',')
#tester = tester.set_index('Date')
#pd.to_pickle(tester, 'F:\\Users\\AmatVictoriaCuram\\Database\\' + df['CSVname'][0][:-4])
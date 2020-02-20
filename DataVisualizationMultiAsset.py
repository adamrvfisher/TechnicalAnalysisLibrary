# -*- coding: utf-8 -*-
"""

@author: Adam Reinhold Von Fisher - https://www.linkedin.com/in/adamrvfisher/

"""

#Developed in Python 3.5 
#R Multiple Finder; Trade Data Tracking

#Import libraries
import numpy as np
import pandas as pd
import warnings 
from YahooGrabber import YahooGrabber
from pandas.parser import CParserError
import matplotlib.pyplot as plt
from matplotlib.finance import candlestick_ohlc
import matplotlib.dates as mdates

#Don't display warnings
warnings.filterwarnings("ignore",category = RuntimeWarning) 
pd.options.mode.chained_assignment = None 

#Input ticker list
tickerlist = ['GLD', 'SLV', 'TMF', 'TQQQ', 'UVXY']

#For all tickers in list
for ticker in tickerlist[:]:
    print('-' * 55)
    #Request data
    while True: 
        try:
            #Get data
            Asset1 = YahooGrabber(ticker)
        except CParserError:
            continue
        break

    #Declaration/Assignments  
    #Empty list
    Empty = []
    #Empty dataframe
    Trades = pd.DataFrame()
    #Define starting equity
    Equity = 100000
    #Risk for first trade
    RiskPerTrade = Equity * .005 
    #Constraints in percentages, still unimplemented
    Commission = .005
    Slippage = .005
    
    #Time series trimmer for in/out sample data
    Asset1 = Asset1[-2500:] #In
    
    #Variable windows / params
    
    #donchianwidow is used to find the min/max of the price range to make the long/short signal
    #Smaller donchain window = more likely double days
    donchianwindow = 55
    #ATRwindow is used for volatility position sizing
    ATRwindow = 20
    #stopwindow is used for trailing high/low used for long/short exits
    stopwindow = 13
    #Counter tracks iteration progress
    Counter = 0
    
    #SubIndex column is a secondary index, it only exists to help identify exits
    Asset1['SubIndex'] = range(0,len(Asset1))
    
    #Log Returns
    Asset1['LogRet'] = np.log(Asset1['Adj Close']/Asset1['Adj Close'].shift(1))
    Asset1['LogRet'] = Asset1['LogRet'].fillna(0)
    
    #ATR calculation using ATRwindow
    Asset1['Method1'] = Asset1['High'] - Asset1['Low']
    Asset1['Method2'] = abs((Asset1['High'] - Asset1['Close'].shift(1)))
    Asset1['Method3'] = abs((Asset1['Low'] - Asset1['Close'].shift(1)))
    Asset1['Method1'] = Asset1['Method1'].fillna(0)
    Asset1['Method2'] = Asset1['Method2'].fillna(0)
    Asset1['Method3'] = Asset1['Method3'].fillna(0)
    Asset1['TrueRange'] = Asset1[['Method1','Method2','Method3']].max(axis = 1)
    #ATR in points; not %
    Asset1['ATR'] = Asset1['TrueRange'].rolling(window = ATRwindow,
                                    center=False).mean()
    Asset1['ATRPercent'] = Asset1['ATR'] / Asset1['Close']
    Asset1['ATRRollingMax'] = Asset1['ATR'].rolling(ATRwindow).max()
    Asset1['ATRRollingMin'] = Asset1['ATR'].rolling(ATRwindow).min()
    Asset1['ATRPercentRollingMax'] = Asset1['ATRPercent'].rolling(ATRwindow).max()
    Asset1['ATRPercentRollingMin'] = Asset1['ATRPercent'].rolling(ATRwindow).min()
    #Efficiency calculation
    Asset1['4wkCloseDiff'] = Asset1['Adj Close'] - Asset1['Adj Close'].shift(20)
    Asset1['4wkEfficiency'] = Asset1['4wkCloseDiff'] / Asset1['ATR']
                                    
    #Market top and bottom calculation
    Asset1['RollingMax'] = Asset1['High'].rolling(window=donchianwindow, center=False).max()
    Asset1['RollingMin'] = Asset1['Low'].rolling(window=donchianwindow, center=False).min()
    
    #SMA
    Asset1['SMA5'] = Asset1['Close'].rolling(5).mean()
    Asset1['SMA20'] = Asset1['Close'].rolling(20).mean()
    
    #Signal = Price </> min/max
    #if price is greater than the max go long
    Asset1['LongSignal'] = np.where(Asset1['High'] >= Asset1['RollingMax'].shift(1), 1, 0)
    #if price is less than the min go short
    Asset1['ShortSignal'] = np.where(Asset1['Low'] <= Asset1['RollingMin'].shift(1), 1, 0)
    
    #Add filter
    Asset1['Filter'] = np.where(Asset1['4wkEfficiency'] >= 4, 1, -1)
    Asset1['LongSignal'].loc[(Asset1['LongSignal'] == 1) & (Asset1['Filter'] == -1)] = 0
    Asset1['ShortSignal'].loc[(Asset1['ShortSignal'] == 1) & (Asset1['Filter'] == 1)] = 0
    
    #If double signal days exist, then entry and P/L on those days will not be reflected correctly, spurious return stream
    Asset1['DoubleDay'] = np.where(Asset1['LongSignal'] + Asset1['ShortSignal'] == 2, 1, 0)
    
    #Next two lines combines long signal and short signal columns into a single column
    #If there is a double day then a short entry is recorded
    Asset1['Signal'] = np.where(Asset1['LongSignal'] == 1, 1, 0)
    Asset1['Signal'] = np.where(Asset1['ShortSignal'] == 1, -1, Asset1['Signal'])
    
    #if Rolling Min/Max is still being computed, stay out of market
    Asset1['Signal'] = np.where(Asset1['RollingMax'] == np.nan, 0, Asset1['Signal'])
    
    #Index values for segmenting data for trade analysis
    SignalDates = list(Asset1['Signal'].loc[(Asset1['Signal'] != 0)].index)
    
    #Trade ATR on signal day
    Asset1['TradeATR'] = np.where(Asset1['Signal'] != 0, Asset1['ATR'].shift(1), np.nan)
    
    #Exits other than initial n-ATR stop, n-day stopwindow is used here
    Asset1['ShortExitPrice'] =  Asset1['High'].rolling(window=stopwindow, center=False).max()
    Asset1['LongExitPrice'] =  Asset1['Low'].rolling(window=stopwindow, center=False).min()
    
    #Declare columns to record entry price and initial n-ATR stop for unit one
    Asset1['EntryPriceUnitOne'] = np.nan
    Asset1['StopPriceUnitOne'] = np.nan
    
    #Be sure to check for double signal days, gaps on first unit entry, and gaps on exits.
    
    #Default stops and entries 
    #Find the first trade of the signal period to document entry prices
    #Long entry first unit // enter one cent above previous high
    Asset1['EntryPriceUnitOne'] = np.where(Asset1['Signal'] == 1, 
                                  Asset1['RollingMax'].shift(1) + .01, np.nan)
    #Short entry first unit // enter one cent below previous low
    Asset1['EntryPriceUnitOne'] = np.where(Asset1['Signal'] == -1, 
                  Asset1['RollingMin'].shift(1) - .01, Asset1['EntryPriceUnitOne'])
    
    #Long gap entry first unit
    #Find all days that gap above entry on open
    LongGapEntryIndexList = list(Asset1['EntryPriceUnitOne'].loc[(Asset1['Signal'] == 1) & (
                Asset1['Open'] > Asset1['EntryPriceUnitOne'])].index)
    #For all LongGapEntries use open price on gap instead of one cent offset breakout price
    for l in LongGapEntryIndexList:
        Asset1.set_value(l, 'EntryPriceUnitOne', Asset1.loc[l]['Open'])
        
    #Short gap entry first unit
    #Find all days that gap below entry on open 
    ShortGapEntryIndexList = list(Asset1['EntryPriceUnitOne'].loc[(Asset1['Signal'] == -1) & (
                Asset1['Open'] < Asset1['EntryPriceUnitOne'])].index)
    #For all ShortGapEntries use open price on gap instead of one cent offset breakout price
    for s in ShortGapEntryIndexList:
        Asset1.set_value(s, 'EntryPriceUnitOne', Asset1.loc[s]['Open'])
    
    #Entry prices are defined, calculate stop based on direction and entry price
    
    #Fixed long stop first unit - 2 ATR
    Asset1['StopPriceUnitOne'] = np.where(Asset1['Signal'] == 1, 
                    Asset1['EntryPriceUnitOne'] - (Asset1['TradeATR'] * 2), np.nan)
    #Fixed short stop first unit - 2 ATR
    Asset1['StopPriceUnitOne'] = np.where(Asset1['Signal'] == -1, 
                  Asset1['EntryPriceUnitOne'] + (Asset1['TradeATR'] * 2), Asset1['StopPriceUnitOne'])
                  
    #Experimental exits - combine fixed n-ATR stop with trailing max high/min low  
    #Once in a long trade, when the n-day low becomes higher than the initial n-ATR stop, that is the new stop, otherwise, initial n-ATR stop
    Asset1['HybridLongExitPrice'] = np.where(Asset1['LongExitPrice'] > Asset1['StopPriceUnitOne'], 
                              Asset1['LongExitPrice'], Asset1['StopPriceUnitOne'])
    Asset1['HybridLongExitPrice'] = Asset1['HybridLongExitPrice'].ffill()
    #In a short trade, when a n-day high becomes lower than the initial n-ATR stop, that is the new stop, otherwise, initial n-ATR stop
    Asset1['HybridShortExitPrice'] = np.where(Asset1['ShortExitPrice'] < Asset1['StopPriceUnitOne'],
                              Asset1['ShortExitPrice'], Asset1['StopPriceUnitOne'])  
    Asset1['HybridShortExitPrice'] = Asset1['HybridShortExitPrice'].ffill()
    
    #On the first signal we record entry, record  exit, record trade details, and then
    #trim the time series to the next signal after exit. This process repeats.    
    #TradeSubset is a copy of Asset1 from the date of the signal to the end of the time series
    TradeSubset = Asset1.loc[(Asset1.index >= SignalDates[0])] 
    
    #Every closed trade is in the while loop. If a position exists that is still open
    #at the end of the testing period, it is taken care of outside the while loop
    
    #while Counter < 15: #Use this instead of the while loop to go a certain number of trades into the iteration
    
    #while there is still a signal in the time series
    while sum(abs(TradeSubset['Signal'])) != 0:
        #This is the ATR on the day before signal day
        TradeATR = TradeSubset['ATR'][0]
        #Volatility position sizing based on nominal risk and market volatility 
        numshares = (RiskPerTrade)/((TradeATR * 2))
        #1 = long; -1 = short
        TradeDirection = TradeSubset['Signal'][0]
        #This column holds the type of exit that was taken
        TradeSubset['Exit'] = 0
        #Short exit, 1 = yes, 0 = no
        TradeSubset['ShortExit'] = 0
        #Long exit, 1 = yes, 0 = no
        TradeSubset['LongExit'] = 0
        #Did the exit gap overnight? 1 = yes, 0 = no 
        TradeSubset['GapShortExit'] = 0
        #Did the exit gap overnight? 1 = yes, 0 = no
        TradeSubset['GapLongExit'] = 0
        
        #If in a long trade:
        if TradeDirection == 1:
            #Change the value of TradeSubset['LongExit'] to 1 on the days that there is a long exit signal
            #Find days for long exits
            LongExitIndexList = list(TradeSubset['LongExit'].loc[(TradeSubset['Low'] < TradeSubset['HybridLongExitPrice'])].index)
            #Set values for long exits
            for l in LongExitIndexList:
                TradeSubset.set_value(l, 'LongExit', 1)
        if TradeDirection == -1:        
            #Change the value of TradeSubset['ShortExit'] to 1 on the days that there is a short exit signal
            #Find days for short exits
            ShortExitIndexList = list(TradeSubset['ShortExit'].loc[(TradeSubset['High'] > TradeSubset['HybridShortExitPrice'])].index)
            #Set values for short exits
            for s in ShortExitIndexList:
                TradeSubset.set_value(s, 'ShortExit', 1)
        
        #Assess Gaps on days where open long trade closes
        if TradeDirection == 1:
            #Change the value of TradeSubset['GapLongExit'] to 1 on the days that there is a long exit signal
            #Find days for gap long exits
            GapLongExitIndexList = list(TradeSubset['GapLongExit'].loc[(TradeSubset['LongExit'] == 1) & (
                     TradeSubset['Open'] < TradeSubset['HybridLongExitPrice'])].index)
            #Set values for gap long exits
            for l in GapLongExitIndexList:
                TradeSubset.set_value(l, 'GapLongExit', 1)
                     
        if TradeDirection == -1:             
            #Change the value of TradeSubset['GapShortExit'] to 1 on the days that there is a short exit signal
            #Find days for gap short exits
            GapShortExitIndexList = list(TradeSubset['GapShortExit'].loc[(TradeSubset['ShortExit'] == 1) & (
                    TradeSubset['Open'] > TradeSubset['HybridShortExitPrice'])].index)
            #Set values for gap short exits
            for s in GapShortExitIndexList:
                TradeSubset.set_value(s, 'GapShortExit', 1)
                
        #Set TradeSubset['Exit'] column to the specific exit recorded
        TradeSubset['Exit'].loc[(TradeSubset['ShortExit'] == 1)] = 1 #1 indicating short exit
        TradeSubset['Exit'].loc[(TradeSubset['LongExit'] == 1)] = 2 #1 indicating long exit 
        TradeSubset['Exit'].loc[(TradeSubset['GapShortExit'] == 1)] = 3 #1 indicating short exit w/ gap
        TradeSubset['Exit'].loc[(TradeSubset['GapLongExit'] == 1)] = 4 #1 indicating long exit w/ gap
     
    #Above is 'df.set_value()' way of assignment 
    #Compare that to the df[].loc[()] = way of assignment above. Which is best?
       
        #List comprehension to find exit taken for subset.
        #The next function gives a position on the TradeSubset index
        ExitTaken = TradeSubset['Exit'][next((n for n, x in enumerate(TradeSubset['Exit']) if x), 0)]
        if ExitTaken == 0:
            break
        
        #The length of the trade
        LengthOfTrade = int(next((n for n, x in enumerate(TradeSubset['Exit']) if x), 0))
        #Index on date of entry
        IndexOfEntry = TradeSubset.index[0]
        #Index on date of exit
        IndexOfExit = TradeSubset.index[next((n for n, x in enumerate(TradeSubset['Exit']) if x), 0)]
        #The SubIndex of the exit date is for continuing looking for rentry in new trade subset 
        SubIndexOfExit = TradeSubset['SubIndex'][next((n for n, x in enumerate(TradeSubset['Exit']) if x), 0)]
        #Entry price on signal day
        EntryPriceUnitOne = TradeSubset['EntryPriceUnitOne'][0]
        
        #Calculate long exit price based on mixed exit - TradeSubset['HybridLongExitPrice']
        if TradeDirection == 1:
            StopPriceUnitOne = TradeSubset['HybridLongExitPrice'][next((n for n, x in enumerate(TradeSubset['Exit']) if x), 0)]
        #Calculate long exit price based on mixed exit - TradeSubset['HybridLongExitPrice']
        elif TradeDirection == -1:
            StopPriceUnitOne = TradeSubset['HybridShortExitPrice'][next((n for n, x in enumerate(TradeSubset['Exit']) if x), 0)]
    
        #Below is referenced for execution on gap days
        OpenPriceOnGap = TradeSubset['Open'][LengthOfTrade]
    
        #Calculate dollar and percent return on exit days based on exit taken
        #This is an appropriate place to add slippage and commission
        if ExitTaken == 1: # if exiting short trade, exit during market day
            TradePercentReturn = (EntryPriceUnitOne - StopPriceUnitOne)/EntryPriceUnitOne
            TradeDollarReturn = (EntryPriceUnitOne - StopPriceUnitOne) * numshares
        elif ExitTaken == 2: # if exiting long trade, exitduring market day 
            TradePercentReturn = (StopPriceUnitOne - EntryPriceUnitOne)/EntryPriceUnitOne
            TradeDollarReturn = (StopPriceUnitOne - EntryPriceUnitOne) * numshares
        elif ExitTaken == 3: # if exiting short trade with gap, use open price to calculate return
            TradePercentReturn = (EntryPriceUnitOne - OpenPriceOnGap)/EntryPriceUnitOne
            TradeDollarReturn = (EntryPriceUnitOne - OpenPriceOnGap) * numshares
        elif ExitTaken == 4: # if exiting long trade with gap, use open price to calculate return 
            TradePercentReturn = (OpenPriceOnGap - EntryPriceUnitOne)/EntryPriceUnitOne
            TradeDollarReturn = (OpenPriceOnGap - EntryPriceUnitOne) * numshares
    
        #R Multiple calculation, return based on initial risk
        RMultiple = TradeDollarReturn / RiskPerTrade
    
        #Log individual trade details in the Trade dataframe
        Empty.append(ExitTaken)
        Empty.append(numshares)
        Empty.append(LengthOfTrade)
        Empty.append(EntryPriceUnitOne)
        Empty.append(StopPriceUnitOne)
        Empty.append(IndexOfEntry)
        Empty.append(IndexOfExit)
        Empty.append(TradeDirection)
        Empty.append(OpenPriceOnGap)
        Empty.append(TradePercentReturn)
        Empty.append(TradeDollarReturn)
        Empty.append(RMultiple)
        Empty.append(SubIndexOfExit)
        Empty.append(TradeATR)
        Empty.append(RiskPerTrade)
    
        #List to series
        Emptyseries = pd.Series(Empty)
        #Append series to Trades dataframe to log details
        Trades[Counter] = Emptyseries.values
    
        #Empty the list for next trade
        Empty[:] = [] 
    
        #Confirm trade number
#        print(Counter) 
        #Keeping track of iteration progress
        Counter = Counter + 1
    
        #Recalculate equity and risk for next trade
        Equity = Equity + TradeDollarReturn
        RiskPerTrade = Equity * .005
    
        #This trimmer trims the above Trade out of the TradeSubset, then trims to the next signal day!
        TradeSubset = TradeSubset[(LengthOfTrade + 1):]
        SignalTrim = next((n for n, x in enumerate(TradeSubset['Signal']) if x), 0)
        TradeSubset = TradeSubset[SignalTrim:]
    
    #If there is a trade that is still open
    if sum(abs(TradeSubset['Signal'])) != 0:
        #This exit type corresponds to an open trade 
        ExitTaken = 0
        #ATR on signal day
        TradeATR = TradeSubset['ATR'][0]
        #RiskPerTrade is already calculated from last iteration of while loop above
        #Volatility position sizing
        numshares = (RiskPerTrade)/((TradeATR) * 2)
        #Duration of trade being open
        LengthOfTrade = len(TradeSubset)
        #Initial entry price
        EntryPriceUnitOne = TradeSubset['EntryPriceUnitOne'][0]
    
        #Referencing stop price based on trade direction
        #Long trade
        if TradeDirection == 1:
            StopPriceUnitOne = TradeSubset['HybridLongExitPrice'][next((n for n, x in enumerate(TradeSubset['Exit']) if x), 0)]
        #Short trade
        elif TradeDirection == -1:
            StopPriceUnitOne = TradeSubset['HybridShortExitPrice'][next((n for n, x in enumerate(TradeSubset['Exit']) if x), 0)]
    
        #Index on the day of entry
        IndexOfEntry = TradeSubset.index[0]
        #Index on the day of exit    
        IndexOfExit = TradeSubset.index[-1]
        #Subindex on day of exit, used to populate return stream
        SubIndexOfExit = TradeSubset['SubIndex'][-1]
        #Direction of the trade long/short
        TradeDirection = TradeSubset['Signal'][0]
        #We cannot have open price gap since the trade is still open
        OpenPriceOnGap = np.nan
        
        #If long trade, then  make percent and dollar return calculation
        if TradeDirection == 1:
            TradePercentReturn = (TradeSubset['Adj Close'][-1] - EntryPriceUnitOne)/EntryPriceUnitOne
            TradeDollarReturn = (TradeSubset['Adj Close'][-1] - EntryPriceUnitOne) * numshares
        #If short trade, then  make percent and dollar return calculation
        elif TradeDirection == -1:
            TradePercentReturn = (EntryPriceUnitOne - TradeSubset['Adj Close'][-1])/EntryPriceUnitOne
            TradeDollarReturn = (EntryPriceUnitOne - TradeSubset['Adj Close'][-1]) * numshares
    
        #Based on latest close price even though trade is still open
        RMultiple = TradeDollarReturn / RiskPerTrade
        #Readjust equity for dollar returns on latest trade
        Equity = Equity + TradeDollarReturn
    
        #Log Trade details in Trade dataframe
        Empty.append(ExitTaken)
        Empty.append(numshares)
        Empty.append(LengthOfTrade)
        Empty.append(EntryPriceUnitOne)
        Empty.append(StopPriceUnitOne)
        Empty.append(IndexOfEntry)
        Empty.append(IndexOfExit)
        Empty.append(TradeDirection)
        Empty.append(OpenPriceOnGap)
        Empty.append(TradePercentReturn)
        Empty.append(TradeDollarReturn)
        Empty.append(RMultiple)
        Empty.append(SubIndexOfExit)
        Empty.append(TradeATR)
        Empty.append(RiskPerTrade)
    
        #Turn list into series    
        Emptyseries = pd.Series(Empty)
        #Add all trade details to Trades DataFrame
        Trades[Counter] = Emptyseries.values
        #Clear the list for next iteration
        Empty[:] = [] 
    
        #Iteration tracking
        Counter = Counter + 1
#        print(Counter)
    
    #Adjust row names for Trades DataFrame
    Trades = Trades.rename(index={0: "ExitTaken", 1: "NumberOfShares", 2: "LengthOfTrade",
        3: "EntryPriceUnitOne", 4: "StopPriceUnitOne", 5: "IndexOfEntry", 6: "IndexOfExit",
        7: "TradeDirection", 8: "OpenPriceOnGap", 9: "TradePercentReturn",
        10: "TradeDollarReturn", 11: "RMultiple", 12:"SubIndexOfExit", 
        13:"TradeATR", 14:"RiskPerTrade"})
    
    Asset1['StrategyPercentReturns'] = 1   
    Asset1['StrategyDollarReturns'] = 0   
    
    #The next two lines are the only reason keep track of 'SubIndexOfExit'
    #This is where I apply the returns on the trade close date to get the trade by trade return stream
    for d in Trades:
        Asset1['StrategyPercentReturns'].loc[(Asset1['SubIndex'] == Trades[d]['SubIndexOfExit'])] = 1 + Trades[d]['TradePercentReturn']
        Asset1['StrategyDollarReturns'].loc[(Asset1['SubIndex'] == Trades[d]['SubIndexOfExit'])] = 1 + Trades[d]['TradeDollarReturn']
    
    #System statistics    
    #Number Win/Loss
    NumWinningTrades = len(Asset1['StrategyPercentReturns'][Asset1['StrategyPercentReturns'] > 1])
    NumLosingTrades = len(Asset1['StrategyPercentReturns'][Asset1['StrategyPercentReturns'] < 1])
    #Size of AvgWin/AvgLoss
    AvgWin = Asset1['StrategyPercentReturns'][Asset1['StrategyPercentReturns'] > 1].mean()
    AvgLoss = Asset1['StrategyPercentReturns'][Asset1['StrategyPercentReturns'] < 1].mean()
    #AvgWin Over AvgLoss
    RewardRisk = AvgWin/AvgLoss
    #Win and Loss rate
    WinRate = NumWinningTrades / (NumWinningTrades + NumLosingTrades)
    LossRate = NumLosingTrades / (NumWinningTrades + NumLosingTrades)
    #Expectancy Calculation
    Expectancy = (WinRate * RewardRisk) - (LossRate)
    
    #Make a DataFrame that stores just R multiples from the Trades DataFrame
    RMultiples = pd.DataFrame(data = Trades.loc['RMultiple',:])
    
    
    #Return stream modification for graphing
    Asset1['Multiplier'] = Asset1['StrategyPercentReturns'].cumprod()
    Asset1['DollarPL'] = Asset1['StrategyDollarReturns'].cumsum()
    
    #See if there are any double days that would call for spurious return stream
#    print(sum(Asset1['DoubleDay']), ' Double signal days exist')
    print('The expectancy of the system is ', Expectancy)
#    print(RMultiples)
    
    #This is a graph of the equity curve from trade exits
    fig, ax = plt.subplots()
    #Line chart of dollar P/L
    ax.plot(Asset1['DollarPL'])
    #Set title and axis labels
    ax.set_title('Dollar P/L')
    ax.set_xlabel('Date')
    ax.set_ylabel('Profit/Loss')
    
    plt.show()    
    print('-' * 55)
    
    #This is a histogram for RMultiples
    fig2, ax2 = plt.subplots()
    #Separate RMultiples for histogram
    PositiveRMultiples = np.array(RMultiples['RMultiple'][RMultiples['RMultiple'] > 0.001])
    NegativeRMultiples = np.array(RMultiples['RMultiple'][RMultiples['RMultiple'] < -0.001])
    SeparatedRMultiples = [PositiveRMultiples, NegativeRMultiples]
    
    #Make histogram - use odd number of bins so bars don't overlap
    plt.hist(SeparatedRMultiples, bins = 21, color = ['green', 'red'], 
             label=['Positive R', 'Negative R'])         
    #Place legend on graph
    plt.legend(loc='upper right')
    #Set title and axis labels
    ax2.set_title('R Multiples')
    ax2.set_xlabel('R Multiple')
    ax2.set_ylabel('Number of Trades')
    
    plt.show()
    print('-' * 60)

    #Make column that represents X axis 
    Asset1['Index'] = Asset1.index
    #Format for mpl
    Asset1['IndexToNumber'] = Asset1['Index'].apply(mdates.date2num)
    
    #Create graph for candlestick chart and define X and Y axis scale
    figure, axe = plt.subplots(figsize = (10,5))
    #Assign titles and axis labels
    axe.set_title(ticker)
    plt.ylabel(ticker + ' Price')
    plt.xlabel('Date') 
    
    #Overlay
    axe.plot(Asset1['IndexToNumber'], Asset1['RollingMax'], color = 'green', label = 'RollingMax')
    axe.plot(Asset1['IndexToNumber'], Asset1['RollingMin'], color = 'red', label = 'RollingMin')
    axe.plot(Asset1['IndexToNumber'], Asset1['SMA5'], color = 'black', label = 'SMA5')
    axe.plot(Asset1['IndexToNumber'], Asset1['SMA20'], color = 'yellow', label = 'SMA20')
    
    #Signal triangles..
    EntryScatterData = pd.DataFrame()
    EntryScatterData['TradeDates'] = Trades.iloc[5]
    EntryScatterData['IndexToNumber'] = EntryScatterData['TradeDates'].apply(mdates.date2num)
    EntryScatterData['TradeDirection'] = Trades.iloc[7]
    EntryScatterData['EntryPriceUnitOne'] = Trades.iloc[3]
    
    #Entry Triangles
    axe.scatter(EntryScatterData.loc[EntryScatterData['TradeDirection'] == 1, 'IndexToNumber'].values, 
            EntryScatterData.loc[EntryScatterData['TradeDirection'] == 1, 'EntryPriceUnitOne'].values, label='skitscat', color='green', s=75, marker="^")
    axe.scatter(EntryScatterData.loc[EntryScatterData['TradeDirection'] == -1, 'IndexToNumber'].values, 
            EntryScatterData.loc[EntryScatterData['TradeDirection'] == -1, 'EntryPriceUnitOne'].values, label='skitscat', color='red', s=75, marker="v")
    
    #Stop X markers
    ExitScatterData = pd.DataFrame()
    ExitScatterData['ExitDates'] = Trades.iloc[6]
    ExitScatterData['IndexToNumber'] = ExitScatterData['ExitDates'].apply(mdates.date2num)
    ExitScatterData['TradeDirection'] = Trades.iloc[7]
    ExitScatterData['ExitPriceUnitOne'] = Trades.iloc[4]
    
    #Exit X
    axe.scatter(ExitScatterData.loc[ExitScatterData['TradeDirection'] == -1, 'IndexToNumber'].values, 
            ExitScatterData.loc[ExitScatterData['TradeDirection'] == -1, 'ExitPriceUnitOne'].values, label='skitscat', color='green', s=75, marker="x")
    axe.scatter(ExitScatterData.loc[ExitScatterData['TradeDirection'] == 1, 'IndexToNumber'].values, 
            ExitScatterData.loc[ExitScatterData['TradeDirection'] == 1, 'ExitPriceUnitOne'].values, label='skitscat', color='red', s=75, marker="x")
    
    #Creating candlestick values as copy from original DataFrame
    Asset1Copy = Asset1[['IndexToNumber', 'Open', 'High', 'Low', 'Close', 'Adj Close']].copy()
    #Plot the DF values with the figure, object
    candlestick_ohlc(axe, Asset1Copy.values, width=.6, colorup='green', colordown='red')
    axe.xaxis.set_major_formatter(mdates.DateFormatter('%Y-%m-%d'))
    
    print('-' * 90)
    plt.show()
    print('-' * 90)
    
    #For ATR indicator
    figure2, axe2 = plt.subplots(figsize = (10,2))
    #Set title and axis labels
    axe2.set_title(ticker + ' ATR')
    plt.ylabel(ticker + ' ATR')
    plt.xlabel('Date')
    #ATR line and ATR channels
    axe2.plot(Asset1['IndexToNumber'], Asset1['ATRPercent'], color = 'black', label = 'ATR Percent')
    axe2.plot(Asset1['IndexToNumber'], Asset1['ATRPercentRollingMax'], color = 'green', label = 'ATRPercentRollingMax')
    axe2.plot(Asset1['IndexToNumber'], Asset1['ATRPercentRollingMin'], color = 'red', label = 'ATRPercentRollingMin')
    #Format date
    axe2.xaxis.set_major_formatter(mdates.DateFormatter('%Y-%m-%d'))
    plt.show()

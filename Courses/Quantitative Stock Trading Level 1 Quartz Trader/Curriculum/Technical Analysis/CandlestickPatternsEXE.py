'''
This program guides user to visualize candlestick pattern occurences in the stock market.
* In practice, candlestick patterns MUST be used with technical indicators to generate trading signals.
'''

# Setting working directory
DIR = 'C:/Users/user/Documents/GitHub/leeykjohn/Aries-Profits/Products/On-Demand Video Courses/Quantitative Stock Trading Level 1 Quartz Trader/Curriculum/Technical Analysis'
import sys
sys.path.insert(0, DIR)

# Import relevant packages
import yfinance as yf
import pandas as pd
import matplotlib.pyplot as plt
from CandlestickPatterns import *

TICKER = 'SPY' # Stock Ticker symbol
START_DATE = '2022-01-01' # Stock data start date
END_DATE = '2022-12-01' # Stock data end date

# Store adjusted stock prices into a variable
stockPx = yf.download(TICKER, START_DATE, END_DATE)

# Configure options to display data frames
pd.set_option('display.max_columns', 1000) # to output 1000 columns max
pd.set_option('display.width', 1000) # adjust console size to display data frames

# Feed price data into CandlestickPatterns function
candleSx = CandlestickPatterns(stockPx)

# Visualizing occurences of Bullish & Bearish Pin Bar Patterns
fig = plt.figure()
ax1 = fig.add_subplot(title = TICKER + ' Daily Prices', ylabel = 'Price in USD ($)')
candleSx.High.plot(ax = ax1) # plot price highs
candleSx.Low.plot(ax = ax1) # plot price lows
ax1.plot(candleSx[candleSx['BullishPinBar'] == 1].index, candleSx[candleSx['BullishPinBar'] == 1].Low, '^', markersize = 8, color = 'g', label = 'Bullish Pin Bar (Buy)')
ax1.plot(candleSx[candleSx['BearishPinBar'] == 1].index, candleSx[candleSx['BearishPinBar'] == 1].High, 'v', markersize = 8, color = 'r', label = 'Bearish Pin Bar (Sell)')
plt.legend(prop={'size': 18})

# Visualizing occurences of Bullish & Bearish Engulfing Patterns
fig = plt.figure()
ax1 = fig.add_subplot(title = TICKER + ' Daily Prices', ylabel = 'Price in USD ($)')
candleSx.High.plot(ax = ax1) # plot price highs
candleSx.Low.plot(ax = ax1) # plot price lows
ax1.plot(candleSx[candleSx['BullishEngulfing'] == 1].index, candleSx[candleSx['BullishEngulfing'] == 1].Low, '^', markersize = 8, color = 'g', label = 'Bullish Engulfing (Buy)')
ax1.plot(candleSx[candleSx['BearishEngulfing'] == 1].index, candleSx[candleSx['BearishEngulfing'] == 1].High, 'v', markersize = 8, color = 'r', label = 'Bearish Engulfing (Sell)')
plt.legend(prop={'size': 18})

# Visualizing occurences of OWS & OBC Patterns
fig = plt.figure()
ax1 = fig.add_subplot(title = TICKER + ' Daily Prices', ylabel = 'Price in USD ($)')
candleSx.High.plot(ax = ax1) # plot price highs
candleSx.Low.plot(ax = ax1) # plot price lows
ax1.plot(candleSx[candleSx['OneWhiteSoldier'] == 1].index, candleSx[candleSx['OneWhiteSoldier'] == 1].Low, '^', markersize = 8, color = 'g', label = 'One White Soldier (Buy)')
ax1.plot(candleSx[candleSx['OneBlackCrow'] == 1].index, candleSx[candleSx['OneBlackCrow'] == 1].High, 'v', markersize = 8, color = 'r', label = 'One Black Crow (Sell)')
plt.legend(prop={'size': 18})

# Visualizing occurences of Morning Star & Evening Star Patterns
fig = plt.figure()
ax1 = fig.add_subplot(title = TICKER + ' Daily Prices', ylabel = 'Price in USD ($)')
candleSx.High.plot(ax = ax1) # plot price highs
candleSx.Low.plot(ax = ax1) # plot price lows
ax1.plot(candleSx[candleSx['MorningStar'] == 1].index, candleSx[candleSx['MorningStar'] == 1].Low, '^', markersize = 8, color = 'g', label = 'Morning Star (Buy)')
ax1.plot(candleSx[candleSx['EveningStar'] == 1].index, candleSx[candleSx['EveningStar'] == 1].High, 'v', markersize = 8, color = 'r', label = 'Evening Star (Sell)')
plt.legend(prop={'size': 18})
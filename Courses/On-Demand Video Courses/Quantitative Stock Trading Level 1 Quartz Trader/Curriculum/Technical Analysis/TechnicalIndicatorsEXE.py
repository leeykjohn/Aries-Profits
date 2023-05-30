'''
This program guides users to visualize stock prices with the technical indicators derived from functions in TechnicalIndicators.py>
* In practice, multiple technical indicators are used as opposed to just one to generate trading signals.
'''

# Setting working directory
DIR = 'C:/Users/user/Documents/GitHub/leeykjohn/Aries-Profits/Products/On-Demand Video Courses/Quantitative Stock Trading Level 1 Quartz Trader/Curriculum/Technical Analysis'
import sys
sys.path.insert(0, DIR)

# Import relevant packages
import yfinance as yf
import pandas as pd
import matplotlib.pyplot as plt
from TechnicalIndicators import *

TICKER = 'SPY' # Stock Ticker symbol
START_DATE = '2017-12-01' # Stock data start date
END_DATE = '2022-12-01' # Stock data end date

# Store adjusted stock prices into a variable
stockPx = yf.download(TICKER, START_DATE, END_DATE)

# Configure options to display data frames
pd.set_option('display.max_columns', 1000) # to output 1000 columns max
pd.set_option('display.width', 1000) # adjust console size to display data frames

# Make a copy of the original price data
technicalSx = stockPx.copy()

#---------------------------------------Simple Moving Average (SMA)---------------------------------------
# Adding SMA columns in the technical indicators table
technicalSx['SMA50'] = SMA(technicalSx, 50)
technicalSx['SMA150'] = SMA(technicalSx, 150)
technicalSx['SMA200'] = SMA(technicalSx, 200)

# Visualizing recent 200-period price trend using 50 SMA, 150 SMA, and 200 SMA
fig = plt.figure()
ax1 = fig.add_subplot(title = TICKER + ' Daily Prices', ylabel = 'Price in USD ($)')
technicalSx['Close'].tail(200).plot(ax=ax1, color='k', lw=2., legend=True)
technicalSx['SMA50'].tail(200).plot(ax=ax1, color='y', lw=2.)
technicalSx['SMA150'].tail(200).plot(ax=ax1, color='g', lw=2.)
technicalSx['SMA200'].tail(200).plot(ax=ax1, color='r', lw=2.)
plt.legend(prop={'size': 18})

#---------------------------------------Exponential Moving Average (EMA)---------------------------------------
# Adding EMA columns in the technical indicators table
technicalSx['EMA20'] = EMA(technicalSx, 20)
technicalSx['EMA40'] = EMA(technicalSx, 40)

# Visualizing recent 200-day price trend using 20 EMA and 40 EMA
fig = plt.figure()
ax1 = fig.add_subplot(title = TICKER + ' Daily Prices', ylabel = 'Price in USD ($)')
technicalSx['Close'].tail(200).plot(ax=ax1, color='k', lw=2., legend=True)
technicalSx['EMA20'].tail(200).plot(ax=ax1, color='magenta', lw=2., linestyle='dotted')
technicalSx['EMA40'].tail(200).plot(ax=ax1, color='cyan', lw=2., linestyle='dotted')
plt.legend(prop={'size': 18})

#---------------------------------------Moving Average Convergence Divergence (MACD)---------------------------------------
# Adding MACD, Signal, and Histogram columns in the technical indicators table
macd_columns = MACD(technicalSx, 12, 26, 9)
technicalSx['MACD'] = macd_columns[0]
technicalSx['MACDSignal'] = macd_columns[1]
technicalSx['MACDHistogram'] = macd_columns[2]

# Visualizing recent 200-day price trend using MACD, MACD Signal, and MACD Histogram
fig = plt.figure()
ax1 = fig.add_subplot(311, title = TICKER + ' Daily Prices', ylabel = 'Price in USD ($)')
technicalSx['Close'].tail(200).plot(ax=ax1, color='k', lw=2., legend=True)
ax2 = fig.add_subplot(312, ylabel='MACD & MACD Signal')
technicalSx['MACD'].tail(200).plot(ax=ax2, color='goldenrod', lw=2., legend=True)
technicalSx['MACDSignal'].tail(200).plot(ax=ax2, color='r', lw=2., legend=True)
ax3 = fig.add_subplot(313, ylabel='MACD - MACD Signal')
technicalSx['MACDHistogram'].tail(200).plot(ax=ax3, color='blue', kind='bar', legend=True, use_index = False)

#---------------------------------------Bollinger Bands (BBANDS)---------------------------------------
# Adding BBANDS columns in the technical indicators table
bbands_columns = BBANDS(technicalSx, 20, 2)
technicalSx['UpperBBAND'] = bbands_columns[0]
technicalSx['MiddleBBAND'] = bbands_columns[1]
technicalSx['LowerBBAND'] = bbands_columns[2]

# Visualizing recent 200-day price with BBANDS
fig = plt.figure()
ax1 = fig.add_subplot(title = TICKER + ' Daily Prices', ylabel = 'Price in USD ($)')
technicalSx['Close'].tail(200).plot(ax=ax1, color='k', lw=2., legend=True)
technicalSx['MiddleBBAND'].tail(200).plot(ax=ax1, color='red', lw=2., linestyle='dashed')
technicalSx['UpperBBAND'].tail(200).plot(ax=ax1, color='grey', lw=2., linestyle='dashed')
technicalSx['LowerBBAND'].tail(200).plot(ax=ax1, color='grey', lw=2., linestyle='dashed')
plt.legend(prop={'size': 18})

#---------------------------------------Force Index---------------------------------------
# Adding Force Index column in the technical indicators table
technicalSx['ForceIndex'] = ForceIndex(technicalSx, 13)

# Visualizing recent 200-day price trend using 13-period Force Index
fig = plt.figure()
ax1 = fig.add_subplot(211, title = TICKER + ' Daily Prices', ylabel = 'Price in USD ($)')
technicalSx['Close'].tail(200).plot(ax=ax1, color='k', lw=2., legend=True)
ax2 = fig.add_subplot(212, ylabel='Force Index (13-day)')
technicalSx['ForceIndex'].tail(200).plot(ax=ax2, color='goldenrod', lw=2., legend=True)
ax2.axhline(y=0, linewidth=2, color='red')

#---------------------------------------Stochastic Oscillator---------------------------------------
# Adding %K and %D column in the technical indicators table
so_columns = StochasticOscillator(technicalSx, 5, 3)
technicalSx['%K'] = so_columns[0]
technicalSx['%D'] = so_columns[1]

# Visualizing recent 200-day price trend using 5-period %K and 3-period %D stochastics
fig = plt.figure()
ax1 = fig.add_subplot(211, title = TICKER + ' Daily Prices', ylabel = 'Price in USD ($)')
technicalSx['Close'].tail(200).plot(ax=ax1, color='k', lw=2., legend=True)
ax2 = fig.add_subplot(212, ylabel='Stochastic Oscillator')
technicalSx['%K'].tail(200).plot(ax=ax2, color='goldenrod', lw=2., legend=True)
technicalSx['%D'].tail(200).plot(ax=ax2, color='red', lw=2., legend=True)
ax2.axhline(y=80, linewidth=2, color='grey', linestyle='dashed')
ax2.axhline(y=20, linewidth=2, color='grey', linestyle='dashed')

#---------------------------------------Williams % R---------------------------------------
# Adding the 10 and 260-period Williams % R column in the technical indicators table
technicalSx['WR10'] = WilliamsR(technicalSx, 10)
technicalSx['WR260'] = WilliamsR(technicalSx, 260)

# Visualizing recent 200-day price trend using 10 and 260-period Williams % R
fig = plt.figure()
ax1 = fig.add_subplot(311, title = TICKER + ' Daily Prices', ylabel = 'Price in USD ($)')
technicalSx['Close'].tail(200).plot(ax=ax1, color='k', lw=2., legend=True)
ax2 = fig.add_subplot(312, ylabel='Williams % R (10-day)')
technicalSx['WR10'].tail(200).plot(ax=ax2, color='goldenrod', lw=2., legend=True)
ax2.axhline(y=-80, linewidth=2, color='grey', linestyle='dashed')
ax2.axhline(y=-20, linewidth=2, color='grey', linestyle='dashed')
ax3 = fig.add_subplot(313, ylabel='Williams % R (260-day)')
technicalSx['WR260'].tail(200).plot(ax=ax3, color='goldenrod', lw=2., legend=True)
ax3.axhline(y=-80, linewidth=2, color='grey', linestyle='dashed')
ax3.axhline(y=-20, linewidth=2, color='grey', linestyle='dashed')

#---------------------------------------Relative Strength Index (RSI)---------------------------------------
# Adding 20-period RSI column in the technical indicators table
technicalSx['RSI20'] = RSI(technicalSx, 20)

# Visualizing recent 200-day price trend using 20-period RSI
fig = plt.figure()
ax1 = fig.add_subplot(211, title = TICKER + ' Daily Prices', ylabel = 'Price in USD ($)')
technicalSx['Close'].tail(200).plot(ax=ax1, color='k', lw=2., legend=True)
ax2 = fig.add_subplot(212, ylabel='RSI (20-day)')
technicalSx['RSI20'].tail(200).plot(ax=ax2, color='goldenrod', lw=2., legend=True)
ax2.axhline(y=70, linewidth=2, color='grey', linestyle='dashed')
ax2.axhline(y=30, linewidth=2, color='grey', linestyle='dashed')
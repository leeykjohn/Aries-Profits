'''
This program guides users to visualize stock prices with the Average True Range measure derived from function in AverageTrueRangeMeasure.py>

'''

# Setting working directory
DIR = 'C:/Users/user/Documents/GitHub/leeykjohn/Aries-Profits/Products/On-Demand Video Courses' \
      '/Quantitative Stock Trading Level 1 Quartz Trader' \
      '/Curriculum' \
      '/Position Sizing'
import sys
sys.path.insert(0, DIR)

# Import relevant packages
import yfinance as yf
import pandas as pd
import matplotlib.pyplot as plt
from AverageTrueRangeMeasure import *

TICKER = 'AXP' # Stock Ticker symbol
START_DATE = '2020-01-20' # Stock data start date
END_DATE = '2023-01-20' # Stock data end date

# Store adjusted stock prices into a variable
stockPx = yf.download(TICKER, START_DATE, END_DATE)

# Configure options to display data frames
pd.set_option('display.max_columns', 1000) # to output 1000 columns max
pd.set_option('display.width', 1000) # adjust console size to display data frames

# Make a copy of the original price data
stockATR = stockPx.copy()

#---------------------------------------Average True Range (ATR)---------------------------------------
# Adding ATR column in the stock data table
stockATR['ATR'] = ATR(stockATR, 14)

# Visualizing recent 90-day price and ATR
fig = plt.figure()
ax1 = fig.add_subplot(211, title = TICKER + ' Daily Prices', ylabel = 'Price in USD ($)')
stockATR['Close'].tail(90).plot(ax=ax1, color='k', lw=2., legend=True)
ax2 = fig.add_subplot(212, ylabel='ATR (14-day)')
stockATR['ATR'].tail(90).plot(ax=ax2, color='goldenrod', lw=2., legend=True)
atr_average90 = (max(stockATR['ATR'].tail(90))+min(stockATR['ATR'].tail(90)))/2
ax2.axhline(y=atr_average90, linewidth=2, color='grey', linestyle='dashed')
ax2.text(stockATR['Close'].index[-1], atr_average90, '{0:.{1}f}'.format(atr_average90, 2), color="grey", ha="center", va="bottom")
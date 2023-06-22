'''
This program guides users to visualize stock prices with the Relative Strength measure derived from function in RelativeStrengthMeasure.py>
'''

# Setting working directory
DIR = 'C:/Users/user/Documents/GitHub/leeykjohn/Aries-Profits/Products/On-Demand Video Courses/Quantitative Stock Trading Level 1 Quartz Trader/Curriculum/Stock Selection'
import sys
sys.path.insert(0, DIR)

# Import relevant packages
import yfinance as yf
import pandas as pd
import matplotlib.pyplot as plt
from RelativeStrengthMeasure import RS, RSSMA

df = pd.read_csv('C:/Users/user/Documents/GitHub/leeykjohn/Aries-Profits/Products/On-Demand Video Courses/Quantitative Stock Trading Level 1 Quartz Trader/Curriculum'
                 '/Stock Selection/20230118StocksToShortFinal.csv')
TICKERS = df['Symbol'].to_list()
BENCHMARK = 'XLY'
START_DATE = '2022-01-18' # Stock data start date
END_DATE = '2023-01-18' # Stock data end date

# Store adjusted stock prices into a variable
stockPx = yf.download(TICKERS + [BENCHMARK], START_DATE, END_DATE)

# Configure options to display data frames
pd.set_option('display.max_columns', 1000) # to output 1000 columns max
pd.set_option('display.width', 1000) # adjust console size to display data frames

# Time plot of stock adjusted close prices
stockRS = stockPx['Adj Close'].copy()

#---------------------------------------Relative Strength (RS)---------------------------------------
for t in TICKERS:
    # Calculate RS values for each stock vs sector
    rs_df = RS(stockRS[[t, BENCHMARK]])
    # Calculate RS SMA values for each stock vs sector
    rs_df['RSSMA50'] = RSSMA(rs_df, 50)
    rs_df['RSSMA150'] = RSSMA(rs_df, 150)
    rs_df['RSSMA200'] = RSSMA(rs_df, 200)

    # Visualizing recent 200-day adjusted close price, RS, and RS SMA values
    fig = plt.figure()
    ax1 = fig.add_subplot(211, title=t + ' Daily Prices', ylabel='Price in USD ($)')
    stockRS[t].tail(200).plot(ax=ax1, color='k', lw=2.)
    ax2 = fig.add_subplot(212, ylabel='RS (' + BENCHMARK + ')')
    rs_df['RS'].tail(200).plot(ax=ax2, color='goldenrod', lw=2.)
    rs_df['RSSMA50'].tail(200).plot(ax=ax2, color='y', lw=2.)
    rs_df['RSSMA150'].tail(200).plot(ax=ax2, color='g', lw=2.)
    rs_df['RSSMA200'].tail(200).plot(ax=ax2, color='r', lw=2.)
    plt.legend(prop={'size': 8})
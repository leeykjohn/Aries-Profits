'''
This program guides user to visualize trade opportunities, position sizes, and profits/losses of the mean reversion strategy.
'''

# Setting working directory
DIR = 'C:/Users/user/Documents/GitHub/leeykjohn/Aries-Profits/Products/On-Demand Video Courses/Quantitative Stock Trading Level 1 Quartz Trader/Curriculum/Mean Reversion Strategy'
import sys
sys.path.insert(0, DIR)

# Import relevant packages
import yfinance as yf
import pandas as pd
import matplotlib.pyplot as plt
from MeanReversionStrategy import *

TICKER = 'SPY' # Stock Ticker symbol
START_DATE = '2017-01-01' # Stock data start date
END_DATE = '2023-01-01' # Stock data end date
TOTAL_CAPITAL = 10000 # Total capital or net liquidation value
LOOKBACK_PERIOD_DAYS = 504 # Most recent days to view

# Store adjusted stock prices into a variable
stockPx = yf.download(TICKER, START_DATE, END_DATE)

# Feed price data, capital amount, and lookback period into MeanReversionStrategy function
tradingSx = MeanReversionStrategy(stockPx, TOTAL_CAPITAL, LOOKBACK_PERIOD_DAYS)

# Visualizing graph with technical indicators
fig = plt.figure(figsize = (10, 8))
ax1 = fig.add_subplot(611, title = TICKER + ' Daily Prices', ylabel = 'Price in USD ($)')
tradingSx['Close'].tail(LOOKBACK_PERIOD_DAYS).plot(ax=ax1, color='k', lw=2., legend=True)
tradingSx['EMA20'].tail(LOOKBACK_PERIOD_DAYS).plot(ax=ax1, color='magenta', lw=2., linestyle='dotted', legend=True)
tradingSx['SMA50'].tail(LOOKBACK_PERIOD_DAYS).plot(ax=ax1, color='y', lw=2., legend=True)
tradingSx['UpperBBAND'].plot(ax=ax1, color='r', lw=2., linestyle='dashed', legend=True)
tradingSx['LowerBBAND'].plot(ax=ax1, color='g', lw=2., linestyle='dashed', legend=True)
ax1.plot(tradingSx.tail(LOOKBACK_PERIOD_DAYS).loc[tradingSx.Trades == 1 ].index
         , tradingSx.Close.tail(LOOKBACK_PERIOD_DAYS)[tradingSx.Trades == 1]
         , color='g', lw=0, marker='^', markersize=5, label='Buy'); ax1.legend()
ax1.plot(tradingSx.tail(LOOKBACK_PERIOD_DAYS).loc[tradingSx.Trades == -1 ].index
         , tradingSx.Close.tail(LOOKBACK_PERIOD_DAYS)[tradingSx.Trades == -1]
         , color='r', lw=0, marker='v', markersize=5, label='Sell'); ax1.legend()
ax2 = fig.add_subplot(612, ylabel='MACD Histogram')
tradingSx['MACDHistogram'].tail(LOOKBACK_PERIOD_DAYS).plot(ax=ax2, color='blue', kind='bar', legend=True)
ax3 = fig.add_subplot(613, ylabel='Stochastic Oscillator')
tradingSx['%K'].plot(ax=ax3, color='goldenrod', lw=2., legend=True)
tradingSx['%D'].plot(ax=ax3, color='red', lw=2., legend=True)
ax3.axhline(y=80, linewidth=2, color='grey', linestyle='dashed')
ax3.axhline(y=20, linewidth=2, color='grey', linestyle='dashed')
ax4 = fig.add_subplot(614, ylabel='RSI (10-day)')
tradingSx['RSI10'].plot(ax=ax4, color='goldenrod', lw=2., legend=True)
ax4.axhline(y=70, linewidth=2, color='grey', linestyle='dashed')
ax4.axhline(y=30, linewidth=2, color='grey', linestyle='dashed')
ax5 = fig.add_subplot(615, ylabel='Williams % R (10-day)')
tradingSx['WR10'].plot(ax=ax5, color='goldenrod', lw=2., legend=True)
ax5.axhline(y=-80, linewidth=2, color='grey', linestyle='dashed')
ax5.axhline(y=-20, linewidth=2, color='grey', linestyle='dashed')
ax6 = fig.add_subplot(616, ylabel='Williams % R (260-day)')
tradingSx['WR260'].plot(ax=ax6, color='goldenrod', lw=2., legend=True)
ax6.axhline(y=-80, linewidth=2, color='grey', linestyle='dashed')
ax6.axhline(y=-20, linewidth=2, color='grey', linestyle='dashed')

# Visualizing position sizes for this strategy
fig = plt.figure()
ax1 = fig.add_subplot(111, title = 'Position Sizes of the Mean Reversion Strategy', ylabel = 'Position Size')
tradingSx['Position'].plot(ax=ax1, color='k', lw=1.)
ax1.plot(tradingSx.loc[tradingSx.Position == 0].index, tradingSx.Position[tradingSx.Position == 0], color='k', lw=0, marker='.', label='Flat') # flat positions
ax1.plot(tradingSx.loc[tradingSx.Position > 0].index, tradingSx.Position[tradingSx.Position > 0], color='g', lw=0, marker='+', label='Long') # long positions
ax1.plot(tradingSx.loc[tradingSx.Position < 0].index, tradingSx.Position[tradingSx.Position < 0], color='r', lw=0, marker='_', label='Short') # short positions
ax1.axhline(y=0, lw=0.5, color='k')
ax1.legend()
ax1.grid()

# Visualizing the pnl for this strategy
fig = plt.figure()
ax1 = fig.add_subplot(111, title = 'PnL of the Mean Reversion Strategy', ylabel = 'PnL')
tradingSx['Pnl'].plot(ax=ax1, color='k', lw=1.)
ax1.plot(tradingSx.loc[tradingSx.Pnl > 0].index, tradingSx.Pnl[tradingSx.Pnl > 0], color='g', lw=0, marker='.', label='+')
ax1.plot(tradingSx.loc[tradingSx.Pnl < 0].index, tradingSx.Pnl[tradingSx.Pnl < 0], color='r', lw=0, marker='.', label='-')
ax1.legend()
ax1.grid()
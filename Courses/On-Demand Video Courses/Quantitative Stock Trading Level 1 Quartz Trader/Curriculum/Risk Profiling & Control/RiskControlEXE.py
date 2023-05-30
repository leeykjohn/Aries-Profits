'''
This script contains code to visualize the risk measures for various trading strategies.
This also serves as a diagnostic program to compare risks of the specified strategies
'''

# Setting working directory
DIR1 = 'C:/Users/user/Documents/GitHub/leeykjohn/Aries-Profits/Products/On-Demand Video Courses' \
       '/Quantitative Stock Trading Level 1 Quartz Trader' \
       '/Curriculum' \
       '/Trend Following Strategy'
DIR2 = 'C:/Users/user/Documents/GitHub/leeykjohn/Aries-Profits/Products/On-Demand Video Courses' \
       '/Quantitative Stock Trading Level 1 Quartz Trader' \
       '/Curriculum' \
       '/Mean Reversion Strategy'
DIR3 = 'C:/Users/user/Documents/GitHub/leeykjohn/Aries-Profits/Products/On-Demand Video Courses' \
       '/Quantitative Stock Trading Level 1 Quartz Trader' \
       '/Curriculum' \
       '/Risk Profiling & Control'

import sys
sys.path += [DIR1, DIR2, DIR3]

# Import relevant packages/modules
import yfinance as yf
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from TrendFollowingStrategy import *
from MeanReversionStrategy import *
from RiskControl import *

# Configure options to display data frames
pd.set_option('display.max_columns', 1000) # to output 1000 columns max
pd.set_option('display.width', 1000) # adjust console size to display data frames

TICKER = 'AAPL' # Stock Ticker symbol
START_DATE = '2017-01-01' # Stock data start date
END_DATE = '2023-01-01' # Stock data end date
TOTAL_CAPITAL = 10000 # Total capital or net liquidation value
LOOKBACK_PERIOD_DAYS = 504 # Most recent days to view

# Store adjusted stock prices into a variable
stockPx = yf.download(TICKER, START_DATE, END_DATE)

# Feed price data, capital amount, and lookback period into TrendFollowingStrategy function
tf_strategy = TrendFollowingStrategy(stockPx, TOTAL_CAPITAL, LOOKBACK_PERIOD_DAYS)
# Feed price data, capital amount, and lookback period into MeanReversionStrategy function
mr_strategy = MeanReversionStrategy(stockPx, TOTAL_CAPITAL, LOOKBACK_PERIOD_DAYS)

#---------------------------------------PnL Distribution---------------------------------------
# Getting daily, weekly, and monthly losses of the strategy
tf_pnls = PnlDistribution(tf_strategy)
mr_pnls = PnlDistribution(mr_strategy)

# Visualizing pnls Distribution for the specified strategy
fig = plt.figure()
ax1 = fig.add_subplot(321, title='Trend Following Daily PnL Distribution', xlabel='Price in USD ($)', ylabel='Density')
_, bins, _ = ax1.hist(tf_pnls[0], bins=50, density=1, alpha=0.5)
ax3 = fig.add_subplot(323, title='Trend Following Weekly PnL Distribution', xlabel='Price in USD ($)', ylabel='Density')
_, bins, _ = ax3.hist(tf_pnls[1], bins=50, density=1, alpha=0.5)
ax5 = fig.add_subplot(325, title='Trend Following Monthly PnL Distribution', xlabel='Price in USD ($)', ylabel='Density')
_, bins, _ = ax5.hist(tf_pnls[2], bins=50, density=1, alpha=0.5)
ax2 = fig.add_subplot(322, title='Mean Reversion Daily PnL Distribution', xlabel='Price in USD ($)', ylabel='Density')
_, bins, _ = ax2.hist(mr_pnls[0], bins=50, density=1, alpha=0.5)
ax4 = fig.add_subplot(324, title='Mean Reversion Weekly PnL Distribution', xlabel='Price in USD ($)', ylabel='Density')
_, bins, _ = ax4.hist(mr_pnls[1], bins=50, density=1, alpha=0.5)
ax6 = fig.add_subplot(326, title='Mean Reversion Monthly PnL Distribution', xlabel='Price in USD ($)', ylabel='Density')
_, bins, _ = ax6.hist(mr_pnls[2], bins=50, density=1, alpha=0.5)
fig.tight_layout()

#---------------------------------------Loss Distribution---------------------------------------
# Getting daily, weekly, and monthly losses of the strategy
tf_losses = LossDistribution(tf_strategy)
mr_losses = LossDistribution(mr_strategy)

# Visualizing losses distribution for the specified strategy
fig = plt.figure()
ax1 = fig.add_subplot(321, title='Trend Following Daily Loss Distribution', xlabel='Price in USD ($)', ylabel='Density')
_, bins, _ = ax1.hist(tf_losses[0], bins=50, density=1, alpha=0.5)
ax3 = fig.add_subplot(323, title='Trend Following Weekly Loss Distribution', xlabel='Price in USD ($)', ylabel='Density')
_, bins, _ = ax3.hist(tf_losses[1], bins=50, density=1, alpha=0.5)
ax5 = fig.add_subplot(325, title='Trend Following Monthly Loss Distribution', xlabel='Price in USD ($)', ylabel='Density')
_, bins, _ = ax5.hist(tf_losses[2], bins=50, density=1, alpha=0.5)
ax2 = fig.add_subplot(322, title='Mean Reversion Daily Loss Distribution', xlabel='Price in USD ($)', ylabel='Density')
_, bins, _ = ax2.hist(mr_losses[0], bins=50, density=1, alpha=0.5)
ax4 = fig.add_subplot(324, title='Mean Reversion Weekly Loss Distribution', xlabel='Price in USD ($)', ylabel='Density')
_, bins, _ = ax4.hist(mr_losses[1], bins=50, density=1, alpha=0.5)
ax6 = fig.add_subplot(326, title='Mean Reversion Monthly Loss Distribution', xlabel='Price in USD ($)', ylabel='Density')
_, bins, _ = ax6.hist(mr_losses[2], bins=50, density=1, alpha=0.5)
fig.tight_layout()

#---------------------------------------Maximum Drawdown---------------------------------------
# Getting max drawdown, drawdown max pnl, and drawdown min pnl of the strategy
tf_max_drawdown = MaximumDrawdown(tf_strategy)
mr_max_drawdown = MaximumDrawdown(mr_strategy)

# Visualizing maximum drawdowns for the specified strategy
fig = plt.figure()
ax1 = fig.add_subplot(211, title='Trend Following Strategy Maximum Drawdown', ylabel='PnL in USD ($)')
tf_strategy['Pnl'].plot(ax = ax1)
ax1.axhline(y=tf_max_drawdown[1], color='g', label='Max PnL')
ax1.axhline(y=tf_max_drawdown[2], color='r', label='Min PnL')
ax1.arrow(x=tf_strategy['Pnl'].index[-1]
          , y=tf_max_drawdown[1]
          , dx=0, dy=-tf_max_drawdown[0]
          , width=10, color='k', length_includes_head = True)
ax1.text(tf_strategy.index[-1]
         , (tf_max_drawdown[1] + tf_max_drawdown[2]) / 2
         , '{0:.{1}f}'.format(tf_max_drawdown[0], 2)
         , color="r", ha="left", va="center_baseline", size = 'large')
plt.legend()
ax2 = fig.add_subplot(212, title='Mean Reversion Strategy Maximum Drawdown', ylabel='PnL in USD ($)')
mr_strategy['Pnl'].plot(ax = ax2)
ax2.axhline(y=mr_max_drawdown[1], color='g', label='Max PnL')
ax2.axhline(y=mr_max_drawdown[2], color='r', label='Min PnL')
ax2.arrow(x=mr_strategy['Pnl'].index[-1]
          , y=mr_max_drawdown[1]
          , dx=0, dy=-mr_max_drawdown[0]
          , width=10, color='k', length_includes_head = True)
ax2.text(mr_strategy.index[-1]
         , (mr_max_drawdown[1] + mr_max_drawdown[2]) / 2
         , '{0:.{1}f}'.format(mr_max_drawdown[0], 2)
         , color="r", ha="left", va="center_baseline", size = 'large')
plt.legend()
fig.tight_layout()

#---------------------------------------Position Distribution---------------------------------------
# Visualizing positions taken for the specified strategy
fig = plt.figure()
ax1 = fig.add_subplot(211, title='Trend Following Position Distribution', xlabel='Position in Shares', ylabel='Density')
_, bins, _ = ax1.hist(tf_strategy['Position'], bins=50, density=1, alpha=0.5)
ax2 = fig.add_subplot(212, title='Mean Reversion Position Distribution', xlabel='Position in Shares', ylabel='Density')
_, bins, _ = ax2.hist(mr_strategy['Position'], bins=50, density=1, alpha=0.5)
fig.tight_layout()

#---------------------------------------Position Holding Time---------------------------------------
# Getting position holding times of the strategy
tf_position_holding_times = PositionHoldingTime(tf_strategy)
mr_position_holding_times = PositionHoldingTime(mr_strategy)

# Visualizing position holding times for the specified strategy
fig = plt.figure()
ax1 = fig.add_subplot(211, title='Trend Following Position Holding Time Distribution', xlabel='Holding time days', ylabel='Density')
_, bins, _ = ax1.hist(tf_position_holding_times, bins=50, density=1, alpha=0.5)
ax2 = fig.add_subplot(212, title='Mean Reversion Position Holding Time Distribution', xlabel='Holding time days', ylabel='Density')
_, bins, _ = ax2.hist(mr_position_holding_times, bins=50, density=1, alpha=0.5)
fig.tight_layout()

#---------------------------------------Execution Distribution---------------------------------------
# Getting daily, weekly, and monthly executions of the strategy
tf_executions = ExecutionDistribution(tf_strategy)
mr_executions = ExecutionDistribution(mr_strategy)

# Visualizing executions distribution for the specified strategy
fig = plt.figure()
ax1 = fig.add_subplot(321, title='Trend Following Daily Execution Distribution', xlabel='Number of Executed Orders', ylabel='Density')
_, bins, _ = ax1.hist(tf_executions[0], bins=50, density=1, alpha=0.5)
ax3 = fig.add_subplot(323, title='Trend Following Weekly Execution Distribution', xlabel='Number of Executed Orders', ylabel='Density')
_, bins, _ = ax3.hist(tf_executions[1], bins=50, density=1, alpha=0.5)
ax5 = fig.add_subplot(325, title='Trend Following Monthly Execution Distribution', xlabel='Number of Executed Orders', ylabel='Density')
_, bins, _ = ax5.hist(tf_executions[2], bins=50, density=1, alpha=0.5)
ax2 = fig.add_subplot(322, title='Mean Reversion Daily Execution Distribution', xlabel='Number of Executed Orders', ylabel='Density')
_, bins, _ = ax2.hist(mr_executions[0], bins=50, density=1, alpha=0.5)
ax4 = fig.add_subplot(324, title='Mean Reversion Weekly Execution Distribution', xlabel='Number of Executed Orders', ylabel='Density')
_, bins, _ = ax4.hist(mr_executions[1], bins=50, density=1, alpha=0.5)
ax6 = fig.add_subplot(326, title='Mean Reversion Monthly Execution Distribution', xlabel='Number of Executed Orders', ylabel='Density')
_, bins, _ = ax6.hist(mr_executions[2], bins=50, density=1, alpha=0.5)
fig.tight_layout()

#---------------------------------------Trading Volume---------------------------------------
# Getting daily, weekly, and monthly trading volumes of the strategy
tf_volume = TradingVolume(tf_strategy)
mr_volume = TradingVolume(mr_strategy)

# Visualizing trading volumes for the specified strategy
fig = plt.figure()
ax1 = fig.add_subplot(111, title='Trend Following vs Mean Reversion Trading Volume', ylabel='Trading Volume in Shares')
ax1.bar(['Trend Following', 'Mean Reversion'], [tf_volume, mr_volume], width=0.8)
for i, v in enumerate([tf_volume, mr_volume]):
    ax1.text(i, v + 5, str(v), color='b', fontweight='bold')

#---------------------------------------Sharpe Ratio---------------------------------------
# Getting daily, weekly, monthly sharpe ratios for the strategy
tf_sharpe_ratio = SharpeRatio(tf_strategy)
mr_sharpe_ratio = SharpeRatio(mr_strategy)
sharp_ratio_table = pd.DataFrame({'Trend Following SR': tf_sharpe_ratio, 'Mean Reversion SR': mr_sharpe_ratio})

# Visualizing sharpe ratios for the specified strategy
fig = plt.figure()
ax1 = fig.add_subplot(111, title='Trend Following vs Mean Reversion Sharpe Ratios', ylabel='Sharpe Ratio')
sharp_ratio_table.plot(ax = ax1, kind = 'bar')
ax1.set_xticklabels(['Daily (1-day)', 'Weekly (5-day)', 'Monthly (18-day)'], rotation  =  45)
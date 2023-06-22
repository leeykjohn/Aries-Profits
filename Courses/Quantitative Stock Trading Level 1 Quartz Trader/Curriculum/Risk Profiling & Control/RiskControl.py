'''
This script contains functions to compute risk measures for the various trading strategies.
'''

import numpy as np

#---------------------------------------PnL Distribution---------------------------------------
# Function to calculate the position holding times (in days)
def PnlDistribution(strategy_data):

    # Get PnL from strategy results
    pnl = strategy_data['Pnl']

    # Initiate last day, week, month index
    last_1d = 0; last_5d = 0; last_18d = 0
    # Lists to track daily, weekly, monthly pnls
    pnls_1d = []; pnls_5d = []; pnls_18d = []
    # Lists to track daily, weekly, monthly lossese
    losses_1d = []; losses_5d = []; losses_18d = []

    # Iterate through pnls day by day
    for i in range(0, len(pnl)):

        if i - last_1d >= 1: # track daily pnl
            pnl_change_1d = pnl[i] - pnl[last_1d]
            pnls_1d.append(pnl_change_1d)
            if pnl_change_1d < 0:
                losses_1d.append(pnl_change_1d)
            last_1d = i

        if i - last_5d >= 5: # track weekly pnl
            pnl_change_5d = pnl[i] - pnl[last_5d]
            pnls_5d.append(pnl_change_5d)
            if pnl_change_5d < 0:
                losses_5d.append(pnl_change_5d)
            last_5d = i

        if i - last_18d >= 18: # track monthly pnl
            pnl_change_18d = pnl[i] - pnl[last_18d]
            pnls_18d.append(pnl_change_18d)
            if pnl_change_18d < 0:
                losses_18d.append(pnl_change_18d)
            last_18d = i

    return (pnls_1d, pnls_5d, pnls_18d)

#---------------------------------------Loss Distribution---------------------------------------
# Function to calculate daily, weekly, and monthly losses allowed by the strategy
def LossDistribution(strategy_data):

    # Get PnL from strategy results
    pnl = strategy_data['Pnl']

    # List to contain strategy loss amounts
    losses_1d = []; losses_5d = []; losses_18d = []

    # Iterate through pnls day by day
    for i in range(0, len(pnl)):

        if i >= 1 and pnl[i - 1] > pnl[i]: # daily loss
            losses_1d.append(pnl[i] - pnl[i - 1])
        if i >= 5 and pnl[i - 5] > pnl[i]: # weekly loss
            losses_5d.append(pnl[i] - pnl[i - 5])
        if i >= 18 and pnl[i - 18] > pnl[i]: # monthly loss
            losses_18d.append(pnl[i] - pnl[i - 18])

    return (losses_1d, losses_5d, losses_18d)

#---------------------------------------Maximum Drawdown---------------------------------------
# Function to calculate mmax drawdown, drawdown max pnl, and drawdown min pnl of the strategy
def MaximumDrawdown(strategy_data):

    # Get PnL from strategy results
    pnl = strategy_data['Pnl']

    max_pnl = 0 # maximum pnl
    max_drawdown = 0 # maximum drawdown
    drawdown_max_pnl = 0 # drawdown maximum pnl
    drawdown_min_pnl = 0 # drawdown minimum pnl

    # Iterate through pnls day by day
    for i in range(0, len(pnl)):

        # Highest between previous max pnl and current pnl
        max_pnl = max(max_pnl, pnl[i])
        # Drawdown is current max pnl - current pnl
        drawdown = max_pnl - pnl[i]

        # Update max drawdown pnls if current is the max drawdown
        if drawdown > max_drawdown:
            max_drawdown = drawdown
            drawdown_max_pnl = max_pnl
            drawdown_min_pnl = pnl[i]

    return (max_drawdown, drawdown_max_pnl, drawdown_min_pnl)

#---------------------------------------Position Holding Time---------------------------------------
# Function to calculate the position holding times (in days)
def PositionHoldingTime(strategy_data):

    # Get position from strategy results
    position = strategy_data['Position']

    # List to contain position holding times
    position_holding_times = []
    current_pos = 0 # track current position
    current_pos_start = 0 # track current position start day

    # Iterate through positions day by day
    for i in range(0, len(position)):

        pos = position.iloc[i] # index position size

        # flat and starting a new position
        if current_pos == 0:
            if pos != 0:
                current_pos = pos
                current_pos_start = i
            continue

        # going from long position to flat or short position or
        # going from short position to flat or long position
        if current_pos * pos <= 0:
            current_pos = pos
            position_holding_times.append(i - current_pos_start)
            current_pos_start = i

    return position_holding_times

#---------------------------------------Execution Distribution---------------------------------------
# Function to track the number of executions for the strategy
def ExecutionDistribution(strategy_data):

    # Get trade orders from strategy results
    trades = strategy_data['Trades']

    # Initiate current dayly, weekly, monthly executions
    executions_current_1d = 0; executions_current_5d = 0; executions_current_18d = 0
    # Lists to track daily, weekly, monthly executions
    executions_per_1d = []; executions_per_5d = []; executions_per_18d = []
    # Initiate last day, week, month index
    last_1d = 0; last_5d = 0; last_18d = 0

    # Iterate through trades day by day
    for i in range(0, len(trades)):

        # Track executions daily
        if trades.iloc[i] != 0:
            executions_current_1d += 1
        if i - last_1d >= 1:
            executions_per_1d.append(executions_current_1d)
            executions_current_1d = 0
            last_1d = i

        # Track executions weekly
        if trades.iloc[i] != 0:
            executions_current_5d += 1
        if i - last_5d >= 5:
            executions_per_5d.append(executions_current_5d)
            executions_current_5d = 0
            last_5d = i

        # Track executions monthly
        if trades.iloc[i] != 0:
            executions_current_18d += 1
        if i - last_18d >= 18:
            executions_per_18d.append(executions_current_18d)
            executions_current_18d = 0
            last_18d = i

    return (executions_per_1d, executions_per_5d, executions_per_18d)

#---------------------------------------Trading Volume---------------------------------------
# Function to track the number of executions for the strategy
def TradingVolume(strategy_data):

    # Get trade orders and positions from strategy results
    trades = strategy_data['Trades']
    position = strategy_data['Position']

    # Initiate trading volume
    traded_volume = 0

    # Iterate through volumes day by day
    for i in range(0, len(trades)):
        if trades.iloc[i] != 0:
            traded_volume += abs(position.iloc[i] - position.iloc[i - 1])

    return traded_volume

#---------------------------------------Sharpe Ratio---------------------------------------
# Function to calculate the sharpe ration of the strategy
def SharpeRatio(strategy_data):
    # Get PnL from strategy results
    pnl = strategy_data['Pnl']

    # Initiate last day, week, month index
    last_1d = 0; last_5d = 0; last_18d = 0
    # Lists to track daily, weekly, monthly pnls
    pnls_1d = []; pnls_5d = []; pnls_18d = []
    # Lists to track daily, weekly, monthly lossese
    losses_1d = []; losses_5d = []; losses_18d = []

    # Iterate through pnls day by day
    for i in range(0, len(pnl)):
        if i - last_1d >= 1: # track daily pnl
            pnl_change_1d = pnl[i] - pnl[last_1d]
            pnls_1d.append(pnl_change_1d)
            if pnl_change_1d < 0:
                losses_1d.append(pnl_change_1d)
            last_1d = i

        if i - last_5d >= 5: # track weekly pnl
            pnl_change_5d = pnl[i] - pnl[last_5d]
            pnls_5d.append(pnl_change_5d)
            if pnl_change_5d < 0:
                losses_5d.append(pnl_change_5d)
            last_5d = i

        if i - last_18d >= 18: # track monthly pnl
            pnl_change_18d = pnl[i] - pnl[last_18d]
            pnls_18d.append(pnl_change_18d)
            if pnl_change_18d < 0:
                losses_18d.append(pnl_change_18d)
            last_18d = i

    # Calculating Sharpe Ratio
    sharpe_ratio_1d = np.mean(pnls_1d) / np.std(pnls_1d) # daily
    sharpe_ratio_5d = np.mean(pnls_5d) / np.std(pnls_5d)  # weekly
    sharpe_ratio_18d = np.mean(pnls_18d) / np.std(pnls_18d)  # monthly

    return (sharpe_ratio_1d, sharpe_ratio_5d, sharpe_ratio_18d)
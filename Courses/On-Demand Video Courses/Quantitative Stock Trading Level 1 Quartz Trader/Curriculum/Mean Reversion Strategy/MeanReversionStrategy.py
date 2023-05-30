'''
This script contains function to implement the mean reversion strategy on a single selected stock.
Entry/exit opportunities, position sizes, and profits/losses of the strategy are also tracked.
'''

# Setting working directory
DIR1 = 'C:/Users/user/Documents/GitHub/leeykjohn/Aries-Profits/Products/On-Demand Video Courses' \
       '/Quantitative Stock Trading Level 1 Quartz Trader' \
       '/Curriculum' \
       '/Technical Analysis'
DIR2 = 'C:/Users/user/Documents/GitHub/leeykjohn/Aries-Profits/Products/On-Demand Video Courses' \
       '/Quantitative Stock Trading Level 1 Quartz Trader' \
       '/Curriculum' \
       '/Position Sizing'
import sys
sys.path += [DIR1, DIR2]

# Import relevant packages
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from datetime import datetime
from CandlestickPatterns import *
from TechnicalIndicators import *
from AverageTrueRangeMeasure import *

# Function to implement the mean reversion strategy
def MeanReversionStrategy(data, TOTAL_CAPITAL, LOOKBACK_PERIOD_DAYS):

    df = data.copy() # make a copy of the data

    # Adding indicator columns in the technical indicators table
    df['EMA20'] = EMA(df, 20)

    df['SMA50'] = SMA(df, 50)

    bbands_columns = BBANDS(df, 20, 2)
    df['UpperBBAND'] = bbands_columns[0]
    df['MiddleBBAND'] = bbands_columns[1]
    df['LowerBBAND'] = bbands_columns[2]

    macd_columns = MACD(df, 12, 26, 9)
    df['MACD'] = macd_columns[0]
    df['MACDSignal'] = macd_columns[1]
    df['MACDHistogram'] = macd_columns[2]

    so_columns = StochasticOscillator(df, 5, 3)
    df['%K'] = so_columns[0]
    df['%D'] = so_columns[1]

    df['RSI10'] = RSI(df, 10)

    df['WR10'] = WilliamsR(df, 10)
    df['WR260'] = WilliamsR(df, 260)

    df['ATR'] = ATR(df, 14)

    df = CandlestickPatterns(df)

    # Subset to include the most recent data
    df = df.tail(LOOKBACK_PERIOD_DAYS)

    # ... Code Strategy Parameters Here ...

    orders = [0] # Container for tracking buy/sell order, +1 for buy order, -1 for sell order, 0 for no-action
    positions = [0] # Container for tracking positions, +ve for long positions, -ve for short positions, 0 for flat/no position
    pnls = [0] # Container for tracking total_pnls, this is the sum of closed_pnl

    last_buy_entry_price = 0 # Price at which last buy entry trade was made
    last_buy_exit_price = 0 # Price at which last buy exit trade was made
    last_sell_entry_price = 0 # Price at which last sell entry trade was made
    last_sell_exit_price = 0 # Price at which last sell exit trade was made
    position = 0 # Current position of the trading strategy
    buy_sum_price_qty = 0 # Summation of products of price and quantity for every buy trade made since last time being flat
    buy_sum_qty = 0 # Summation of quantity for every buy trade made since last time being flat
    sell_sum_price_qty = 0 # Summation of products of price and quantity for every sell trade made since last time being flat
    sell_sum_qty = 0 # Summation of quantity for every sell trade made since last time being flat
    open_pnl = 0 # Open/Unrealized PnL marked to market
    closed_pnl = 0 # Closed/Realized PnL so far

    # Minimum price change since last trade before considering trading again, this is to prevent over-trading at/around same prices
    MIN_PRICE_MOVE_FROM_LAST_TRADE = 0

    # Loop through prices, technical indicators, and candlestick patterns day by day
    for i in range(1,len(df)):
        high_c = df.iloc[i]['High']
        low_c = df.iloc[i]['Low']
        price_c = df.iloc[i]['Close']

        ema20_c = df.iloc[i]['EMA20']

        sma50_c = df.iloc[i]['SMA50']

        ubband = df.iloc[i]['UpperBBAND']
        lbband = df.iloc[i]['LowerBBAND']

        mcad_histo = df.iloc[i]['MACDHistogram']

        so_k = df.iloc[i]['%K']
        so_d = df.iloc[i]['%D']

        rsi10 = df.iloc[i]['RSI10']

        wr10 = df.iloc[i]['WR10']
        wr260 = df.iloc[i]['WR260']

        bullish_pin_bar = df.iloc[i]['BullishPinBar']
        bearish_pin_bar = df.iloc[i]['BearishPinBar']
        bullish_engulfing = df.iloc[i]['BullishEngulfing']
        bearish_engulfing = df.iloc[i]['BearishEngulfing']
        one_white_soldier = df.iloc[i]['OneWhiteSoldier']
        one_black_crow = df.iloc[i]['OneBlackCrow']
        morning_star = df.iloc[i]['MorningStar']
        evening_star = df.iloc[i]['EveningStar']

        atr = df.iloc[:i]['ATR'].tail(90).mean()  # Take the average ATR in the most recent 3 months

        # Buy-Entry (all must be met):
        # 1. 20EMA < 50 SMA
        # 2. Bullish pin bar, or bullish engulfing, or one white soldier, or morning star candlestick pattern
        # 3. Reversal pattern pierces or appears below the lower Bollinger Bands
        # 4. Stochastic(5,3) %K < %D and Stochastic(5,3) %K < 20 and Stochastic(5,3) %D < 20, or
            # 10-day Relative Strength Index < 30, or
            # 10-day Williams % R < -80 and 260-day Williams % R < -80, or
            # MACD(12,26,9) histogram > 0
        # 5. Entry price must be at least 1R lower than 20 EMA and at least 2R lower than 50 SMA

        if (ema20_c < sma50_c)\
            and (bullish_pin_bar == 1 or bullish_engulfing == 1 or one_white_soldier == 1 or morning_star == 1)\
            and ((high_c > lbband and low_c < lbband) or (high_c < lbband))\
            and ((so_k < so_d and so_k < 20 and so_d < 20) or (rsi10 < 30) or (wr10 < -80 and wr260 < -80) or (mcad_histo > 0))\
            and (ema20_c - price_c >= atr and sma50_c - price_c >= 2 * atr)\
            and (abs(price_c - max(last_buy_entry_price, last_buy_exit_price)) > MIN_PRICE_MOVE_FROM_LAST_TRADE):

            NUM_SHARES_PER_TRADE = int(np.round((TOTAL_CAPITAL * 0.02) / atr))  # Number of shares to buy/sell on every trade
            MIN_PRICE_MOVE_FROM_LAST_TRADE = atr * 2  # Minimum price movement away from the last buy price
            MIN_PROFIT_TO_CLOSE = atr * 2 * NUM_SHARES_PER_TRADE  # Minimum Open/Unrealized profit at which to close positions and lock profits

            orders.append(1)  # mark the buy trade
            if (price_c >= 10 and price_c < 50):
                last_buy_entry_price = price_c + 0.03  # $0.03 above close
            elif (price_c >= 50 and price_c < 100):
                last_buy_entry_price = price_c + 0.05  # $0.05 above close
            elif (price_c > 100):
                last_buy_entry_price = price_c + 0.1  # $0.1 above close
            else:
                pass

            position += NUM_SHARES_PER_TRADE  # increase position by the size of this trade
            buy_sum_price_qty += (price_c * NUM_SHARES_PER_TRADE)  # update the value of this trade
            buy_sum_qty += NUM_SHARES_PER_TRADE  # update share number in long trades
            # print(df.index[i].strftime('%d-%m-%y'), "Buy ", NUM_SHARES_PER_TRADE, TICKER, " @ ", price_c, "Position: ", position)

        # Buy-Exit:
        # 1. We are in short position and either profit target is hit, stop loss is hit, or price < 50 SMA

        elif (position < 0 and (open_pnl > MIN_PROFIT_TO_CLOSE or price_c - last_sell_entry_price >= atr or price_c < sma50_c)):

            orders.append(1)  # mark the buy trade
            last_buy_exit_price = price_c  # save last buy entry price
            position += NUM_SHARES_PER_TRADE  # increase position by the size of this trade
            buy_sum_price_qty += (price_c * NUM_SHARES_PER_TRADE)  # update the value of this trade
            buy_sum_qty += NUM_SHARES_PER_TRADE  # update share number in long trades
            # print(df.index[i].strftime('%d-%m-%y'), "Buy ", NUM_SHARES_PER_TRADE, TICKER, " @ ", price_c, "Position: ", position)


        # Sell-Entry (all must be met):
        # 1. 20EMA > 50 SMA
        # 2. Bearish pin bar, or bearish engulfing, or one black crow, or evening star candlestick pattern
        # 3. Reversal pattern pierces or appears above the upper Bollinger Bands
        # 4. Stochastic(5,3) %K > %D and Stochastic(5,3) %K > 80 and Stochastic(5,3) %D > 80, or
            # 10-day Relative Strength Index > 70, or
            # 10-day Williams % R > -20 and 260-day Williams % R > -20, or
            # MACD(12,26,9) histogram < 0
        # 5. Entry price must be at least 1R higher than 20 EMA and at least 2R higher than 50 SMA

        elif (ema20_c > sma50_c)\
            and (bearish_pin_bar == 1 or bearish_engulfing == 1 or one_black_crow == 1 or evening_star == 1)\
            and ((high_c > ubband and low_c < ubband) or (low_c > ubband)) \
            and ((so_k > so_d and so_k > 80 and so_d > 80) or (rsi10 > 70) or (wr10 > -20 and wr260 > -20) or (mcad_histo < 0))\
            and (price_c - ema20_c >= atr and price_c - sma50_c >= 2 * atr)\
            and (abs(price_c - max(last_sell_entry_price, last_sell_exit_price)) > MIN_PRICE_MOVE_FROM_LAST_TRADE):

            NUM_SHARES_PER_TRADE = int(np.round((TOTAL_CAPITAL * 0.02) / atr))  # Number of shares to buy/sell on every trade
            MIN_PRICE_MOVE_FROM_LAST_TRADE = atr * 2  # Minimum price movement away from the last sell price
            MIN_PROFIT_TO_CLOSE = atr * 2 * NUM_SHARES_PER_TRADE  # Minimum Open/Unrealized profit at which to close positions and lock profits

            orders.append(-1)  # mark the sell trade
            if (price_c >= 10 and price_c < 50):
                last_sell_entry_price = price_c - 0.03  # $0.03 below close
            elif (price_c >= 50 and price_c < 100):
                last_sell_entry_price = price_c - 0.05  # $0.05 below close
            elif (price_c > 100):
                last_sell_entry_price = price_c - 0.1  # $0.1 below close
            else:
                pass

            position -= NUM_SHARES_PER_TRADE  # reduce position by the size of this trade
            sell_sum_price_qty += (price_c * NUM_SHARES_PER_TRADE)  # update the value of this trade
            sell_sum_qty += NUM_SHARES_PER_TRADE # update share number in short trades
            # print(df.index[i].strftime('%d-%m-%y'), "Sell ", NUM_SHARES_PER_TRADE, TICKER, " @ ", price_c, "Position: ", position)

        # Sell-Exit:
        # 1. We are in long position and either profitable target is hit, stop loss is hit, or price > 50 SMA

        elif (position > 0 and (open_pnl > MIN_PROFIT_TO_CLOSE or last_buy_entry_price - price_c >= atr or price_c > sma50_c)):

            orders.append(-1) # mark the sell trade
            last_sell_exit_price = price_c # save last sell entry price
            position -= NUM_SHARES_PER_TRADE  # reduce position by the size of this trade
            sell_sum_price_qty += (price_c * NUM_SHARES_PER_TRADE)  # update the value of this trade
            sell_sum_qty += NUM_SHARES_PER_TRADE # update share number in short trades
            # print(df.index[i].strftime('%d-%m-%y'), "Sell ", NUM_SHARES_PER_TRADE, TICKER, " @ ", price_c, "Position: ", position)

        else:
            # No trade since none of the conditions were met to buy or sell
            orders.append(0)

        positions.append(position) # track position of this trade

        # Update Open/Unrealized & Closed/Realized Positions
        open_pnl = 0
        if position > 0:
            if sell_sum_qty > 0:  # long position and some sell trades have been made against it, close that amount based on how much was sold against this long position
                open_pnl = abs(sell_sum_qty) * (sell_sum_price_qty / sell_sum_qty - buy_sum_price_qty / buy_sum_qty)
            # mark the remaining position to market i.e. pnl would be what it would be if we closed at current price
            open_pnl += abs(sell_sum_qty - position) * (price_c - buy_sum_price_qty / buy_sum_qty)
        elif position < 0:
            if buy_sum_qty > 0:  # short position and some buy trades have been made against it, close that amount based on how much was bought against this short position
                open_pnl = abs(buy_sum_qty) * (sell_sum_price_qty / sell_sum_qty - buy_sum_price_qty / buy_sum_qty)
            # mark the remaining position to market i.e. pnl would be what it would be if we closed at current price
            open_pnl += abs(buy_sum_qty - position) * (sell_sum_price_qty / sell_sum_qty - price_c)
        else:
            # flat, so update closed_pnl and reset tracking variables for positions & pnls
            closed_pnl += (sell_sum_price_qty - buy_sum_price_qty)
            buy_sum_price_qty = 0
            buy_sum_qty = 0
            sell_sum_price_qty = 0
            sell_sum_qty = 0
            last_buy_entry_price = 0
            last_buy_exit_price = 0
            last_sell_entry_price = 0
            last_sell_exit_price = 0

        # print("OpenPnL: ", open_pnl, " ClosedPnL: ", closed_pnl, " TotalPnL: ", (open_pnl + closed_pnl))
        pnls.append(closed_pnl + open_pnl)

    # Preparing the dataframe from the trading strategy results
    df['Trades'] = orders
    df['Position'] = positions
    df['Pnl'] = pnls

    return df
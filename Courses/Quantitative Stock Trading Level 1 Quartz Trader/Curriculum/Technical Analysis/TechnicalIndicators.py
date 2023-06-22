'''
This script contains functions to derive technical indicators from historical prices in the stock market.
* In practice, multiple technical indicators are used as opposed to just one to generate trading signals.
'''

import statistics as stats
import math as math

#---------------------------------------Simple Moving Average (SMA)---------------------------------------
'''
SMA = ( Sum ( Price, n ) ) / n    

Where: n = Time Period
'''

# Function to generate n-period SMA
def SMA(data, n_period):

    close = data['Close'] # get close prices

    history = [] # to track historical prices
    sma_values = [] # to track n-period SMA values

    for c in close:
        history.append(c) # stores n-period historical prices

        if len(history) > n_period: # remove price that exceeds the n-period lookback
            del (history[0])

        sma_values.append(stats.mean(history)) # averages n-period historical prices

    return sma_values

#---------------------------------------Exponential Moving Average (EMA)---------------------------------------
'''
EMA = (P * 2 / (n + 1)) + (EMAp * (1 - 2 / (n + 1))) = ( P - EMAp ) * 2 / (n + 1) + EMAp

Where:

P = Price for the current period
EMAp = the Exponential moving Average for the previous period
n = the number of periods in a simple moving average roughly approximated by the EMA
'''
# Function to generate n-period EMA
def EMA(data, n_period):

    close = data['Close']  # get close prices

    ema_p = 0 # n-period EMA for the previous period
    ema_values = [] # to track n-period EMA values

    for c in close:
        if ema_p == 0: # check for first observation
            ema_p = c
        else:
            ema_p = (c - ema_p) * 2 / (n_period + 1) + ema_p
        ema_values.append(ema_p)

    return ema_values

#---------------------------------------Moving Average Convergence Divergence (MACD)---------------------------------------
'''
MACD = FastEMA - SlowEMA

Where:

FastEMA = the 12-Period EMA
SlowMA = the 26-Period EMA
SignalLine = the 9-Period EMA of MACD
 '''

# Function to generate MACD
def MACD(data, fast_period, slow_period, macd_period):

    close = data['Close']  # get close prices

    fast_K = 2 / (fast_period + 1) # fast EMA smoothing factor
    fast_ema = 0 # fast ema start
    slow_K = 2 / (slow_period + 1) # slow EMA smoothing factor
    slow_ema = 0 # slow ema start
    macd_K = 2 / (macd_period + 1) # MACD EMA smoothing factor
    macd_ema = 0 # macd ema start

    fast_ema_values = [] # track fast EMA values
    slow_ema_values = [] # track slow EMA values
    macd_values = [] # track MACD values
    macd_ema_values = [] # track MACD EMA values
    macd_histogram_values = [] # MACD histogram values

    for c in close:
      if fast_ema == 0: # first observation
        fast_ema = c
        slow_ema = c
      else:
        fast_ema = (c - fast_ema) * fast_K + fast_ema
        slow_ema = (c - slow_ema) * slow_K + slow_ema

      fast_ema_values.append(fast_ema)
      slow_ema_values.append(slow_ema)

      macd = fast_ema - slow_ema # MACD = fast EMA - slow_EMA

      if macd_ema == 0: # first observation
        macd_ema = macd
      else:
        macd_ema = (macd - macd_ema) * macd_K + macd_ema # signal is EMA of MACD values

      macd_values.append(macd)
      macd_ema_values.append(macd_ema)
      macd_histogram_values.append(macd - macd_ema)

    return [macd_values, macd_ema_values, macd_histogram_values]

#---------------------------------------Bollinger Bands (BBANDS)---------------------------------------
'''
Middle Band = n-period moving average

Upper Band = Middle Band + ( y * n-period standard deviation)

Lower Band = Middle Band - ( y * n-period standard deviation)

Where:

n = number of periods
y = factor to apply to the standard deviation value, (typical default for y = 2)
n-period standard deviation = sqrt(((P1-SMA)^2 + (P2-SMA)^2 + ... (Pn-SMA)^2)/n)
 '''

# Function to generate BBANDS
def BBANDS(data, n_period, stdev_factor):

    close = data['Close']  # get close prices

    history = []  # to track historical prices
    sma_values = []  # to track n-period SMA values
    upper_band = [] # to upper band values
    lower_band = [] # to lower band values

    for c in close:
        history.append(c)  # stores n-period historical prices

        if len(history) > n_period:  # remove price that exceeds the n-period lookback
            del (history[0])

        sma = stats.mean(history)  # averages n-period historical prices as SMA
        sma_values.append(sma)  # averages n-period historical prices

        variance = 0 # variance is the square of standard deviation

        for h in history:
            variance = variance + ((h - sma) ** 2)

        stdev = math.sqrt(variance / len(history)) # square root variance to get standard deviation

        upper_band.append(sma + stdev_factor * stdev)
        lower_band.append(sma - stdev_factor * stdev)

    return [upper_band, sma_values, lower_band]

#---------------------------------------Force Index---------------------------------------
'''
FI(1) = ( CCP - PCP ) * Volume 
FI(13) = 13-Period EMA of FI(1)

Where:

FI(1) = 1-Period Force Index
FI(13) = 13-Period Force Index
CCP = Current Close Price
PCP = Prior Close Price
EMA = Exponential Moving Average
 '''

# Function to generate Force Index
def ForceIndex(data, n_period):

    close = data['Close']  # get close prices
    volume = data['Volume']  # get volumes

    fi1_values = [0] # to track 1-period EMA values of Force Index
    fin_values = [] # to track n-period EMA values of Force Index
    fin_p = 0 # n-period EMA for the previous period Force Index

    # Calculating 1-period Force Index
    for i in range(1, len(close)):
        fi1_values.append((close[i] - close[i-1]) * volume[i])

    # calculate the n-period Force Index with the 1-period Force Index values
    for fi in fi1_values:
        if (fin_p == 0): # check for first observation
            fin_p = fi
        else:
            fin_p = (fi - fin_p) * 2 / (n_period + 1) + fin_p
        fin_values.append(fin_p)

    return fin_values

#---------------------------------------Stochastic Oscillator---------------------------------------
'''
%K = (C - L5) * 100 / (H5 - L5)

%D = ( Sum ( %K, 3 ) ) / 3  

Where:
C = The most recent closing price
L5 = The lowest price traded of the 5 previous trading sessions
H5 = The highest price traded during the same 5-day period
%K = The current value of the stochastic indicator
%D = 3-period moving average of %K
 '''

# Function to generate Stochastic Oscillator
def StochasticOscillator(data, k_period, d_period):

    high = data['High']  # get high prices
    low = data['Low']  # get low prices
    close = data['Close']  # get close prices

    high_history = [] # to track a k-period historical highs
    low_history = [] # to track a k-period historical lows
    high_values = [] # to track k-period highs
    low_values = [] # to track k-period lows
    k_values = [] # to track %K values
    d_history = [] # to track d_period historical %D
    d_values = [] # to track %D values

    for h in high:
        high_history.append(h) # stores k-period historical highs
        if len(high_history) > k_period: # remove price that exceeds the k-period lookback
            del (high_history[0])
        high_values.append(max(high_history)) # take the max of the k-period highs

    for l in low:
        low_history.append(l) # stores k-period historical lows
        if len(low_history) > k_period: # remove price that exceeds the k-period lookback
            del (low_history[0])
        low_values.append(min(low_history)) # take the min of the k-period lows

    # Uses the high, low, and close values to calculate the %K (as a percentage)
    for i in range(len(close)):
        k_values.append((close[i] - low_values[i]) * 100 / (high_values[i] - low_values[i]))

    # Calculate the d_period SMA of %K values
    for k in k_values:
        d_history.append(k) # stores d_period historical %K
        if len(d_history) > d_period: # remove price that exceeds the d_period lookback
            del (d_history[0])
        d_values.append(stats.mean(d_history)) # averages d_period historical %D

    return [k_values, d_values]

#---------------------------------------Williams % R---------------------------------------
'''
Williams % R = -100 * (H - C) / (H - L)

Where:
C = The most recent closing price
L = The lowest price traded of the previous n period
H = The highest price traded of the previous n period
 '''

# Function to generate Williams % R
def WilliamsR(data, n_period):

    high = data['High']  # get high prices
    low = data['Low']  # get low prices
    close = data['Close']  # get close prices

    high_history = [] # to track historical highs
    low_history = [] # to track historical lows
    high_values = [] # to track n_period highs
    low_values = [] # to track n_period lows
    wr_values = [] # to track n_period Williams % R values

    for h in high:
        high_history.append(h) # stores n_period historical highs

        if len(high_history) > n_period: # remove price that exceeds the n_period lookback
            del (high_history[0])

        high_values.append(max(high_history)) # take the max of the n_period highs

    for l in low:
        low_history.append(l) # stores n_period historical lows

        if len(low_history) > n_period: # remove price that exceeds the n_period lookback
            del (low_history[0])

        low_values.append(min(low_history)) # take the min of the n_period lows

    # Uses the high, low, and close values to calculate the Williams % R
    for i in range(len(close)):
        wr_values.append(-100 * (high_values[i] - close[i]) / (high_values[i] - low_values[i]))

    return wr_values

#---------------------------------------Relative Strength Index (RSI)---------------------------------------
'''
RSI = 100 - (100 / (1 + RS))

Where:
RS = abs(smoothed average of n-period gains)/abs(smoothed average of n-period losses)
abs = the absolute value function
 '''

# Function to generate RSI
def RSI(data, n_period):

    close = data['Close']  # get close prices

    gain_history = [] # to track history of gains (0 if no gain, magnitude of gain if gain)
    loss_history = [] # to track history of losses (0 if no loss, magnitude of loss if loss)
    avg_gain_values = [] # track avg gains
    avg_loss_values = [] # track avg losses
    rsi_values = [] # track RSI values
    last_price = 0 # current_price - last_price > 0 ==> gain. current_price - last_price < 0 ==> loss.

    for c in close:
      if last_price == 0:
        last_price = c

      gain_history.append(max(0, c - last_price))
      loss_history.append(max(0, last_price - c))
      last_price = c

      if len(gain_history) > n_period: # remove gains/losses that exceed the n_period lookback
        del (gain_history[0])
        del (loss_history[0])

      avg_gain = stats.mean(gain_history) # average gain over n_period lookback
      avg_loss = stats.mean(loss_history) # average loss over n_period lookback
      avg_gain_values.append(avg_gain) # append average gain
      avg_loss_values.append(avg_loss) # append average gain

      rs = 0 # relative strength starts at 0
      if avg_loss > 0: # to avoid division by 0, which is undefined
        rs = avg_gain / avg_loss

      rsi = 100 - (100 / (1 + rs))
      rsi_values.append(rsi)

    return rsi_values
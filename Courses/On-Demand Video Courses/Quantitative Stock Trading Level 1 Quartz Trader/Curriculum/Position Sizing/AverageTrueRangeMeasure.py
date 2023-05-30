'''
This script contains functions to derive the Average True Range (ATR) measure for the stocks to trade.
'''

import statistics as stats
import pandas as pd
import numpy as np

#---------------------------------------Average True Range (ATR) Measure---------------------------------------
# Function to calculate ATR
def ATR(data, n_period): # input is a two-column price data

    high_low = data['High'] - data['Low'] # H-L
    high_close = np.abs(data['High'] - data['Close'].shift()) # |H-Cp|
    low_close = np.abs(data['Low'] - data['Close'].shift()) # |L-Cp|
    ranges = pd.concat([high_low, high_close, low_close], axis=1) # combine the above three measure
    true_range = np.max(ranges, axis=1) # find max of the three measures for each day
    atr_values = true_range.rolling(n_period).mean().values # average the true range over n_period days

    return atr_values



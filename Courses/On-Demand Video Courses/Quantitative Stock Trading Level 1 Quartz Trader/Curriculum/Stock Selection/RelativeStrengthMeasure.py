'''
This script contains functions to derive Relative Strength measure for the screened stocks relative to their sectors.
'''

import statistics as stats
import pandas as pd

#---------------------------------------Relative Strength (RS) Measure---------------------------------------
# Function to calculate RS
def RS(data): # input is a two-column price data

    # Divide stock prices with Sector ETF prices to get RS
    rs_df = pd.DataFrame(data.iloc[:, 0] / data.iloc[:, 1], columns = ['RS'])

    return rs_df

#---------------------------------------Relative Strength (RS) SMA Measure---------------------------------------
# Function to calculate RS SMA
def RSSMA(rs_df, n_period):

    rs_history = []  # to track historical RS
    rs_sma_values = []  # to track n-period SMA values

    for rs in rs_df['RS']:

        rs_history.append(rs)  # stores n-period historical RS

        if len(rs_history) > n_period:  # remove RS that exceeds the n-period lookback
            del (rs_history[0])

        rs_sma_values.append(stats.mean(rs_history))  # averages n-period historical RS

    return rs_sma_values







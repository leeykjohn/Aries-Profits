'''
This script contains function to identify candlestick patterns in the stock market.
* In practice, candlestick patterns MUST be used with technical indicators to generate trading signals.
'''

# Import relevant packages
import pandas as pd

# Function to generate candlestick pattern logics
def CandlestickPatterns(data):

    df = data.copy() # make a copy of the data

    # Use a for loop to calculate to identify candlestick patterns
    for i in range(2, len(df)):
        current = df.iloc[i,:]
        prev = df.iloc[i-1,:]
        prev2 = df.iloc[i-2,:]
        body_c = abs(current['Open'] - current['Close'])
        body_prev = abs(prev['Open'] - prev['Close'])
        body_prev2 = abs(prev2['Open'] - prev2['Close'])
        range_c = current['High'] - current['Low']
        range_prev = prev['High'] - prev['Low']
        range_prev2 = prev2['High'] - prev2['Low']
        idx = df.index[i]

        # ... Code Candlestick Patterns Here ...

        # Bullish Pin Bar
        df.loc[idx,'BullishPinBar'] = (body_c <= range_c / 3) \
                                              and (min(current['Open'], current['Close']) > (current['High'] + current['Low'])/2) \
                                              and (current['Low'] < prev['Low'])
        # Bearish Pin Bar
        df.loc[idx, 'BearishPinBar'] = (body_c <= range_c / 3) \
                                               and (max(current['Open'], current['Close']) < (current['High'] + current['Low']) / 2) \
                                               and (current['High'] > prev['High'])
        # Bullish Engulfing
        df.loc[idx, 'BullishEngulfing'] = (prev['Close'] < prev['Open']) \
                                                 and (current['Close'] > current['Open']) \
                                                 and (current['High'] > prev['High']) \
                                                 and (current['Low'] < prev['Low']) \
                                                 and (current['Close'] > prev['Open']) \
                                                 and (current['Open'] < prev['Close']) \
                                                 and (body_c >= 0.8 * range_c)
        # Bearish Engulfing
        df.loc[idx,'BearishEngulfing'] = (prev['Close'] > prev['Open']) \
                                                 and (current['Close'] < current['Open']) \
                                                 and (current['High'] > prev['High']) \
                                                 and (current['Low'] < prev['Low']) \
                                                 and (current['Close'] < prev['Open']) \
                                                 and (current['Open'] > prev['Close']) \
                                                 and (body_c >= 0.8 * range_c)
        # One White Soldier (OWS)
        df.loc[idx, 'OneWhiteSoldier'] = (prev['Close'] < prev['Open']) \
                                                 and (current['Close'] > current['Open']) \
                                                 and (body_prev >= 0.8 * range_prev) \
                                                 and (body_c >= 0.8 * range_c) \
                                                 and (current['Open'] > prev['Close']) \
                                                 and (current['Close'] > prev['High'])
        # One Black Crow (OBC)
        df.loc[idx,'OneBlackCrow'] = (prev['Close'] > prev['Open']) \
                                             and (current['Close'] < current['Open']) \
                                             and (body_prev >= 0.8 * range_prev) \
                                             and (body_c >= 0.8 * range_c) \
                                             and (current['Open'] < prev['Close']) \
                                             and (current['Close'] < prev['Low'])
        # Morning Star
        df.loc[idx, 'MorningStar'] = (prev2['Close'] < prev2['Open']) \
                                            and (body_prev2 >= 0.6 * range_prev2) \
                                            and (body_prev <= 0.2 * range_prev) \
                                            and (max(prev['Open'], prev['Close']) < prev2['Close']) \
                                            and (max(prev['Open'], prev['Close']) < current['Open']) \
                                            and (current['Close'] > current['Open']) \
                                            and (current['Close'] > (prev2['Open'] + prev2['Close']) / 2)
        # Evening Star
        df.loc[idx,'EveningStar'] = (prev2['Close'] > prev2['Open']) \
                                           and (body_prev2 >= 0.6 * range_prev2) \
                                           and (body_prev <= 0.2 * range_prev) \
                                           and (min(prev['Open'], prev['Close']) > prev2['Close']) \
                                           and (max(prev['Open'], prev['Close']) > current['Open']) \
                                           and (current['Close'] < current['Open']) \
                                           and (current['Close'] < (prev2['Open'] + prev2['Close']) / 2)

    # NaN rows will not have a signal, so False
    df.fillna(False, inplace=True)

    return df
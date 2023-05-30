'''
This script contains code to output correlation heatmap for the selected stocks.
'''

#---------------------------------------Correlation Heatmap---------------------------------------
# Import relevant packages
import yfinance as yf
import numpy as np
import seaborn as sns
import matplotlib.pyplot as plt

TICKERS = ['CMG', 'JPM', 'HLT', 'GLD','C']  # Stock Ticker symbols
START_DATE = '2017-01-01'  # Stock data start date
END_DATE = '2023-01-01'  # Stock data end date
# Store adjusted stock prices into a variable
stockPx = yf.download(TICKERS, START_DATE, END_DATE)['Adj Close']

# converting prices to log returns and removing NaN values
stockLogRetList = np.log(stockPx).diff().dropna()
# visualizing correlation heatmap
sns.heatmap(stockLogRetList.corr(), annot=True)
plt.title("Correlations Coefficients Between Stock Log Returns")
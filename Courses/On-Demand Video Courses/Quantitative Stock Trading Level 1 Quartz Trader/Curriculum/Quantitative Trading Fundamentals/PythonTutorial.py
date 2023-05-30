# Anything preceded by '#' are comments and will not be run as a command.

#----------------------------Data Structures----------------------------
# Assigning an integer to a variable
n = 10 # a small integer
t = 9e6 # equivalent to 9000000, a large integer

# Assigning a decimal to a variable
pi = 3.1316

# Assigning a boolean to a variable
b1 = True
b2 = False

# Assigning a character to a variable
char = 'a'

# Assigning a string to a variable
message = "You are in charge of your own portfolio."

# Assigning a list of values to a variable - a list can store any data types
ls1 = [1, 0.75, 999]
ls2 = ["META", "AAPL", "NFLX"]
ls3 = [10, 22, 45, 6,67, 22, 'A', "SPY"]

# Assigning a tuple of numbers to a variable - unlike lists, tuples are immutable
tup = (66, 77, 88, 99)

# Assigning a set of values to a variable - values in a set are distinct
s = {"Singapore", "United States", "United States", "Hong Kong", "Russia", "Russia"} # equivalent to {"Singapore", "United States", "Hong Kong", "Russia"}

# Assigning a dictionary of values to a variable
dx = {'JPM': 131.59, 'PFE': 49.71, 'KO': 63.44, 'AAPL':151.9}
dx.keys() # dict_keys(['JPM', 'PFE', 'KO', 'AAPL'])
dx.values() # dict_values([131.59, 49.71, 63.44, 151.9])

#----------------------------Indexing----------------------------
# Indexing a list
ls1[0] # 1
ls1[1] # 0.75
ls1[2] # 999
ls2[-1] # 'NFLX'
ls2[-2] # 'AAPL'
ls2[-3] # 'META'

# Indexing a tuple
tup[0] # 66
tup[-1] # 99

# A set is not subscriptable

# Indexing a dictionary
dx['JPM'] # 131.59
dx['PFE'] # 49.71
dx['KO'] # 63.44
dx['AAPL'] # 151.9

#----------------------------Arithmetic Operations----------------------------
# Addition
y1 = n + 25 # 35
# Subtraction
y2 = y1 - 11 # 24
# Multiplication
y3 = y2 * 2 # 48
# Division
y4 = y3 / 4 # 12
# Raising y4 to the 2nd power then assigning the result to y5
y5 = y4 ** 2 # 144
# Add 10 to y4 then assign the result to itself
y5 += 52 # 196
# Subtract 100 from y4 then assign the result to itself
y5 -= 100 # -96
# Multiply y4 by -0.5 then assign the result to itself
y5 *= -0.5 # -48
# Divide y4 by 5 then assign the result to itself
y5 /= 5 # -9.6
# Raising y5 to the 3rd power then assigning the result itself
y5 **= 3 # -884.7359999999999

#----------------------------Functions----------------------------
# Convert a decimal to an integer, no round off
int(y5) # -884

# Convert integers and strings to floating-point (decimal) numbers
float(n) # 10.0
float('-7') # 7.0

# Convert integers and floats to strings
str(n) # '10'
str(y5) # '-884.7359999999999'

# Convert a tuple to a list
list(tup) # [66, 77, 88, 99]
# Convert a list to a tuple
tuple(ls1) # (1, 0.75, 999)

# Length of a variable
len('A') # 1
len('AAPL') # 4
len(ls1) # 3
len(tup) # 4
len(dx) # 4

# Print message
print('Treat trading as your own business.')

# Print message with the format method
print('I have {} stocks in my portfolio. The maximum drawdown is {}.'. format(n, y5))

# Create a function that prints a stock's price
def StockPx(ticker, price): # first argument stock ticker; second argument: stock price
    print('The market price of {} is ${}.'.format(ticker, price))
StockPx("GOOG", 96.96) # The market price of GOOG is $96.96.

# Create a function that calculates market cap of a stock
def MktCap(ticker, price, num_shares): # first argument stock ticker; second argument: stock price; third argument: number of shares outstanding
    mkt_cap = price * num_shares
    print('The market cap of {} is ${}.'.format(ticker, mkt_cap))
MktCap("GOOG", 96.96, 13.982e9) # The market cap of GOOG is $1355694720000.0.

# Create a function that calculates the percentage return of a stock trade
def StockPctReturn(ticker, entry_price, exit_price): # first argument stock ticker; second argument: stock price; third argument: number of shares outstanding
    pct_ret = round((exit_price - entry_price) * 100 / entry_price, 2) # round to 2 decimal places
    print('The percentage return of {} is {} %.'.format(ticker, pct_ret))
StockPctReturn("GOOG", 96.96, 121.74) # The percentage return of GOOG is 25.56 %.

#----------------------------Other Operators----------------------------
# Floor division returns the divided outcome, rounding down to an integer
minutes = 105
hours = minutes // 60 # 1

# Modulus divides the two numbers and returns the remainder
remainder = minutes % 60  # 45

# Boolean expressions to check for equality (==)
1 == 1 # True
1 == 2 # False
ls1 == ls2 # False
n % 2 == 0 # True

# Boolean expressions to check for inequality (!=)
1 != 2 # True
1 != 1 # False
ls1 != ls2 # True

# Boolean expressions to check for other inequalities (>, <, >=, <=)
1 > 2 # False
1 < 2 # True
1 >= 2 # True
2 <= 2 # True

# Conjunction
1 == 1 and 1 == 2 # False
1 == 1 or 1 == 2 # True
1 == 1 and n % 2 == 0 # True
1 == 1 or n % 2 == 0 # True

#----------------------------Conditional Statements----------------------------
# if else statement to check for even or odd numbers
if n % 2 == 0:
    print('{} is an even number.'.format(n))
else:
    print('{} is an odd number.'.format(n))

# if else statement to determine market size
mkt_cap = 96.96 * 13.982e9 # share price * number of shares outstanding
if mkt_cap > 10e9:
    print('Large Cap')
elif mkt_cap > 2e9 and mkt_cap <= 10e9:
    print('Medium Cap')
else:
    print('Small Cap')
# Large Cap

#----------------------------For Loop Iteration----------------------------
# For loops through a set
for country in s:
    print(country)

# For loop with conditional statements to discover market price
for ticker in ls2:
    if ticker in dx.keys():
        print('{} is worth ${} per share.'. format(ticker, dx[ticker]))
    else:
        print('{} price not found.'.format(ticker))

# For loop to index multiple values in a list or tuple
[ls3[i] for i in range(3)] # [10, 22, 45]
[tup[i] for i in range(2)] # [66, 77]
[ls3[i] for i in range(len(ls3)) if i % 2 == 0] # [10, 45, 67, 'A'] - even number indexes
[tup[i] for i in range(len(tup)) if i % 2 != 0] # [77, 99] - odd number indexes

# While loop with conditional statement to determine when to exit a trade
p1 = 96.96 # stock price
d1 = 0 # number of days till exit
while p1 >= 70: # execute sell stop order when stock price falls below $70
    p1 *= (1 - 0.025) # assume stock price drops 2.5% daily on average
    d1 += 1
print('It takes {} days until trade exit.'.format(d1))
# It takes 13 days until trade exit.

#----------------------------Recursive Interation----------------------------
# Recursive function to determine when to exit a trade
def DaysUntilTradeExit(price, days):
    if price < 70: # execute sell stop order when stock price falls below $70
        print('It takes {} days until trade exit.'.format(days))
    else:
        DaysUntilTradeExit(price * (1 - 0.025), days + 1) # assume stock price drops 2.5% daily on average
p2 = 96.96  # stock price
d2 = 0  # number of days till exit
DaysUntilTradeExit(p2, d2) # It takes 13 days until trade exit.

#----------------------------Starter Code for Financial Data----------------------------
# Import relevant packages
import yfinance as yf
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt

TICKER = 'SPY' # Stock Ticker symbol
START_DATE = '2016-01-01' # Stock data start date
END_DATE = '2022-01-01' # Stock data end date

# Store adjusted stock prices into a variable
stockPx = yf.download(TICKER, START_DATE, END_DATE)

# Configure options to display data frames
pd.set_option('display.max_rows', 1000) # to output 1000 rows max
pd.set_option('display.max_columns', 1000) # to output 1000 columns max
pd.set_option('display.width', 1000) # adjust console size to display data frames

# Display rows of Yahoo stock data
stockPx

# Summary statistics of Yahoo stock data
stockPx.describe()

# Time plot of stock adjusted close prices
stockPxAj = stockPx['Adj Close'] # index adjusted close price column
stockPxAj.plot(title = TICKER + ' Daily Prices', ylabel = 'Price in USD ($)', color = 'k')

# Covert stock price to log returns
stockLogRet = np.log(stockPxAj).diff().dropna() # calculate log returns and drop null values
# Time plot of stock log returns
stockLogRet.plot(title = TICKER + ' Daily Log Returns', ylabel = 'Log Return', color = 'k')

# Histogram of stock log returns
_, bins, _= plt.hist(stockLogRet, bins=50, density=1, alpha=0.5, color = 'k')
plt.title('Histogram of ' + TICKER + ' Daily Log Returns') # label title
plt.xlabel('Log Return') # label x-axis
plt.ylabel('Density') # label y-axis

# Boxplot of stock log returns
_ = plt.boxplot(stockLogRet, vert = False)
plt.title('Boxplot of ' + TICKER + ' Daily Log Returns') # label title
plt.xlabel('Log Return') # label x-axis
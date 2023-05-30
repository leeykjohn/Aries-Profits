'''
This program copies the ticker symbols of the filtered stocks.
Next step is to paste them into the watchlist you created in TOS.
'''

# Setting working directory
DIR = 'C:/Users/user/Documents/GitHub/leeykjohn/Aries-Profits/Products/On-Demand Video Courses/Quantitative Stock Trading Level 1 Quartz Trader/Curriculum/Stock Selection'
import sys
sys.path.insert(0, DIR)

# Import relevant packages
# ! pip install pyperclip
import pyperclip
from FinvizScreener import FinvizScreener

# Setting filter criteria into variables
fsector = "Consumer Cyclical" # stock sector
fmarket_cap = "Medium Cap" # market size
fprice = "Over $10" # stock price
fshares_oustanding = ("Over 5M", "Under 20M") # # of shares outstanding
faverage_volume = "Over 200K" # stock average volume

# Return the list of stocks that meet the specified criteria
final_ticker = FinvizScreener(fsector, fmarket_cap, fprice, fshares_oustanding, faverage_volume)
final_ticker_text = ', '.join([t for t in final_ticker]) # convert list to string
pyperclip.copy(final_ticker_text) # copy the string of filtered stock symbols (equivalent to CTRL + C)
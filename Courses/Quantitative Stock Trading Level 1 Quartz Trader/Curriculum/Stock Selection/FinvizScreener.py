'''
This script contains a function to screen for stocks from Finviz.com before implementing our strategy setups.
'''

# ! pip install finvizfinance
from finvizfinance.screener.overview import Overview

def FinvizScreener(fsector, fmarket_cap, fprice, fshares_oustanding, faverage_volume):

    # Define small, medium, and large market cap.
    fmarket_cap_dict = {"Large Cap": ["Mega ($200bln and more)", "Large ($10bln to $200bln)"],
                        "Medium Cap": ["Mid ($2bln to $10bln)"],
                        "Samll Cap": ["Small ($300mln to $2bln)", "Micro (over $50mln)", "Nano (under $50mln)"]}

    # Iiterate through definitions that matches the specified market cap.
    for i in range(len(fmarket_cap_dict[fmarket_cap])):
        foverview = Overview() # create an overview object to display filtered stocks
        fset１ = {'Sector': fsector
                 , 'Market Cap.':fmarket_cap_dict[fmarket_cap][i]
                 , 'Price':fprice
                 , 'Shares Outstanding':fshares_oustanding[0]
                 , 'Average Volume': faverage_volume} # first set of filters with first outstanding shares criterion
        foverview.set_filter(filters_dict=fset１) # input filter settings into overview object
        try:
            ticker_list1 = foverview.screener_view()["Ticker"].to_list() # extract first list of filtered stocks
        except:
            ticker_list1 = [] # if there are no filtered stocks, then set an empty list

        fset2 = {'Sector': fsector
            , 'Market Cap.': fmarket_cap_dict[fmarket_cap][i]
            , 'Price': fprice
            , 'Shares Outstanding': fshares_oustanding[1]
            , 'Average Volume': faverage_volume} # second set of filters with second shares outstanding shares criterion
        foverview.set_filter(filters_dict=fset2) # input filter settings into overview object
        try:
            ticker_list2 = foverview.screener_view()["Ticker"].to_list() # extract second list of filtered stocks
        except:
            ticker_list2 = [] # if there are no filtered stocks, then set an empty list

        final_ticker = list(set(ticker_list1) & set(ticker_list2)) # find common stock tickers in both filters lists

    return final_ticker
'''
This script contains procedures to derive risk metrics such as Value-at-Risk (VaR) and Expected Shortfall of a single asset portfolio.
'''

#-------------------------Probability Distribution-------------------------
# Import relevant packages
import yfinance as yf
import pandas as pd
import numpy as np
import scipy.stats as stats
import statsmodels.api as sm
import matplotlib.pyplot as plt

TICKER = 'SPY' # Stock Ticker symbol
START_DATE = '2017-01-01' # Stock data start date
END_DATE = '2022-01-01' # Stock data end date

# Store adjusted stock prices into a variable
stockPx = yf.download(TICKER, START_DATE, END_DATE)

# Configure options to display data frames
pd.set_option('display.max_columns', 1000) # to output 1000 columns max
pd.set_option('display.width', 1000) # adjust console size to display data frames

# Time plot of stock adjusted close prices
stockPxAj = stockPx['Adj Close'] # index adjusted close price column

# Covert stock price to log returns
stockLogRet = np.log(stockPxAj).diff().dropna() # calculate log returns and drop null values

# Time plot of stock log returns
fig = plt.figure()
ax1 = fig.add_subplot(111, title = TICKER + ' Daily Log Return', ylabel = 'Log Return')
stockLogRet.plot(ax = ax1) # stock log return series

# Histogram of stock log return
fig = plt.figure()
ax1 = fig.add_subplot(111, title='Histogram of ' + TICKER + ' Daily Log Return', xlabel='Log Return', ylabel='Density')
_, bins, _= ax1.hist(stockLogRet, bins=50, density=1, alpha=0.5) # log returns histogram

# Fit probability curve on log return histogram
fig = plt.figure()
ax1 = fig.add_subplot(111, title=TICKER + ' Daily Log Return with Student-t Fit', xlabel='Log Return', ylabel='Density')
_, bins, _= ax1.hist(stockLogRet, bins=50, density=1, alpha=0.5) # log returns histogram
shape_t, loc_t, scale_t = stats.t.fit(stockLogRet) # shape, location, and scale estimates
fitted_t = stats.t.pdf(bins, shape_t, loc_t, scale_t) # generate theoretical student-t pdf
ax1.plot(bins, fitted_t, label='Student-t PDF', color = 'r', lw=2.) # plot theoretical student-t pdf over histogram

#-------------------------Fit Normal Distribution-------------------------
# Fit Normal Distribution Curve
fig = plt.figure()
loc_norm, scale_norm = stats.norm.fit(stockLogRet) # location and scale estimates
ax1 = fig.add_subplot(111
                      , title=TICKER + ' Daily Log Return with '
                              + 'N('+str(round(loc_norm, 2))
                              +', '
                              +str(round(scale_norm, 2))+'$^{2}$) Fit'
                      , xlabel='Log Return'
                      , ylabel='Density')
_, bins, _= ax1.hist(stockLogRet, bins=50, density=1, alpha=0.5) # log returns histogram
fitted_norm = stats.norm.pdf(bins, loc_norm, scale_norm) # generate theoretical normal pdf
ax1.plot(bins, fitted_norm, label='Normal PDF', color = 'r', lw=2.) # plot theoretical normal pdf over histogram

# Fit Normal QQ Plot
fig = plt.figure()
qq_norm = stats.probplot(stockLogRet, dist = 'norm', sparams= (loc_norm, scale_norm), plot = plt, fit = True)
plt.title('Normal QQ Plot of ' + TICKER + ' Daily Log Return')
plt.ylabel('Sample quantiles')

#-------------------------Fit Student-t Distribution-------------------------
# Fit Student-t Distribution Curve
fig = plt.figure()
shape_t, loc_t, scale_t = stats.t.fit(stockLogRet) # shape, location, and scale estimates
ax1 = fig.add_subplot(111
                      , title=TICKER + " Daily Log Return with $t_{"
                          +str(round(shape_t, 2))+"}$"
                          +"("+str(round(loc_t, 2))
                          +', '
                          + str(round(scale_t, 2))+"$^{2}$) Fit"
                      , xlabel='Log Return'
                      , ylabel='Density')
_, bins, _= ax1.hist(stockLogRet, bins=50, density=1, alpha=0.5) # log returns histogram
fitted_t = stats.t.pdf(bins, shape_t, loc_t, scale_t) # generate theoretical student-t pdf
ax1.plot(bins, fitted_t, label='Student-t PDF', color = 'r', lw=2.) # plot theoretical student-t pdf over histogram

# Fit Student-t QQ Plot
fig = plt.figure()
qq_t = stats.probplot(stockLogRet, dist = 't', sparams= (shape_t, loc_t, scale_t), plot = plt, fit = True)
plt.title('Student-t QQ Plot of ' + TICKER + ' Daily Log Return', size=15)
plt.ylabel('Sample quantiles')

#-------------------------Fit Double Exponential (DExp) Distribution-------------------------
# Fit DExp Distribution Curve
fig = plt.figure()
loc_dexp, scale_dexp = stats.laplace.fit(stockLogRet) # location and scale estimates
ax1 = fig.add_subplot(111
                      , title=TICKER
                              + " Daily Log Return with DExp("+str(round(loc_dexp, 2))
                              +', '
                              + str(round(scale_dexp, 2))+") Fit"
                      , xlabel='Log Return'
                      , ylabel='Density')
_, bins, _= ax1.hist(stockLogRet, bins=50, density=1, alpha=0.5) # log returns histogram
fitted_dexp = stats.laplace.pdf(bins, loc_dexp, scale_dexp) # generate theoretical DExp pdf
ax1.plot(bins, fitted_dexp, label='DExp PDF', color = 'r', lw=2.) # plot theoretical DExp pdf over histogram

# Fit DExp QQ Plot
fig = plt.figure()
qq_laplace = stats.probplot(stockLogRet, dist = 'laplace', sparams= (loc_dexp, scale_dexp), plot = plt, fit = True)
plt.title('DExp QQ Plot of ' + TICKER + ' Daily Log Return', size=15)
plt.ylabel('Sample quantiles')

#-------------------------Fit Generalized Error (GED) Distribution-------------------------
# Fit GED Distribution Curve
fig = plt.figure()
shape_ged, loc_ged, scale_ged = stats.gennorm.fit(stockLogRet) # shape, location, and scale estimates
ax1 = fig.add_subplot(111
                      , title=TICKER + " Daily Log Return with GED("
                          +str(round(loc_ged, 2))
                          +', '+str(round(scale_ged, 2))+"$^{2}$"
                          +', '+ str(round(shape_ged, 2))+") Fit"
                      , xlabel='Log Return'
                      , ylabel='Density')
_, bins, _= ax1.hist(stockLogRet, bins=50, density=1, alpha=0.5) # log returns histogram
fitted_ged = stats.gennorm.pdf(bins, shape_ged, loc_ged, scale_ged) # generate theoretical GED pdf
ax1.plot(bins, fitted_ged, label='GED PDF', color = 'r', lw=2.) # plot theoretical GED pdf over histogram

# Fit GED QQ Plot
fig = plt.figure()
qq_ged = stats.probplot(stockLogRet, dist = 'gennorm', sparams= (shape_ged, loc_ged, scale_ged), plot = plt, fit = True)
plt.title('GED QQ Plot of ' + TICKER + ' Daily Log Return', size=15)
plt.ylabel('Sample quantiles')

#-------------------------Perato (PD) Distribution-------------------------
# Fit PD Distribution Curve
fig = plt.figure()
threshold = np.quantile(stockLogRet, 0.9) # threshold to limit log returns
exceedances = stockLogRet[stockLogRet > threshold] # limit log returns beyond threshold
shape_pd, loc_pd, scale_pd  = stats.pareto.fit(exceedances) # shape, location, and scale estimates
ax1 = fig.add_subplot(111
                      , title=TICKER + " Daily Log Return with PD("
                          +str(round(loc_pd, 2))
                          +', '+str(round(shape_pd, 2))
                          +', '+str(round(scale_pd, 2))+") Fit"
                      , xlabel='Log Return'
                      , ylabel='Density')
_, bins, _= ax1.hist(exceedances , bins=50, density=1, alpha=0.5) # log returns histogram
fitted_pd = stats.pareto.pdf(bins, shape_pd, loc_pd, scale_pd) # generate theoretical PD pdf
ax1.plot(bins, fitted_pd, label='PD PDF', color = 'r', lw=2.) # plot theoretical PD pdf over histogram

# Fit PD QQ Plot
fig = plt.figure()
qq_pd = stats.probplot(exceedances, dist = 'pareto', sparams= (shape_pd, loc_pd, scale_pd), plot = plt, fit = True)
plt.title('PD QQ Plot of ' + TICKER + ' Daily Log Return', size=15)
plt.ylabel('Sample quantiles')

#-------------------------Fit Generalized Perato (GPD) Distribution-------------------------
# Fit GPD Distribution Curve
fig = plt.figure()
shape_gpd, loc_gpd, scale_gpd  = stats.genpareto.fit(exceedances) # shape, location, and scale estimates
ax1 = fig.add_subplot(111
                      , title=TICKER + " Daily Log Return with GPD("
                          +str(round(loc_gpd, 2))
                          +', '+str(round(shape_gpd, 2))
                          +', '+str(round(scale_gpd, 2))+") Fit"
                      , xlabel='Log Return'
                      , ylabel='Density')
_, bins, _= ax1.hist(exceedances , bins=50, density=1, alpha=0.5) # log returns histogram
fitted_gpd = stats.genpareto.pdf(bins, shape_gpd, loc_gpd, scale_gpd ) # generate theoretical GPD pdf
ax1.plot(bins, fitted_gpd, label='GPD PDF', color = 'r', lw=2.) # plot theoretical GPD pdf over histogram

# Fit GPD QQ Plot
fig = plt.figure()
qq_gpd = stats.probplot(exceedances, dist = 'genpareto', sparams= (shape_gpd, loc_gpd, scale_gpd), plot = plt, fit = True)
plt.title('GPD QQ Plot of ' + TICKER + ' Daily Log Return', size=15)
plt.ylabel('Sample quantiles')

#-------------------------Distribution Selection-------------------------
from fitter import Fitter
# Declare distributions to fit
f1 = Fitter(stockLogRet,
           distributions = ["norm"
                          , "t"
                          , "laplace"
                          , "gennorm"])
f1.fit() # fit distributions
sum1 = f1.summary(plot=False) # store distribution metrics
# Declare tail distributions to fit
f2 = Fitter(exceedances,
           distributions = ["pareto"
                            , "genpareto"])
f2.fit() # fit tail distributions
sum2 = f2.summary(plot=False) # store tail distribution metrics
distr_performance = sum1.append(sum2, ignore_index = False)[['sumsquare_error', 'aic', 'bic']] # combine two summary tables
distr_performance = distr_performance.sort_values(by=['sumsquare_error']) # sort sumsquare serror in ascending order
distr_performance # output sorted summary tables

#-------------------------Value-at-Risk (VaR)-------------------------
# Calculating 1%, 5%, 10% quantiles
quantile_1 = stats.t.ppf(0.01, shape_t, loc_t, scale_t) # 1%
quantile_5 = stats.t.ppf(0.05, shape_t, loc_t, scale_t) # 5%
quantile_10 = stats.t.ppf(0.1, shape_t, loc_t, scale_t) # 10%

# Fit Student-t Distribution Curve
fig = plt.figure()
shape_t, loc_t, scale_t = stats.t.fit(stockLogRet) # shape, location, and scale estimates
ax1 = fig.add_subplot(111
                      , title=TICKER + " Daily Log Return with $t_{"
                          +str(round(shape_t, 2))+"}$"
                          +"("+str(round(loc_t, 2))
                          +', '+ str(round(scale_t, 2))+"$^{2}$) Fit"
                      , xlabel='Log Return'
                      , ylabel='Density')
_, bins, _= ax1.hist(stockLogRet, bins=50, density=1, alpha=0.5) # log returns histogram
fitted_t = stats.t.pdf(bins, shape_t, loc_t, scale_t) # generate theoretical student-t pdf
ax1.plot(bins, fitted_t, label='Student-t PDF', color = 'r', lw=2.) # plot theoretical student-t pdf over histogram
# Plotting rVaR at 1%, 5%, 10% significance levels
ax1.axvline(quantile_1, color='red', linewidth=1, label='1% Quantile') # 1% cutoff
ax1.axvline(quantile_5, color='blue', linewidth=1, label='5% Quantile') # 5% cutoff
ax1.axvline(quantile_10, color='green', linewidth=1, label='10% Quantile') # 10% cutoff
ax1.legend()

# Calculating rVar at 1%, 5%, 10% significance levels
rVaR_1 = -(np.exp(quantile_1)-1) # 1% rVaR
rVaR_5 = -(np.exp(quantile_5)-1) # 5% rVaR
rVaR_10 = -(np.exp(quantile_10)-1) # 10% rVaR

# Creating a risk table
riskTable = pd.DataFrame({'Significance Level': ['1%', '5%', '10%']
                         , 'Quantile': [quantile_1, quantile_5, quantile_10]
                         , 'rVaR': [rVaR_1, rVaR_5, rVaR_10]})
riskTable

#-------------------------Expected Shortfall (ES)-------------------------
import random
random.seed(10) # to reproduce the same simulation next time

# Monte Carlo simulation to generate 10 million daily losses
simLoss = -(np.exp(stats.t.rvs(df=shape_t, loc=loc_t, scale=scale_t, size=10000000))-1)

# Calculating rES at 1%, 5%, 10% significance levels
rES_1 = np.mean(simLoss[simLoss>rVaR_1]) # 1% rES
rES_5 = np.mean(simLoss[simLoss>rVaR_5]) # 5% rES
rES_10 = np.mean(simLoss[simLoss>rVaR_10]) # 10% rES

# Updating risk table to include rES
riskTable['rES'] = [rES_1, rES_5, rES_10]
riskTable
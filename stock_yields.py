# Script to calculate the profits and yields for each time period
import pandas as pd
import numpy as np

dave = "./Dave"
ingwe = "./Ingwe"
portfolio = ingwe

transactions = pd.read_csv(portfolio + '/input_data/transactions.csv', index_col='Date', parse_dates=True)
# tickers = transactions.Ticker.unique()
tickers = ['LON:CRST', 'NYSE:BRK-B']

for indx, company in enumerate(tickers):
    market_data = pd.read_csv(portfolio + '/stock_performance_daily/' + company.split(':')[1] + '.csv', index_col=False, parse_dates=['Date'])
    print(market_data.head())
    
    def previousValuesFunction(days, date, val):
        global market_data
        currentVal = market_data.loc[market_data['Date'] == date, val].values[0]
        previousDate = date - pd.to_timedelta(days, unit='d')
        returnVal = np.nan
        if (previousDate in market_data.values):
            previousVal = market_data.loc[market_data['Date'] == previousDate, val].values[0]
            returnVal = currentVal - previousVal
        return returnVal

    market_data = market_data.assign(Profit_wk = market_data['Date'].map(lambda x: previousValuesFunction(7, x, 'Profit')))
    market_data = market_data.assign(Yield_wk = market_data['Date'].map(lambda x: previousValuesFunction(7, x, 'Yield')))
    market_data = market_data.assign(Profit_mth = market_data['Date'].map(lambda x: previousValuesFunction(31, x, 'Profit')))
    market_data = market_data.assign(Yield_mth = market_data['Date'].map(lambda x: previousValuesFunction(31, x, 'Yield')))
    print(market_data)
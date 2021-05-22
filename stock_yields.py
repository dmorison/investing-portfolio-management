# Script to calculate the profits and yields for each time period
import pandas as pd
import numpy as np

dave = "./Dave"
ingwe = "./Ingwe"
portfolio = ingwe

transactions = pd.read_csv(portfolio + '/input_data/transactions.csv', index_col='Date', parse_dates=True)
# tickers = transactions.Ticker.unique()
tickers = ['LON:CRST', 'NYSE:BRK-B']

summary_df = None

for indx, company in enumerate(tickers):
    df = pd.read_csv(portfolio + '/stock_performance_daily/' + company.split(':')[1] + '.csv', index_col=False, parse_dates=['Date'])
    print(df.head())
    print(df.tail())

    df = df.assign(Cost_diff = df['Cost'].diff())
    
    firstDate = df.iloc[0, 0]
    lastdayofyear = firstDate
    weekly_pl = True
    def timePeriodYieldsFunc(days, date, totalProfit):
        global df
        global firstDate
        global lastdayofyear
        global weekly_pl
        if (days == 0):
            if (date.year == firstDate.year):
                sinceDate = firstDate
                lastdayofyear = date
            else:
                if (date.year > lastdayofyear.year):
                    sinceDate = lastdayofyear
                    lastdayofyear = date
                else:
                    sinceDate = lastdayofyear
        else:
            sinceDate = date - pd.to_timedelta(days, unit='d')

        # performance fix needed
        if (days > 7):
            if (sinceDate not in df.values):
                sinceDate = date - pd.to_timedelta((days-1), unit='d')
                if (sinceDate not in df.values):
                    sinceDate = date - pd.to_timedelta((days-2), unit='d')
        
        returnVal = np.nan
        if (sinceDate in df.values):
            temp_df = df.loc[(df['Date'] >= sinceDate) & (df['Date'] <= date)]
            sum_id = temp_df['Cost_diff'].sum(skipna=True)
            previousTotalProfit = df.loc[df['Date'] == sinceDate, 'Profit'].values[0]
            profitDiff = totalProfit - previousTotalProfit
            previousMarketValue = df.loc[df['Date'] == sinceDate, 'Market_value'].values[0]
            if (weekly_pl == True):
                returnVal = profitDiff
            else:
                returnVal = (profitDiff / (previousMarketValue + sum_id)) * 100
        return returnVal

    df = df.assign(Weekly_profit = df.apply(lambda x: timePeriodYieldsFunc(7, x['Date'], x['Profit']), axis=1))
    weekly_pl = False
    df = df.assign(Weekly_yield = df.apply(lambda x: timePeriodYieldsFunc(7, x['Date'], x['Profit']), axis=1))
    df = df.assign(Monthly_yield = df.apply(lambda x: timePeriodYieldsFunc(31, x['Date'], x['Profit']), axis=1))
    df = df.assign(Annual_yield = df.apply(lambda x: timePeriodYieldsFunc(365, x['Date'], x['Profit']), axis=1))
    df = df.assign(ytd_yield = df.apply(lambda x: timePeriodYieldsFunc(0, x['Date'], x['Profit']), axis=1))
    
    df.set_index('Date', inplace=True)
    print(df.head())
    print(df.tail())
    # df.to_csv(portfolio + '/stock_performance_daily/' + company.split(':')[1] + '.csv', float_format='%.2f', encoding='utf-8')

    Company_value = transactions.loc[transactions['Ticker'] == company, 'Company'].iloc[0]
    Weekly_profit = df['Weekly_profit'].iloc[-1]
    Weekly_yield = df['Weekly_yield'].iloc[-1]
    Monthly_yield = df['Monthly_yield'].iloc[-1]
    Annual_yield = df['Annual_yield'].iloc[-1]
    ytd_yield = df['ytd_yield'].iloc[-1]

    stock_summary_df = df[['Weekly_profit', 'Weekly_yield', 'Monthly_yield', 'Annual_yield', 'ytd_yield']].tail(1)
    stock_summary_df.insert(loc=0, column='Company', value=Company_value)
    print(stock_summary_df)

    if indx == 0:
        summary_df = stock_summary_df.copy(deep=True)
    else:
        summary_df = summary_df.append(stock_summary_df)

    # performance_data = np.array([["Week_profit", Weekly_profit], ["Week", Weekly_yield], ["Month", Monthly_yield], ["Annual", Annual_yield], ["Year_to_date", ytd_yield]])
    # performance_df = pd.DataFrame(data=performance_data, columns=["Period", "Percent"])
    # print(performance_df)
    # performance_df.to_csv(portfolio + '/portfolio_performance/time_to_date_performance.csv', float_format='%.2f', encoding='utf-8')

print(summary_df)
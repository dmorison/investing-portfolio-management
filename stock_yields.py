# Script to calculate the profits and yields for each time period
import pandas as pd
import numpy as np

dave = "./Dave"
ingwe = "./Ingwe"
portfolio = dave

transactions = pd.read_csv(portfolio + '/input_data/transactions.csv', index_col='Date', parse_dates=True)
tickers = transactions.Ticker.unique()
# tickers = ['LON:CRST', 'NYSE:BRK-B']

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
    df.to_csv(portfolio + '/stock_performance_daily/' + company.split(':')[1] + '.csv', float_format='%.2f', encoding='utf-8')

    Company_name = transactions.loc[transactions['Ticker'] == company, 'Company'].iloc[0]
    Company_shares = transactions.loc[transactions['Ticker'] == company, 'Quantity'].sum()
    Cost_per_share = transactions.loc[transactions['Ticker'] == company, 'Cost_per_share_ave'].iloc[-1]
    company_transactions = transactions[transactions['Ticker'] == company]
    Count_trades = len(transactions[transactions['Ticker'] == company].index)

    stock_summary_df = df[['Close', 'Cost', 'Market_value', 'Profit', 'Yield', 'Weekly_profit', 'Weekly_yield', 'Monthly_yield', 'Annual_yield', 'ytd_yield']].tail(1)
    stock_summary_df.insert(loc=0, column='Company', value=Company_name)
    stock_summary_df.insert(loc=0, column='Ticker', value=company)
    stock_summary_df.insert(loc=3, column='Total_shares', value=Company_shares)
    stock_summary_df.insert(loc=4, column='Average_share_price', value=Cost_per_share)
    stock_summary_df['Number_of_trades'] = Count_trades
    print(stock_summary_df)

    if indx == 0:
        summary_df = stock_summary_df.copy(deep=True)
    else:
        summary_df = summary_df.append(stock_summary_df)

summary_cost = summary_df['Cost'].sum()
summary_value = summary_df['Market_value'].sum()
summary_profit = summary_value - summary_cost  # not in use
summary_yield = (summary_profit / summary_cost) * 100  # not in use
summary_df = summary_df.assign(Percent_of_portfolio = summary_df['Market_value'].map(lambda x: (x / summary_value) * 100))
summary_df = summary_df.assign(Percent_of_total_return = summary_df['Profit'].map(lambda x: ((x / summary_profit) * 100) if x > 0 else np.nan))

summary_df = summary_df.assign(symbol = summary_df['Ticker'].map(lambda x: x.split(':')[1]))
summary_df.reset_index(inplace=True)

print(summary_df)

dv_df = pd.read_csv(portfolio + '/portfolio_performance/company_dividend_payouts.csv', index_col='Date', parse_dates=True)

dv_totals = dv_df.groupby(dv_df.symbol, as_index=False).agg({'dividend':'sum'})

if portfolio == "./Ingwe":
    dv_totals['symbol'] = dv_totals['symbol'].map(lambda x: x.split(':')[1].split('.')[0])

print(dv_totals)

resultdf = pd.merge(summary_df, dv_totals, how="outer", on="symbol")
resultdf['dividend'].fillna(0, inplace=True)
resultdf = resultdf.assign(dividend_yield = resultdf.apply(lambda x: x['dividend'] / x['Cost'], axis=1))
resultdf = resultdf.assign(yield_inc_dividend = resultdf.apply(lambda x: (x['Profit'] + x['dividend']) / x['Cost'], axis=1))

types_df = pd.read_csv('./Dave/input_data/stock_types.csv')
types_df.drop(['Stock'], axis=1, inplace=True)
dfall = pd.merge(resultdf, types_df, how="outer", on="Ticker")

dfall.set_index('Date', inplace=True)
print(dfall)

dfall.to_csv(portfolio + '/portfolio_performance/summary_stock_performance_yields.csv', float_format='%.2f', encoding='utf-8')

print("================ stock_yields script COMPLETE ================") #PRINT------------PRINT--------------PRINT#
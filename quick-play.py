import pandas as pd
import numpy as np
# import yfinance as yf
import requests
from bs4 import BeautifulSoup

headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.164 Safari/537.36'}
url = 'https://uk.finance.yahoo.com/quote/MONY.L'
stock_url = 'https://query2.finance.yahoo.com/v10/finance/download/MONY.L?period1=1625097600&period2=1626912000&interval=1d&events=history&includeAdjustedClose=true'
response = requests.get(stock_url)
print(response.status_code)

# dv_df = pd.read_csv('./Dave/portfolio_performance/summary_stock_performance_yields.csv', index_col='Date', parse_dates=True)
# types_df = pd.read_csv('./Dave/input_data/stock_types.csv')
# df = pd.merge(dv_df, types_df, how="outer", on="Ticker")
# print(df.info())


# summary_df = pd.read_csv('./Ingwe/portfolio_performance/summary_stock_performance_yields-original.csv', index_col='Date', parse_dates=True)
# summary_df = summary_df.assign(symbol = summary_df['Ticker'].map(lambda x: x.split(':')[1]))
# summary_df.reset_index(inplace=True)
# print(summary_df)

# dv_df = pd.read_csv('./Ingwe/portfolio_performance/company_dividend_payouts.csv', index_col='Date', parse_dates=True)

# dv_totals = dv_df.groupby(dv_df.symbol, as_index=False).agg({'dividend':'sum'})
# dv_totals['symbol'] = dv_totals['symbol'].map(lambda x: x.split(':')[1].split('.')[0])
# print(dv_totals)

# resultdf = pd.merge(summary_df, dv_totals, how="outer", on="symbol")
# resultdf['dividend'].fillna(0, inplace=True)
# resultdf = resultdf.assign(dividend_yield = resultdf.apply(lambda x: x['dividend'] / x['Cost'], axis=1))

# resultdf.set_index('Date', inplace=True)

# print(resultdf)

# dfs = dfs.assign(symbol = dfs['Ticker'].map(lambda x: x.split(':')[1]))
# print(dfs)

# dftotals = df.groupby(df.symbol, as_index=False).agg({'dividend':'sum'})
# dftotals['symbol'] = dftotals['symbol'].map(lambda x: x.split(':')[1].split('.')[0])
# print(dftotals)

# dfr = pd.merge(dfs, dftotals, how="outer", on="symbol")
# print(dfr)
# dfr['dividend'].fillna(0, inplace=True)
# print(dfr)

# market_data = pd.read_csv('./Ingwe/stock_performance_daily/CRST.csv', index_col=False, parse_dates=['Date'])
# print(market_data.tail(10))
# df = market_data['Profit'].iloc[-1]
# print(df)

# def previousValuesFunction(days, date, val):
#     global market_data
#     print(days)
#     print(date)
#     print(val)

#     # currentVal = market_data[market_data['Date'] == date][val]
#     currentVal = market_data.loc[market_data['Date'] == date, val].values[0]
#     print(currentVal)
#     previousDate = date - pd.to_timedelta(days, unit='d')
#     print(previousDate)
#     # exists = previousDate in market_data.values
#     returnVal = np.nan
#     if (previousDate in market_data.values):
#         print("date exists")
#         previousVal = market_data.loc[market_data['Date'] == previousDate, val].values[0]
#         print(previousVal)
#         returnVal = currentVal - previousVal
    
#     print(returnVal)
#     return returnVal

# rowNum = 8
# result = previousValuesFunction(7, market_data.iloc[rowNum]['Date'], 'Profit')
# print(result)

# curryear = pd.datetime.now().year
# today = pd.datetime.now()
# print(today)
# first = today.replace(year=curryear)
# print(first)
# lastMonth = first - pd.to_timedelta(1, unit='d')
# print(lastMonth)

# df = pd.read_csv("./Ingwe/daily_unit_value.csv", index_col="Date")
# print(df)
# print(df.info())

# transactions = pd.read_csv('./Ingwe/input_data/transactions.csv', index_col='Date', parse_dates=True)
# print(transactions)
# transactions['Year'] = transactions.index.year
# transactions['Week'] = transactions.index.week
# transactions['year_week'] = (transactions.index.year).astype(str) + '_' + (transactions.index.week).astype(str)
# print(transactions)

# symbl = 'LON:ULVR'
# df = yf.download("ULVR.L", '2019-02-26')
# print(df)
# row1 = transactions.loc[transactions['Ticker'] == symbl, 'Company'].values[0]
# print(row1)

# companies = transactions.Ticker.unique()
# print(companies)

# print(transactions.head())
# init_date = transactions.iloc[0, 0]
# print(init_date)

### getting previous date x number days before:
# init_date = pd.to_datetime("2020-09-01")
# print(init_date)
# init_date_90 = init_date - pd.to_timedelta(93, unit='d')
# print(init_date_90)
# df = yf.download("SPLK", init_date_90)
# print(df.head())
# print(df.info())

# ts_Date_loc = df.index.get_loc(init_date)
# df = df.iloc[ts_Date_loc: , :]
# print(df.head())
# print(df.info())

# exchR = yf.download("GBPUSD=X", init_date)
# print(exchR.head())
# Exchange_rate = exchR[['Close']]
# Exchange_rate.columns = ["GBPUSD"]
# print(Exchange_rate.shape)
# print(Exchange_rate.head())

# ts_Date = "2018-09-14"
# date_loc = Exchange_rate.index.get_loc(ts_Date)
# print(date_loc)
# new_ex_df = Exchange_rate.iloc[date_loc: , :]
# print(new_ex_df.shape)
# print(new_ex_df.head())

# ftse100 = yf.download("^FTSE", initdate90)
# print(ftse100.head())
# ftse100 = ftse100[['Close']]
# print(ftse100.head())
# init_val = ftse100.iloc[0, 0]
# ftse100 = ftse100.assign(Percent = ftse100['Close'].map(lambda x: ((x - init_val) / init_val) * 100))
# print(ftse100.head(10))
# print(ftse100.tail(10))

# indices_df = None

# initdate = pd.to_datetime("2020-01-01")
# initdate90 = initdate - pd.to_timedelta(90, unit='d')

# index_names = ["SP500", "FTSE100", "FTSE250", "FTSE350"]
# index_symbls = ["^GSPC", "^FTSE", "^FTMC", "^FTAS"]
# for indx, symbl in enumerate(index_symbls):
#     df = yf.download(symbl, initdate90)
#     df = df[['Close']]
#     init_val = df.iloc[0, 0]
#     df = df.assign(Percent = df['Close'].map(lambda x: ((x - init_val) / init_val) * 100))
#     symbl_name = index_names[indx]
#     df.columns = [symbl_name + "_Close", symbl_name + "_Percent"]

#     if indx == 0:
#         indices_df = df
#     else:
#         indices_df = indices_df.join(df, how="outer")

# print(indices_df.head(10))
# print(indices_df.info())

# indices_percent_df = indices_df[['SP500_Percent', 'FTSE100_Percent', 'FTSE250_Percent', 'FTSE350_Percent']]
# print(indices_percent_df.head(10))
# print(indices_percent_df.info())

# sp500 = yf.download("^GSPC", "2020-01-01")
# print(sp500.head())
# print(sp500.info())

# ftse250 = yf.download("^FTMC", "2020-01-01")
# print(ftse250.head())
# print(ftse250.info())

# ftseAll = yf.download("^FTAS", "2020-01-01")
# print(ftseAll.head())
# print(ftseAll.info())
import pandas as pd
import yfinance as yf

transactions = pd.read_csv('transactions.csv')

# companies = transactions.Ticker.unique()
# print(companies)

# print(transactions.head())
# init_date = transactions.iloc[0, 0]
# print(init_date)

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

us = yf.download("SPLK", "2018-10-19")
print(us.head())
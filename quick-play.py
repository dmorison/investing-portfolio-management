import pandas as pd
import yfinance as yf

# df = pd.read_csv("./Ingwe/daily_unit_value.csv", index_col="Date")
# print(df)
# print(df.info())

# transactions = pd.read_csv('./Dave/input_data/transactions.csv')

# companies = transactions.Ticker.unique()
# print(companies)

# print(transactions.head())
# init_date = transactions.iloc[0, 0]
# print(init_date)

init_date = pd.to_datetime("2020-09-01")
print(init_date)
init_date_90 = init_date - pd.to_timedelta(93, unit='d')
print(init_date_90)
df = yf.download("SPLK", init_date_90)
print(df.head())
print(df.info())

ts_Date_loc = df.index.get_loc(init_date)
df = df.iloc[ts_Date_loc: , :]
print(df.head())
print(df.info())

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

# us = yf.download("SPLK", "2020-12-20")
# print(us)
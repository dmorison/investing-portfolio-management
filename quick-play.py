import pandas as pd
# import yfinance as yf

# df = pd.read_csv("./Ingwe/daily_unit_value.csv", index_col="Date")
# print(df)
# print(df.info())

transactions = pd.read_csv('./Ingwe/input_data/transactions.csv')

symbl = 'LON:LLOY'
row1 = transactions.loc[transactions['Ticker'] == symbl, 'Company'].values[0]
print(row1)

# companies = transactions.Ticker.unique()
# print(companies)

# print(transactions.head())
# init_date = transactions.iloc[0, 0]
# print(init_date)

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
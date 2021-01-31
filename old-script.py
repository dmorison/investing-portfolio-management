import yfinance as yf
import pandas as pd

transactions = pd.read_csv('transactions.csv')
# positions = pd.read_csv('positions.csv')

print(transactions.head())
# print(transactions.info())
# print(positions.head())
# print(positions.info())

# symbol = 'LLOY.L'
# start_date = '2018-02-16'
# end_date = '2020-12-01'
# df1 = yf.download(symbol, start_date)
# print(df[:10])
# print(df1.info())
# print(df.iloc[0:5, 1])
# print(df.loc['2019-01-04', 'Close'])
# df1_close = df1['Close']
# print(df1_close.head())

company = "LON:LLOY"

def market(x):
	if x.split(':')[0] == "LON":
		return "UK"
	else:
		return "US"

def ticker(x):
	if market(x) == "UK":
		return x.split(':')[1] + ".L"
	else:
		return x.split(':')[1]

company_transactions = transactions[transactions['Ticker'] == company]
print(company_transactions)

# get first transaction to retrieve market data
ts = company_transactions.iloc[0, :]
ts_Date = ts['Date']
ts_Ticker = ticker(company)

market_data = yf.download(ts_Ticker, ts_Date)
print(market_data.info())
df = market_data[['Close']]

# ts_Quantity = transaction['Quantity'] #ts
# def total_val_calc(x):
# 	if country == "UK":
# 		return round((x * ts_Quantity) / 100, 2)
# 	else:
# 		return round(x * ts_Quantity, 2)

# df = df.assign(Value = df['Close'].apply(total_val_calc))
# print(df.head())
# df = df.assign(Profit = df['Value'].apply(lambda x: x - transaction['Total_cost_ave'])) #ts
# print(df.head())

# # get next transaction
# transaction_x = transactions.iloc[1, :] # company_transactions
# print(transaction_x)
# transaction_x_date = transaction_x['Date']
# print(df.loc[transaction_x_date])
# df_x_loc = df.index.get_loc(transaction_x_date)
# print(df_x_loc)

# df_1 = df.iloc[:df_x_loc, :]
# df_2 = df.iloc[df_x_loc:, :]
# print(df_1.tail())
# print(df_2.head())

# ts_Quantity = ts_Quantity + transaction_x['Quantity']
# print(ts_Quantity)
# df_2 = df_2.assign(Value = df_2['Close'].apply(total_val_calc))
# df_2 = df_2.assign(Profit = df_2['Value'].apply(lambda x: x - transaction_x['Total_cost_ave']))
# print(df_2.head())

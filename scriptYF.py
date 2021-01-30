import yfinance as yf
import pandas as pd

transactions = pd.read_csv('transactions.csv')
# positions = pd.read_csv('positions.csv')

# print(transactions.head())
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

company_transactions = transactions[transactions['Ticker'] == company]
# print(company_transactions)

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


# get first transaction to retrieve market data
ts = company_transactions.iloc[0, :]
ts_Date = ts['Date']
ts_Ticker = ticker(company)
ts_Quantity = ts['Quantity']
ts_Total_cost_ave = ts['Total_cost_ave']

# market data only necessary for first transaction
market_data = yf.download(ts_Ticker, ts_Date)
print(market_data.info())
df = market_data[['Close']]
##################################################

def total_val_calc(x):
	if market(company) == "UK":
		return round((x * ts_Quantity) / 100, 2)
	else:
		return round(x * ts_Quantity, 2)

df = df.assign(Market_value = df['Close'].apply(total_val_calc))
df = df.assign(Profit = df['Market_value'].apply(lambda x: x - ts_Total_cost_ave))

print(company_transactions)
# get next transactions
def build_dataset(x):
	global df
	global ts_Quantity
	ts_x = company_transactions.iloc[x, :]
	ts_x_Date = ts_x['Date']
	ts_Quantity = ts_Quantity + ts_x['Quantity'] # reset initial ts_Quantity to use in function
	ts_x_Total_cost_ave = ts_x['Total_cost_ave']

	print(df.loc[ts_x_Date])
	df_x_loc = df.index.get_loc(ts_x_Date)
	print(df_x_loc)

	df_1 = df.iloc[:df_x_loc, :]
	df_2 = df.iloc[df_x_loc:, :]
	print(df_1.tail(3))
	print(df_2.head(3))

	df_2 = df_2.assign(Market_value = df_2['Close'].apply(total_val_calc))
	df_2 = df_2.assign(Profit = df_2['Market_value'].apply(lambda x: x - ts_x_Total_cost_ave))
	print(df_2.head(3))

	print(df.shape)
	print(df_1.shape)
	df = pd.concat([df_1, df_2])
	print(df.shape)

build_dataset(1)
build_dataset(2)
print(df.info())
print(df['Market_value'].describe())

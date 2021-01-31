import yfinance as yf
import pandas as pd

transactions = pd.read_csv('transactions.csv')

company = "LON:HSTN"

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

df = df.assign(Market_value = df['Close'].map(total_val_calc))
df = df.assign(Cost = ts_Total_cost_ave)
df = df.assign(Profit = df['Market_value'].map(lambda x: round(x - ts_Total_cost_ave, 2)))
df = df.assign(Yield = df['Profit'].map(lambda x: round((x/ts_Total_cost_ave)*100,1)))

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
	
	df_2 = df_2.assign(Market_value = df_2['Close'].map(total_val_calc))
	df_2 = df_2.assign(Cost = ts_x_Total_cost_ave)
	df_2 = df_2.assign(Profit = df_2['Market_value'].map(lambda x: round(x - ts_x_Total_cost_ave,2)))
	df_2 = df_2.assign(Yield = df_2['Profit'].map(lambda x: round((x/ts_x_Total_cost_ave)*100,1)))
	print(df_2.head(3))

	print(df.shape)
	print(df_1.shape)
	df = pd.concat([df_1, df_2])
	print(df.shape)

if len(company_transactions.index) > 1:
	for x in range(1, len(company_transactions.index)):
		print("**************************")
		print(x)
		build_dataset(x)

print(df.info())
print(df['Yield'].describe())

df.to_csv('./company_datasets/' + company.split(':')[1] + '.csv', encoding='utf-8')

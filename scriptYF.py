import yfinance as yf
import pandas as pd

transactions = pd.read_csv('transactions.csv')

company_transactions = None
ts_Quantity = None
df = None
pf = None
company = None

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

def total_val_calc(x):
	if market(company) == "UK":
		return round((x * ts_Quantity) / 100, 2)
	else:
		return round(x * ts_Quantity, 2)

def get_company_data(xyz):
	global company_transactions
	global ts_Quantity
	global df
	global company
	company = xyz
	company_transactions = transactions[transactions['Ticker'] == company]
	# get first transaction to retrieve market data
	ts = company_transactions.iloc[0, :]
	ts_Date = ts['Date']
	ts_Ticker = ticker(company)
	ts_Quantity = ts['Quantity']
	ts_Total_cost_ave = ts['Total_cost_ave']

	# market data only necessary for first transaction
	market_data = yf.download(ts_Ticker, ts_Date)
	print(market_data.info())
	if market_data.empty:
		exit(ts_Ticker + ": No data found, symbol may be delisted")
	else:
		df = market_data[['Close']]
	##################################################

	df = df.assign(Market_value = df['Close'].map(total_val_calc))
	df = df.assign(Cost = ts_Total_cost_ave)
	df = df.assign(Profit = df['Market_value'].map(lambda x: round(x - ts_Total_cost_ave, 2)))
	df = df.assign(Yield = df['Profit'].map(lambda x: round((x/ts_Total_cost_ave)*100,1)))

	print(company_transactions)

# get next transactions
def build_data(x):
	global df
	global ts_Quantity
	global company_transactions
	ts_x = company_transactions.iloc[x, :]
	ts_x_Date = ts_x['Date']
	ts_Quantity = ts_Quantity + ts_x['Quantity'] # reset initial ts_Quantity to use in function
	ts_x_Total_cost_ave = ts_x['Total_cost_ave']

	df_x_loc = df.index.get_loc(ts_x_Date)

	df_1 = df.iloc[:df_x_loc, :]
	df_2 = df.iloc[df_x_loc:, :]
	# print(df_1.tail(3))
	# print(df_2.head(3))
	
	df_2 = df_2.assign(Market_value = df_2['Close'].map(total_val_calc))
	df_2 = df_2.assign(Cost = ts_x_Total_cost_ave)
	df_2 = df_2.assign(Profit = df_2['Market_value'].map(lambda x: round(x - ts_x_Total_cost_ave,2)))
	df_2 = df_2.assign(Yield = df_2['Profit'].map(lambda x: round((x/ts_x_Total_cost_ave)*100,1)))
	# print(df_2.head(3))

	# print(df.shape)
	# print(df_1.shape)
	df = pd.concat([df_1, df_2])
	# print(df.shape)

def build_company_datasets():
	global company_transactions
	if len(company_transactions.index) > 1:
		for x in range(1, len(company_transactions.index)):
			print("**************************")
			print(x)
			build_data(x)

tickers = ["LON:LLOY", "LON:BBOX", "LON:MONY"]
for indx, symbl in enumerate(tickers):
	print(indx)
	print(symbl)
	global df
	global pf
	get_company_data(symbl)
	build_company_datasets()

	print(df.info())
	print(df.head())
	print(df.tail())

	# df.to_csv('./company_datasets/' + company.split(':')[1] + '.csv', encoding='utf-8')

	if indx == 0:
		pf = df[['Cost', 'Profit']]
		pf_cost_col_name = "Cost_" + symbl.split(':')[1]
		pf_profit_col_name = "Profit_" + symbl.split(':')[1]
		pf.columns = [pf_cost_col_name, pf_profit_col_name]
	else:
		pf_1 = df[['Cost', 'Profit']]
		pf_1_rsuffix = "_" + symbl.split(':')[1]
		print(pf_1_rsuffix)
		pf = pf.join(pf_1, how="outer", rsuffix=pf_1_rsuffix)
		# pf = pf.assign(Cost = pf['Cost'].fillna(0) + pf_1['Cost'].fillna(0))
		# pf = pf.assign(Profit = pf['Profit'].fillna(0) + pf_1['Profit'].fillna(0))
	
	print(pf.head())
	print(pf.tail())
	print(pf.info())

# pf = pf.assign(Total_cost = pf['Cost_'])

# companies = ["LON:LLOY", "LON:BBOX"]
# for company in companies:
# 	get_data(company)

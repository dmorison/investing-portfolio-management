# transactions need to be in cronological order
# ensure transactions are numbers without commas
# US stocks need to have Cost_per_share_ave quoted in dollars but Total_cost_ave in pounds

import yfinance as yf
import pandas as pd
import numpy as np

dave = "./Dave"
ingwe = "./Ingwe"
portfolio = ingwe

transactions = pd.read_csv(portfolio + '/input_data/transactions.csv', parse_dates=['Date'])

company_transactions = None
ts_Quantity = None
df = None
company = None

init_date = transactions.iloc[0, 0]
# first get GBPUSD exchange rate data and assign it to dataframe
Exchange_rate_data = yf.download("GBPUSD=X", init_date)
Exchange_rate = Exchange_rate_data[['Close']]
Exchange_rate.columns = ["GBPUSD"]

# return which market
def market(x):
	if x.split(':')[0] == "LON":
		return "UK"
	else:
		return "US"

# return company ticker to get Yahoo Finance market data
def ticker(x):
	if market(x) == "UK":
		return x.split(':')[1] + ".L"
	else:
		return x.split(':')[1]

# calculate market value by multiplying x='close share price' by quantity of transaction shares
# divide UK stocks by 100 to return total value
def total_val_calc(x):
	return float((x * ts_Quantity) / 100)

# US stocks need to factor in exchange rate a='close share price' and b = 'GBPUSD' exchange rate
def us_total_val_calc(a, b):
	return float((a / b) * ts_Quantity)

# get company market data based on the first transaction and build the company dataframe for the first transaction up to todays date
def get_company_data(xyz):
	print("Company: " + xyz) #PRINT------------PRINT--------------PRINT#
	global company_transactions
	global ts_Quantity
	global df
	global company
	global Exchange_rate
	company = xyz  # set the company to the transaction symbol
	company_transactions = transactions[transactions['Ticker'] == company]  # get transactions for company from all transactions
	ts = company_transactions.iloc[0, :]  # get first transaction to retrieve market data from
	# set transaction values
	ts_Date = pd.to_datetime(ts['Date'])
	ts_Ticker = ticker(company) # get Yahoo Finance ticket/symbol for company
	ts_Quantity = ts['Quantity']
	ts_Total_cost_ave = ts['Total_cost_ave']
	ts_Cost_per_share_ave = ts['Cost_per_share_ave']

	print("First purchased: " + str(ts_Date)) #PRINT------------PRINT--------------PRINT#
	ts_Date_90 = ts_Date - pd.to_timedelta(90, unit='d')
	print("90 days before first purchased: " + str(ts_Date_90)) #PRINT------------PRINT--------------PRINT#
	#====================================================#
	# get market data only necessary for first transaction
	market_data = yf.download(ts_Ticker, ts_Date_90)
	print(market_data.head(3)) #PRINT------------PRINT--------------PRINT#
	print("Market data length: " + str(len(market_data.index))) #PRINT------------PRINT--------------PRINT#
	if market_data.empty:
		exit(ts_Ticker + ": No data found, symbol may be delisted")
	else:
		df = market_data[['Close']]  # create dataframe with only close values from market dataframe (index = Date)
	#====================================================#

	df.to_csv(portfolio + '/stock_market_trading/' + company.split(':')[1] + '.csv', encoding='utf-8')

	ts_Date_loc = df.index.get_loc(ts_Date)
	df = df.iloc[ts_Date_loc: , :]
	print(df.head(3)) #PRINT------------PRINT--------------PRINT#
	
	# seperate US stocks to calculate Market value and Cost to be able to factor in exchange rate
	if market(company) == "US":
		# get the location of the transaction date from which to rebase the exchange rate data from
		date_loc = Exchange_rate.index.get_loc(ts_Date)
		Ex_rate_df = Exchange_rate.iloc[date_loc: , :]
		init_ex_rate = Exchange_rate.loc[ts_Date, 'GBPUSD']
		Ex_rate_df = Ex_rate_df.assign(Percent = Ex_rate_df['GBPUSD'].map(lambda x: ((x - init_ex_rate) / init_ex_rate) * 100))
		# join exchange rate dataframe with market data
		df = df.join(Ex_rate_df, how="outer")
		df['Close'].replace('', np.nan, inplace=True)
		df['Close'] = df['Close'].fillna(method='ffill')
		
		df = df.assign(Market_value = df.apply(lambda x: us_total_val_calc(a = x['Close'], b = x['GBPUSD']), axis=1))
		df = df.assign(Cost = df['GBPUSD'].map(lambda x: (ts_Cost_per_share_ave * ts_Quantity) / x))
	else:
		df = df.assign(Market_value = df['Close'].map(total_val_calc))  # calculate market value and assign column to df
		df = df.assign(Cost = float(ts_Total_cost_ave))  # assign total cost to df column
	
	# need to check which is more accurate between two sets of calculations below
	df = df.assign(Profit = df['Market_value'] - df['Cost'])  # calculate profit based on market value subtract total cost for each day and assign column to df
	df = df.assign(Yield = (df['Profit'] / df['Cost']) * 100)  # calculate percentage yield based on profit for each day and assign column to df
	# insert the weekday names column
	week_day_col_values = df.index.weekday_name
	df.insert(loc=0, column='Weekday', value=week_day_col_values)

# using all following transactions, break up initial df into chuncks to rebase calculations for each transactions and concatenate them back together
def build_data(x):
	global df
	global company
	global ts_Quantity
	global company_transactions
	
	ts_x = company_transactions.iloc[x, :]  # get the next transaction
	# set transaction values
	ts_x_Date = ts_x['Date']
	print("Transaction date: " + str(ts_x_Date)) #PRINT------------PRINT--------------PRINT#
	ts_Quantity = ts_Quantity + ts_x['Quantity']  # reset the initial ts_Quantity to use in total_val_calc function
	ts_x_Total_cost_ave = ts_x['Total_cost_ave']
	ts_x_Cost_per_share_ave = ts_x['Cost_per_share_ave']

	df_x_loc = df.index.get_loc(ts_x_Date)  # get the location of the transaction from the initial df
	# split the current df by the transaction date
	df_1 = df.iloc[:df_x_loc, :]
	df_2 = df.iloc[df_x_loc:, :]
	
	# recalculate the the second dataframe based on the transaction
	if market(company) == "US":
		df_2 = df_2.assign(Market_value = df_2.apply(lambda x: us_total_val_calc(a = x['Close'], b = x['GBPUSD']), axis=1))
		# df_2 = df_2.assign(Cost = df['GBPUSD'].map(lambda x: round(ts_x_Total_cost_ave / x, 2)))
		df_2 = df_2.assign(Cost = df_2['GBPUSD'].map(lambda x: (ts_x_Cost_per_share_ave * ts_Quantity) / x))
	else:
		df_2 = df_2.assign(Market_value = df_2['Close'].map(total_val_calc))
		df_2 = df_2.assign(Cost = float(ts_x_Total_cost_ave))

	df_2 = df_2.assign(Profit = df_2['Market_value'] - df_2['Cost'])
	df_2 = df_2.assign(Yield = (df_2['Profit'] / df_2['Cost']) * 100)

	df = pd.concat([df_1, df_2])  # concatenate recalculated df_2 onto df_1 and set this newly created dataframe to the initial df

# loop through all compnays transactions to rebase the calculations for each transaction
def build_company_datasets():
	global company_transactions
	print("----------- TRANSACTIONS CALCULATIONS -----------") #PRINT------------PRINT--------------PRINT#
	print(company_transactions) #PRINT------------PRINT--------------PRINT#
	for x in range(1, len(company_transactions.index)):
		build_data(x)

# set the number of companies to use to 0
num_companies = 0
# initiate a variable that will become a dataframe made up of each companies cost and profit
pf = None
# list of companies to use
tickers = transactions.Ticker.unique()
# loop through each company in the tickers list
for indx, symbl in enumerate(tickers):
	print("---------------- Company " + str(num_companies + 1) + " of " + str(len(tickers)) + " ----------------") #PRINT------------PRINT--------------PRINT#
	get_company_data(symbl)  # get company market data and create initial df
	# only build data if there are more than one transaction
	if len(company_transactions.index) > 1:
		build_company_datasets()  # build the company dataset for the remaining transactions

	# create dataframe of weeks
	df_weeks = df.loc[df['Weekday'] == "Friday"]
	print(df_weeks.info()) #PRINT------------PRINT--------------PRINT#
	df_weeks.drop('Weekday', axis=1, inplace=True)  # remove the weekday column which would consist only of Friday
	print(df.info()) #PRINT------------PRINT--------------PRINT#
	# write company data to csv file
	df.to_csv(portfolio + '/stock_performance_daily/' + company.split(':')[1] + '.csv', float_format='%.2f', encoding='utf-8')
	df_weeks.to_csv(portfolio + '/stock_performance_weekly/' + company.split(':')[1] + '.csv', float_format='%.2f', encoding='utf-8')

	# create col names for pf dataframe with company suffix
	pf_cost_col_name = "Cost_" + symbl.split(':')[1]
	pf_profit_col_name = "Profit_" + symbl.split(':')[1]
	# get cost and profit columns from company df and join up pf dataframe with all companies
	# first company to set pf dataframe while the remaining companies get joined onto pf
	if indx == 0:
		init_ts_date = company_transactions['Date'].iloc[0]  # set the global initial transaction date for use further down on pf dataframe
		pf = df[['Cost', 'Profit']]
		pf.columns = [pf_cost_col_name, pf_profit_col_name]
		num_companies = 1
	else:
		pf_1 = df[['Cost', 'Profit']]
		pf_1.columns = [pf_cost_col_name, pf_profit_col_name]
		pf = pf.join(pf_1, how="outer")
		num_companies = num_companies + 1
	
	print("================ COMPANY COMPLETE ================") #PRINT------------PRINT--------------PRINT#

pf.fillna(method='ffill', inplace=True)
print(pf.info()) #PRINT------------PRINT--------------PRINT#

# initiate empty list variables for cost and column numbers
Cost_cols = []
Profit_cols = []
# build lists of cost and profit column numbers for pf
for x in range(0, num_companies):
	cost_col_nums = x * 2
	profit_col_nums = cost_col_nums + 1
	Cost_cols += [cost_col_nums]
	Profit_cols += [profit_col_nums]

# create all coasts and all profits dataframes for companies from pf dataframe
All_costs = pf.iloc[:, Cost_cols]
All_profits = pf.iloc[:, Profit_cols]

# sum the columns for all costs and all profits dataframes to get the totals
Total_cost = All_costs.sum(axis=1, skipna=True)
Total_profit = All_profits.sum(axis=1, skipna=True)
# calculate the percentage performance column for each day
Performance = (Total_profit/Total_cost)*100

# add the totals and performance columns to pf dataframe
pf['Total_invested'] = Total_cost
pf['Total_profit'] = Total_profit
pf['Performance'] = Performance

# create a dataframe of just the totals and performance
Totals_df = pf[['Total_invested', 'Total_profit', 'Performance']]
# insert the weekday names column
totals_week_days = Totals_df.index.weekday_name
Totals_df.insert(loc=0, column='Weekday', value=totals_week_days)

# get indices market data and create indices percentage df to join onto pf daily dataframe
indices_df = None
index_names = ["SP500", "FTSE100", "FTSE250", "FTSE350"]
index_symbls = ["^GSPC", "^FTSE", "^FTMC", "^FTAS"]
for indx, symbl in enumerate(index_symbls):
	print(symbl) #PRINT------------PRINT--------------PRINT#
	idf = yf.download(symbl, init_ts_date)  # use global initial transaction date
	idf = idf[['Close']]
	init_val = idf.iloc[0, 0]
	idf = idf.assign(Percent = idf['Close'].map(lambda x: ((x - init_val) / init_val) * 100))
	symbl_name = index_names[indx]
	idf.columns = [symbl_name + "_Close", symbl_name + "_Percent"]

	if indx == 0:
		indices_df = idf
	else:
		indices_df = indices_df.join(idf, how="outer")

print(indices_df.head()) #PRINT------------PRINT--------------PRINT#
print(indices_df.info()) #PRINT------------PRINT--------------PRINT#

indices_percent_df = indices_df[['SP500_Percent', 'FTSE100_Percent', 'FTSE250_Percent', 'FTSE350_Percent']]

Totals_df = Totals_df.join(indices_percent_df, how="outer")

# create dataframe of weeks
Totals_df_weeks = Totals_df.loc[Totals_df['Weekday'] == "Friday"]
Totals_df_weeks.drop('Weekday', axis=1, inplace=True)  # remove the weekday column which would consist only of Friday

print(Totals_df.head())
print(Totals_df.tail())
print(Totals_df.info())
print(Totals_df_weeks.head())
print(Totals_df_weeks.tail())
print(Totals_df_weeks.info())
# write performance dataframe with total cost and profit to csv
Totals_df.to_csv(portfolio + '/portfolio_performance/daily_portfolio_performance.csv', float_format='%.2f', encoding='utf-8')
Totals_df_weeks.to_csv(portfolio + '/portfolio_performance/weekly_portfolio_performance.csv', float_format='%.2f', encoding='utf-8')
print("--------------- PORTFOLIO CALCULATIONS COMPLETE ---------------") #PRINT------------PRINT--------------PRINT#
# to try when writing to csv: date_format='%Y-%m-%d'
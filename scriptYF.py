# transactions need to be in cronological order
# ensure transactions are numbers without commas
# US stocks need to have Cost_per_share_ave quoted in dollars but Total_cost_ave in pounds

import yfinance as yf
import pandas as pd
import numpy as np

dave = "./Dave"
ingwe = "./Ingwe"
portfolio = ingwe
offline = True

transactions = pd.read_csv(portfolio + '/input_data/transactions.csv', parse_dates=['Date'])

company_transactions = None
ts_Quantity = None
df = None
company = None
company_ticker = None

init_date = transactions.iloc[0, 0]
# first get GBPUSD exchange rate data and assign it to dataframe
if offline == True:
	Exchange_rate_data = pd.read_csv('./market_data/GBPUSD.csv', index_col='Date', parse_dates=True)
else:
	Exchange_rate_data = yf.download("GBPUSD=X", init_date)
	Exchange_rate_data.to_csv('./market_data/GBPUSD.csv', encoding='utf-8')

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
	global company_ticker
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
	#====================================================#
	# get market data only necessary for first transaction
	if offline == True:
		print("offline mode") #PRINT------------PRINT--------------PRINT#
		market_data = pd.read_csv('./market_data/' + company_ticker + '.csv', index_col='Date', parse_dates=True)
	else:
		print("fetching yf api data") #PRINT------------PRINT--------------PRINT#
		market_data = yf.download(ts_Ticker, ts_Date)
		market_data.to_csv('./market_data/' + company_ticker + '.csv', encoding='utf-8')
	
	print(market_data.head(3)) #PRINT------------PRINT--------------PRINT#
	print(market_data.tail(3)) #PRINT------------PRINT--------------PRINT#
	# print("Market data length: " + str(len(market_data.index))) #PRINT------------PRINT--------------PRINT#
	if market_data.empty:
		exit(ts_Ticker + ": No data found, symbol may be delisted")
	else:
		df = market_data[['Close']]  # create dataframe with only close values from market dataframe (index = Date)
	#====================================================#

	df.to_csv(portfolio + '/stock_market_trading/' + company_ticker + '.csv', encoding='utf-8') # rename folder to stockmarket_vs_trading
	
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
	year_week_col_values = (df.index.year).astype(str) + '_' + (df.index.week).astype(str)
	df.insert(loc=1, column='Year_week', value=year_week_col_values)
	print(df.tail()) #PRINT------------PRINT--------------PRINT#

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
# tickers = ['LON:CRST', 'NYSE:BRK-B']
# loop through each company in the tickers list
for indx, symbl in enumerate(tickers):
	print("---------------- Company " + str(num_companies + 1) + " of " + str(len(tickers)) + " ----------------") #PRINT------------PRINT--------------PRINT#
	company_name = transactions.loc[transactions['Ticker'] == symbl, 'Company'].values[0]
	company_ticker = symbl.split(':')[1]
	get_company_data(symbl)  # get company market data and create initial df
	# only build data if there are more than one transaction
	if len(company_transactions.index) > 1:
		build_company_datasets()  # build the company dataset for the remaining transactions

	# create dataframe of weeks
	df_weeks = df.groupby(df['Year_week'], as_index=False).tail(1)
	df_weeks.insert(loc=0, column='Company', value=company_name)  # insert the company name into the weekly data

	# write company data to csv file
	df.to_csv(portfolio + '/stock_performance_daily/' + company_ticker + '.csv', float_format='%.2f', encoding='utf-8')
	df_weeks.to_csv(portfolio + '/stock_performance_weekly/' + company_ticker + '.csv', float_format='%.2f', encoding='utf-8')

	# create col names for pf dataframe with company suffix
	pf_cost_col_name = "Cost_" + company_ticker
	pf_profit_col_name = "Profit_" + company_ticker
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

# now all companies added to pf dataframe calculate totals
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

# calculate to to dates performances
Totals_df = Totals_df.assign(Market_value = Totals_df['Total_invested'] + Totals_df['Total_profit'])
Totals_df = Totals_df.assign(Invested_diff = Totals_df['Total_invested'].diff())
Totals_df.reset_index(inplace=True)
Totals_df.set_index('Date', drop=False, inplace=True)

firstDate = Totals_df.iloc[0, 0]
lastdayofyear = firstDate
def timePeriodYieldsFunc(days, date, totalProfit):
	global Totals_df
	global firstDate
	global lastdayofyear
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
		if (sinceDate not in Totals_df.values):
			sinceDate = date - pd.to_timedelta((days-1), unit='d')
			if (sinceDate not in Totals_df.values):
				sinceDate = date - pd.to_timedelta((days-2), unit='d')
	
	returnVal = np.nan
	if (sinceDate in Totals_df.values):
		temp_df = Totals_df.loc[(Totals_df['Date'] >= sinceDate) & (Totals_df['Date'] <= date)]
		sum_id = temp_df['Invested_diff'].sum(skipna=True)
		previousTotalProfit = Totals_df.loc[Totals_df['Date'] == sinceDate, 'Total_profit'].values[0]
		profitDiff = totalProfit - previousTotalProfit
		previousMarketValue = Totals_df.loc[Totals_df['Date'] == sinceDate, 'Market_value'].values[0]
		returnVal = (profitDiff / (previousMarketValue + sum_id)) * 100
	return returnVal

Totals_df = Totals_df.assign(Weekly_yield = Totals_df.apply(lambda x: timePeriodYieldsFunc(7, x['Date'], x['Total_profit']), axis=1))
Totals_df = Totals_df.assign(Monthly_yield = Totals_df.apply(lambda x: timePeriodYieldsFunc(31, x['Date'], x['Total_profit']), axis=1))
Totals_df = Totals_df.assign(Annual_yield = Totals_df.apply(lambda x: timePeriodYieldsFunc(365, x['Date'], x['Total_profit']), axis=1))
Totals_df = Totals_df.assign(ytd_yield = Totals_df.apply(lambda x: timePeriodYieldsFunc(0, x['Date'], x['Total_profit']), axis=1))
Totals_df.drop(['Date'], axis=1, inplace=True)
print(Totals_df)
Totals_df.to_csv(portfolio + '/portfolio_performance/daily_portfolio_performance_yields.csv', float_format='%.2f', encoding='utf-8')

Weekly_yield = Totals_df['Weekly_yield'].iloc[-1]
Monthly_yield = Totals_df['Monthly_yield'].iloc[-1]
Annual_yield = Totals_df['Annual_yield'].iloc[-1]
ytd_yield = Totals_df['ytd_yield'].iloc[-1]

performance_data = np.array([["Week", Weekly_yield], ["Month", Monthly_yield], ["Annual", Annual_yield], ["Year_to_date", ytd_yield]])
performance_df = pd.DataFrame(data=performance_data, columns=["Period", "Percent"])
print(performance_df)
performance_df.to_csv(portfolio + '/portfolio_performance/summary_portfolio_performance_yields.csv', float_format='%.2f', encoding='utf-8')

# create Year_week column values and insert them into Totals_df
totals_year_week_col_values = (Totals_df.index.year).astype(str) + '_' + (Totals_df.index.week).astype(str)
Totals_df.insert(loc=1, column='Year_week', value=totals_year_week_col_values)
# set a Date column to be later reset as the index column
Totals_df = Totals_df.assign(Date = Totals_df.index)
# create the Totals_weeks_df
Totals_weeks_df = Totals_df.groupby(Totals_df['Year_week']).tail(1)

# get indices market data and create indices percentage df to join onto pf daily dataframe
indices_df = None
index_names = ["SP500", "FTSE100", "FTSE250", "FTSE350"]
index_symbls = ["^GSPC", "^FTSE", "^FTMC", "^FTAS"]
for indx, symbl in enumerate(index_symbls):
	print(symbl) #PRINT------------PRINT--------------PRINT#
	symbl_name = index_names[indx]
	if offline == True:
		idf = pd.read_csv('./market_data/' + symbl_name + '.csv', index_col='Date', parse_dates=True)
	else:
		idf = yf.download(symbl, init_ts_date)  # use global initial transaction date
		idf.to_csv('./market_data/' + symbl_name + '.csv', encoding='utf-8')
	
	idf = idf[['Close']]
	init_val = idf.iloc[0, 0]
	idf = idf.assign(Percent = idf['Close'].map(lambda x: ((x - init_val) / init_val) * 100))
	idf.columns = [symbl_name + "_Close", symbl_name + "_Percent"]

	if indx == 0:
		indices_df = idf
	else:
		indices_df = indices_df.join(idf, how="outer")

# print(indices_df.head()) #PRINT------------PRINT--------------PRINT#
# print(indices_df.info()) #PRINT------------PRINT--------------PRINT#

indices_percent_df = indices_df[['SP500_Percent', 'FTSE100_Percent', 'FTSE250_Percent', 'FTSE350_Percent']]
indices_percent_df.fillna(method='ffill', inplace=True)
# create Year_week column values and insert them into indices_percent_df
indices_year_week_col_values = (indices_percent_df.index.year).astype(str) + '_' + (indices_percent_df.index.week).astype(str)
indices_percent_df.insert(loc=0, column='Year_week', value=indices_year_week_col_values)
# create the indices_percent_weeks_df
indices_percent_weeks_df = indices_percent_df.groupby(indices_percent_df['Year_week']).tail(1)

# merge the two weekly dataframes
Totals_df_weeks = pd.merge(Totals_weeks_df, indices_percent_weeks_df, on="Year_week")
# reset the index to the Date column values
Totals_df_weeks.set_index('Date', inplace=True)
Totals_df_weeks.drop(['Weekday'], axis=1, inplace=True)
print(Totals_df_weeks.head()) #PRINT------------PRINT--------------PRINT#

# remove the Date and Year_week columns before joining the two daily dataframes on the index/dates
Totals_df.drop('Date', axis=1, inplace=True)
indices_percent_df.drop('Year_week', axis=1, inplace=True)
Totals_df = Totals_df.join(indices_percent_df, how="outer")  # think about ffill indices values to fill in gaps
print(Totals_df.head()) #PRINT------------PRINT--------------PRINT#

print(Totals_df_weeks.info()) #PRINT------------PRINT--------------PRINT#
print(Totals_df.info()) #PRINT------------PRINT--------------PRINT#
# write performance dataframe with total cost and profit to csv
Totals_df.to_csv(portfolio + '/portfolio_performance/daily_portfolio_performance.csv', float_format='%.2f', encoding='utf-8')
Totals_df_weeks.to_csv(portfolio + '/portfolio_performance/weekly_portfolio_performance.csv', float_format='%.2f', encoding='utf-8')
print("--------------- PORTFOLIO CALCULATIONS COMPLETE ---------------") #PRINT------------PRINT--------------PRINT#
# to try when writing to csv: date_format='%Y-%m-%d'
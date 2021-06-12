# Script to create individual stock datasets of the stock market performance as a percent together with when and how much of the stock was purchased/(sold)
# All individual stocks datasets are combined to create one large expanded dataset
# Input data:
#  - /input_data/transactions.csv
#  - /stock_market_trading/<<stock>>
# Output data:
#  - /stock_market_trading/<<stock>>
#  - /portfolio_performance/all_companies_trading_performance.csv

import pandas as pd
import numpy as np

dave = "./Dave"
ingwe = "./Ingwe"
portfolio = ingwe

transactions = pd.read_csv(portfolio + '/input_data/transactions.csv', index_col='Date', parse_dates=True)
dividends = pd.read_csv(portfolio + '/portfolio_performance/company_dividend_payouts.csv', index_col='Date', parse_dates=True)

if portfolio == "./Ingwe":
    dividends['symbol'] = dividends['symbol'].map(lambda x: x.split(':')[1].split('.')[0])

print(dividends) #PRINT------------PRINT--------------PRINT#

tickers = transactions.Ticker.unique()
all_companies_weeks = None

for indx, company in enumerate(tickers):
    print("---------------- Company: " + company + " ----------------") #PRINT------------PRINT--------------PRINT#
    stock_symbol = company.split(':')[1]
    market_data = pd.read_csv(portfolio + '/stock_market_trading/' + stock_symbol + '.csv', index_col='Date', parse_dates=True)
    company_transactions = transactions[transactions['Ticker'] == company]  # get transactions for company from all transactions
    print(company_transactions) #PRINT------------PRINT--------------PRINT#
    company_dividends = dividends[dividends['symbol'] == stock_symbol]
    print(company_dividends) #PRINT------------PRINT--------------PRINT#
    company_dividends.drop('symbol', axis=1, inplace=True)

    init_date_close = market_data.iloc[0, 0]
    print(init_date_close) #PRINT------------PRINT--------------PRINT#
    market_data = market_data.assign(Percent = market_data['Close'].map(lambda x: ((x - init_date_close) / init_date_close) * 100))

    company_name = company_transactions['Company'].iloc[0]
    company_transactions = company_transactions[['Total_ts_cost']]
    df = market_data.join(company_transactions, how="outer")

    df = df.join(company_dividends, how="outer")
    print(df)

    df.insert(loc=0, column='Company', value=company_name)
    df = df.assign(Year_week = (df.index.year).astype(str) + '_' + (df.index.week).astype(str))
    df = df.assign(Week = df.index)
    df_weeks = df.groupby(df.Year_week).agg({'Company': lambda x: x.tail(1),
                                             'Week': lambda x: x.tail(1),
                                             'Close': lambda x: x.tail(1),
                                             'Percent': lambda x: x.tail(1),
                                             'Total_ts_cost':'sum',
                                             'dividend':'sum',
                                             'quantity':'sum',
                                             'price':'sum'})

    if indx == 0:
        all_companies_weeks = df_weeks.copy(deep=True)
    else:
        all_companies_weeks = all_companies_weeks.append(df_weeks)
    # df.fillna(0, inplace=True)

    df.drop('Year_week', axis=1, inplace=True)
    df.drop('Week', axis=1, inplace=True)
    df.to_csv(portfolio + '/stock_market_trading/' + stock_symbol + '.csv', float_format='%.2f', encoding='utf-8')

all_companies_weeks.replace(0, np.nan, inplace=True)
print(all_companies_weeks.info()) #PRINT------------PRINT--------------PRINT#
all_companies_weeks.to_csv(portfolio + '/portfolio_performance/all_companies_trading_performance.csv', float_format='%.2f', encoding='utf-8')

print("================ marketTradingScript COMPLETE ================") #PRINT------------PRINT--------------PRINT#
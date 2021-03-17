import pandas as pd

dave = "./Dave"
ingwe = "./Ingwe"
portfolio = ingwe

transactions = pd.read_csv(portfolio + '/input_data/transactions.csv', index_col='Date', parse_dates=True)
tickers = transactions.Ticker.unique()

for company in tickers:
    print("---------------- Company: " + company + " ----------------") #PRINT------------PRINT--------------PRINT#
    market_data = pd.read_csv(portfolio + './stock_market_trading/' + company.split(':')[1] + '.csv', index_col='Date', parse_dates=True)
    company_transactions = transactions[transactions['Ticker'] == company]  # get transactions for company from all transactions
    print(company_transactions) #PRINT------------PRINT--------------PRINT#

    init_date = market_data.iloc[0, 0]
    print(init_date) #PRINT------------PRINT--------------PRINT#
    market_data = market_data.assign(Percent = market_data['Close'].map(lambda x: ((x - init_date) / init_date) * 100))

    company_transactions = company_transactions[['Total_ts_cost']]
    df = market_data.join(company_transactions, how="outer")
    # df.fillna(0, inplace=True)
    print(df.info()) #PRINT------------PRINT--------------PRINT#

    df.to_csv(portfolio + './stock_market_trading/' + company.split(':')[1] + '.csv', float_format='%.2f', encoding='utf-8')

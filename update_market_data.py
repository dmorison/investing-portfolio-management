import pandas as pd

portfolios = ["Dave", "Ingwe"]
index_names = ["SP500", "FTSE100", "FTSE250", "FTSE350", "GBPUSD"]
arr = []

for indx in portfolios:
    transactions = pd.read_csv('./' + indx + '/input_data/transactions.csv', parse_dates=['Date'])
    tickers = transactions.Ticker.unique()
    for symbl in tickers:
        company_ticker = symbl.split(':')[1]
        arr.append(company_ticker)

for indx in index_names:
    arr.append(indx)

print(arr)

for stock in arr:
    market_data = pd.read_csv('./market_data/' + stock + '.csv', index_col='Date', parse_dates=True)
    last_date = market_data.index[-1]
    print(last_date)

    data_feed = pd.read_csv('./Scraper/data_feed/' + stock + '.csv', index_col='Date', parse_dates=True)
    last_date_loc = data_feed.index.get_loc(last_date)
    last_date_loc = last_date_loc + 1
    print(last_date_loc)

    latest_data = data_feed.iloc[last_date_loc: , :]
    updated_data = pd.concat([market_data, latest_data], sort=True)
    updated_data.to_csv('./market_data/' + stock + '.csv', encoding='utf-8')


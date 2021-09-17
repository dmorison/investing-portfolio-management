import pandas as pd

# insert list of stocks in the array below:
stockList = []

portfolios = ["Dave", "Ingwe"]
index_names = ["SP500", "FTSE100", "FTSE250", "FTSE350", "GBPUSD"]
arr = []

for indx in portfolios:
    transactions = pd.read_csv('./' + indx + '/input_data/transactions.csv', parse_dates=['Date'])
    tickers = transactions.Ticker.unique()
    for symbl in tickers:
        company_ticker = symbl.split(':')[1]
        arr.append(company_ticker)

# print(arr) #PRINT------------PRINT--------------PRINT#

arr2 = list(set(arr))  # remove duplicate stocks held by both portfolios
print(arr2) #PRINT------------PRINT--------------PRINT#

simpleStockList = [item.split('.')[0] for item in stockList]  # remove the ".L" from the stock list above

newStocks = list(set(arr2) - set(simpleStockList))  # find any new stocks from the transactions
print(len(newStocks)) #PRINT------------PRINT--------------PRINT#
if len(newStocks) > 0:
    print("=================================")
    print("EXITING SCRIPT - NEW STOCKS FOUND")
    print("First add these to stockList array and stocks array in stockList.js (including the '.L' for UK stocks)")
    print(newStocks) #PRINT------------PRINT--------------PRINT#
    print("Then copy them into newStocks array in the script below")
    print("Then go back and fetch the latest data first before re-running this script")
    exit()

print("There are no new stocks found")
print("If there were new stocks make sure they exist in the newStocks array below (WITHOUT '.L' for UK stocks) before continuing:")
newStocks = []
print(newStocks) #PRINT------------PRINT--------------PRINT#
reply = str(raw_input("Is the new stocks list correct AND you fetched the latest data (y/n)? ")).lower().strip()
if reply[0] == 'n':
    print("Please ensure the new stocks list is correct or that you have fetched the latest data before continuing!!!")
    exit()

if reply[0] == 'y':
    reply2 = str(raw_input("You are about to update the datasets, do you wish to continue (y/n)? ")).lower().strip()
    if reply2[0] == 'n':
        print("Exiting the script")
        exit()

# add the index and currency names to the array
for indx in index_names:
    arr2.append(indx)

for stock in arr2:
    # if its a new stock read the scraped data and copy into market data else update the market data with the scraped data
    if stock in newStocks:
        newData = pd.read_csv('./Scraper/data_feed/' + stock + '.csv', index_col='Date', parse_dates=True)
        newData.to_csv('./market_data/' + stock + '.csv', encoding='utf-8')
    else:
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

print("================ update_market_data script COMPLETE ================") #PRINT------------PRINT--------------PRINT#

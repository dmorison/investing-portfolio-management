import pandas as pd
import numpy as np

dave = "./Dave"
ingwe = "./Ingwe"
portfolio = dave

transactions = pd.read_csv(portfolio + '/input_data/allTransactions.csv', parse_dates=['Date'])
print(transactions.head())

stocks = transactions['Symbol'].dropna().unique()
print(stocks)

print(stocks[2])
df = transactions[(transactions['Symbol'] == stocks[2]) & (transactions['Transaction_type'] != "Dividend")]
print(df)

cost_array = np.array([])

for indx, item in enumerate(df):
    if(indx > 0):
        print(indx)
        df2 = df.iloc[0:indx,]
        cost_ave = round(np.average(df2['Price'], weights = df2['Quantity']), 2)
        print(cost_ave)
        cost_array = np.append(cost_array, [cost_ave])
        print(df2)
        print("============")

print(cost_array)

df['Cost_ave'] = cost_array
print(df)
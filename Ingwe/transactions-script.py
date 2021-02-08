import pandas as pd
import numpy as np

transactions = pd.read_csv('all_transactions.csv', index_col='date')
performance = pd.read_csv('daily_performance.csv', index_col='Date')

ts_df = transactions[['typeid', 'value', 'symbol']]
ts_df = ts_df.sort_index()
ts_df = ts_df.rename_axis('Date')

running_total = 0
def sum_cash(a, b):
    global running_total
    if a == 'buylong' or a == 'quarterlymanagementfee':
        running_total = running_total - b
    else:
        running_total = running_total + b
    return running_total

ts_df = ts_df.assign(cash_balance = ts_df.apply(lambda x: sum_cash(a = x['typeid'], b = x['value']), axis=1))

df_cash_balance = ts_df[['cash_balance']]
# print(df_cash_balance)
# print(df_cash_balance.shape)

df1 = df_cash_balance.groupby(df_cash_balance.index).tail(1)
# print(df1)
# print(df1.shape)

df = ts_df.join(performance, how='outer')
print(df)
df = df.join(df1, how='outer', rsuffix="_right")
print(df)

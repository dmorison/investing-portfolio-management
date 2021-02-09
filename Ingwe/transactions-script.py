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
# print(ts_df.head(10))
df_cash_balance = ts_df[['cash_balance']]
# print(df_cash_balance)
# print(df_cash_balance.shape)

df = df_cash_balance.groupby(df_cash_balance.index).tail(1)
print(df.head(10))
# print(df.shape)
print(performance.head(10))

df1 = performance.join(df, how='outer')
print(df1.head(10))

current_cash = 0
def calculate_cash(a, b):
    global current_cash
    profit_value = a

    if pd.isna(a):
        profit_value = 0

    if pd.notna(b):
        current_cash = b
        return profit_value + b
    else:
        return profit_value + current_cash

current_balance = 0
def calculate_running_balance(a):
    global current_balance
    if pd.notna(a):
        current_balance = a
        return a
    else:
        return current_balance

def calculate_unit_value(a, b):
    profit = 0
    if pd.notna(a):
        profit = a
    percentage = profit / b
    return np.round_(1 + percentage, decimals=4)

# df1 = df1.assign(Balance = df1.apply(lambda x: calculate_cash(a = x['Total_profit'], b = x['cash_balance']), axis=1))
df1 = df1.assign(Running_balance = df1['cash_balance'].map(calculate_running_balance))
df1 = df1.assign(Net_asset_value = df1['Total_cost'].fillna(0) + df1['Total_profit'].fillna(0) + df1['Running_balance'])
df1 = df1.assign(Unit_value = df1.apply(lambda x: calculate_unit_value(a = x['Total_profit'], b = x['Net_asset_value']), axis=1))
df1 = df1.assign(Unit_val_change = df1['Unit_value'].map(lambda x: np.round_(((x - 1) / 1) * 100, decimals=2)))
print(df1)

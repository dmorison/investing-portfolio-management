import pandas as pd
import numpy as np

transactions = pd.read_csv('./input_data/trading_transactions.csv', index_col='date', parse_dates=True)
performance = pd.read_csv('./portfolio_performance/daily_portfolio_performance.csv', index_col='Date', parse_dates=True)
print(transactions.info()) #PRINT------------PRINT--------------PRINT#
print(performance.info()) #PRINT------------PRINT--------------PRINT#

# transactions.index = pd.to_datetime(transactions.index)
ts_df = transactions[['typeid', 'value', 'symbol']]
ts_df = ts_df.sort_index()
ts_df = ts_df.rename_axis('Date')

# current_balance = 0
# def sum_cash(a, b):
#     global current_balance
#     if a == 'buylong' or a == 'quarterlymanagementfee':
#         current_balance = current_balance - b
#     else:
#         current_balance = current_balance + b
#     return current_balance

# ts_df = ts_df.assign(Cash_balance = ts_df.apply(lambda x: sum_cash(a = x['typeid'], b = x['value']), axis=1))
ts_df = ts_df.assign(Amount = np.where((ts_df['typeid'] == 'buylong') | (ts_df['typeid'] == 'quarterlymanagementfee'), ts_df['value'] * (-1), ts_df['value']))
ts_df = ts_df.assign(Cash_balance = ts_df['Amount'].cumsum())
print(ts_df.head(10)) #PRINT------------PRINT--------------PRINT#

unit_val = 1
total_units = 0
def calc_units_purchased(row, val):
    global unit_val
    global total_units
    units_purchased = row['unitpurchase'] / unit_val
    total_units = total_units + units_purchased
    unit_val = row['NAV'] / total_units
    if val == 'unit':
        return unit_val
    else:
        return units_purchased


# tsdf2 = ts_df.join(performance[['Total_invested', 'Total_profit']])
# tsdf2.fillna(method='ffill', inplace=True)
# tsdf2 = tsdf2.assign(Investment_value = tsdf2['Total_invested'].fillna(0) + tsdf2['Total_profit'].fillna(0))
# tsdf2 = tsdf2.assign(NAV = tsdf2['Cash_balance'] + tsdf2['Investment_value'])
# tsdf2 = tsdf2.assign(unitpurchase = np.where((tsdf2['typeid'] == 'unitpurchase') | (tsdf2['typeid'] == 'cardunitpurchase'), tsdf2['Amount'], 0))
# tsdf2 = tsdf2.assign(unit_val = tsdf2.apply(lambda x: calc_units_purchased(row = x, val = 'unit'), axis=1))
# unit_val = 1
# total_units = 0
# tsdf2 = tsdf2.assign(units_purchased = tsdf2.apply(lambda x: calc_units_purchased(row = x, val = 'purchased'), axis=1))
# tsdf2 = tsdf2.assign(units_cumsum = tsdf2['units_purchased'].cumsum())
# print(tsdf2)
# tsdf2.to_csv('units_by_member.csv')

# unit_val = 1
# total_units = 0
ts_df = ts_df.assign(unitpurchase = np.where((ts_df['typeid'] == 'unitpurchase') | (ts_df['typeid'] == 'cardunitpurchase'), ts_df['Amount'], 0))
ts_df.drop(['symbol', 'value', 'typeid'], axis=1, inplace=True)
# ts_df.drop(['value'], axis=1, inplace=True)
# ts_df.drop(['typeid'], axis=1, inplace=True)
print(ts_df) #PRINT------------PRINT--------------PRINT#

# df_cash_balance = tsdf2[['Cash_balance', 'unitpurchase', 'Amount']]
# df_cash_balance = df_cash_balance.assign(value = np.where((df_cash_balance['type_units'] == 'unitpurchase'), df_cash_balance['Amount'], 0))
# df_cash_balance = ts_df[['Cash_balance', 'Amount']]

df = ts_df.groupby(ts_df.index).agg({'unitpurchase':'sum', 'Amount':'sum', 'Cash_balance': lambda x: x.tail(1)})
# df = df_cash_balance.groupby(df_cash_balance.index).tail(1)
print(df.head(10)) #PRINT------------PRINT--------------PRINT#
df1 = performance.join(df, how='outer')
# performance_cols = ['Total_invested', 'Total_profit', 'Performance', 'Cash_balance]
# for col in ['Total_invested', 'Total_profit', 'Performance']:
#     df1[col].fillna(method='ffill', inplace=True)
df1['Total_invested'].fillna(method='ffill', inplace=True)
df1['Total_profit'].fillna(method='ffill', inplace=True)
df1['Cash_balance'].fillna(method='ffill', inplace=True)
df1['unitpurchase'].fillna(0, inplace=True)
df1 = df1.assign(Investment_value = df1['Total_invested'].fillna(0) + df1['Total_profit'].fillna(0))
df1 = df1.assign(NAV = df1['Cash_balance'] + df1['Investment_value'])
df1 = df1.assign(unit_val = df1.apply(lambda x: calc_units_purchased(row = x, val = 'unit'), axis=1))
unit_val = 1
total_units = 0
df1 = df1.assign(units_purchased = df1.apply(lambda x: calc_units_purchased(row = x, val = 'purchased'), axis=1))
df1 = df1.assign(units_cumsum = df1['units_purchased'].cumsum())
print(df1) #PRINT------------PRINT--------------PRINT#
# df1.to_csv('units_by_day_4.csv')


# running_balance = 0
# def calculate_running_balance(a):
#     global running_balance
#     if pd.notna(a):
#         running_balance = a
#         return a
#     else:
#         return running_balance

# performance_cols = ['Total_invested', 'Total_profit', 'Performance']
# for col in performance_cols:
#     df1[col] = df1[col].map(calculate_running_balance)
#     running_balance = 0

# def calculate_unit_value(a, b):
#     profit = 0
#     if pd.notna(a):
#         profit = a
#     percentage = profit / b
#     return np.round_(1 + percentage, decimals=4)

# df1 = df1.assign(Running_balance = df1['Cash_balance'].map(calculate_running_balance))
# df1 = df1.assign(Net_asset_value = df1['Total_invested'].fillna(0) + df1['Total_profit'].fillna(0) + df1['Running_balance'])
# df1 = df1.assign(Unit_value = df1.apply(lambda x: unit_val_calc(a = )))
# df1 = df1.assign(Unit_value = df1.apply(lambda x: calculate_unit_value(a = x['Total_profit'], b = x['Net_asset_value']), axis=1))
# df1 = df1.assign(Unit_val_change = df1['Unit_value'].map(lambda x: np.round_(((x - 1) / 1) * 100, decimals=2)))

# print(df1.head(10)) #PRINT------------PRINT--------------PRINT#
# print(df1.tail(10)) #PRINT------------PRINT--------------PRINT#
print(df1.info()) #PRINT------------PRINT--------------PRINT#
df1.to_csv('./portfolio_performance/daily_unit_values.csv', encoding='utf-8')

print(df1['Performance'].describe()) #PRINT------------PRINT--------------PRINT#
maxpf_daily = df1['Performance'].idxmax()
print(df1.loc[maxpf_daily]) #PRINT------------PRINT--------------PRINT#

df_weeks = df1.loc[df1['Weekday'] == "Friday"]
df_weeks.drop('Weekday', axis=1, inplace=True)  # remove the weekday column which would consist only of Friday
print(df_weeks.head(10)) #PRINT------------PRINT--------------PRINT#
print(df_weeks.tail(10)) #PRINT------------PRINT--------------PRINT#
print(df_weeks.info()) #PRINT------------PRINT--------------PRINT#
df_weeks.to_csv('./portfolio_performance/weekly_unit_values.csv', encoding='utf-8')

print(df_weeks['Performance'].describe()) #PRINT------------PRINT--------------PRINT#
maxpf_weekly = df_weeks['Performance'].idxmax()
print(df_weeks.loc[maxpf_weekly]) #PRINT------------PRINT--------------PRINT#
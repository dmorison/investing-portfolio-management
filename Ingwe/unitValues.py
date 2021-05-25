import pandas as pd
import numpy as np

transactions = pd.read_csv('./input_data/trading_transactions.csv', index_col='date', parse_dates=True)
performance = pd.read_csv('./portfolio_performance/daily_portfolio_performance.csv', index_col='Date', parse_dates=True)
# print(transactions.info()) #PRINT------------PRINT--------------PRINT#
# print(performance.info()) #PRINT------------PRINT--------------PRINT#

# transactions.index = pd.to_datetime(transactions.index)
ts_df = transactions[['typeid', 'value', 'symbol', 'quantity', 'price']]
ts_df = ts_df.sort_index()
ts_df = ts_df.rename_axis('Date')

ts_df = ts_df.assign(Amount = np.where((ts_df['typeid'] == 'buylong') | (ts_df['typeid'] == 'quarterlymanagementfee'), ts_df['value'] * (-1), ts_df['value']))
ts_df = ts_df.assign(Cash_balance = ts_df['Amount'].cumsum())
ts_df = ts_df.assign(Dividend = np.where(ts_df['typeid'] == 'dividend_dom', ts_df['value'], 0))
# print(ts_df.head(10)) #PRINT------------PRINT--------------PRINT#

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

ts_df = ts_df.assign(unitpurchase = np.where((ts_df['typeid'] == 'unitpurchase') | (ts_df['typeid'] == 'cardunitpurchase'), ts_df['Amount'], 0))
# Create data set for dividend calculations
dv_df = ts_df[['typeid', 'value', 'symbol', 'quantity', 'price']]
# print(dv_df)

ts_df.drop(['symbol', 'value', 'typeid', 'quantity', 'price'], axis=1, inplace=True)
# print(ts_df) #PRINT------------PRINT--------------PRINT#

df = ts_df.groupby(ts_df.index).agg({'unitpurchase':'sum', 'Amount':'sum', 'Cash_balance': lambda x: x.tail(1), 'Dividend':'sum'})
# df = df_cash_balance.groupby(df_cash_balance.index).tail(1)
print(df) #PRINT------------PRINT--------------PRINT#
df1 = performance.join(df, how='outer')

df1.update(df1[['Total_invested', 'Total_profit', 'Cash_balance']].fillna(method='ffill'))
df1.update(df1[['Dividend', 'unitpurchase']].fillna(0))
df1 = df1.assign(Investment_value = df1['Total_invested'].fillna(0) + df1['Total_profit'].fillna(0))
df1 = df1.assign(NAV = df1['Cash_balance'] + df1['Investment_value'])
df1 = df1.assign(unit_val = df1.apply(lambda x: calc_units_purchased(row = x, val = 'unit'), axis=1))
unit_val = 1
total_units = 0
df1 = df1.assign(units_purchased = df1.apply(lambda x: calc_units_purchased(row = x, val = 'purchased'), axis=1))
df1 = df1.assign(units_cumsum = df1['units_purchased'].cumsum())
df1.update(df1[['Year_week', 'Performance', 'SP500_Percent', 'FTSE100_Percent', 'FTSE250_Percent', 'FTSE350_Percent']].fillna(method='ffill'))
# print(df1) #PRINT------------PRINT--------------PRINT#

# print(df1.info()) #PRINT------------PRINT--------------PRINT#
# df1.to_csv('./portfolio_performance/daily_unit_values.csv', encoding='utf-8')

# print(df1['Performance'].describe()) #PRINT------------PRINT--------------PRINT#
# maxpf_daily = df1['Performance'].idxmax()
# print(df1.loc[maxpf_daily]) #PRINT------------PRINT--------------PRINT#

df1 = df1.assign(Week = df1.index)
df1.drop(['Total_invested', 'Total_profit', 'Market_value', 'Invested_diff', 'Weekly_yield', 'Monthly_yield', 'Annual_yield', 'ytd_yield', 'Amount', 'unitpurchase', 'Cash_balance', 'units_purchased', 'units_cumsum'], axis=1, inplace=True)
print(df1)
df_weeks = df1.groupby(df1.Year_week).agg({'Weekday': lambda x: x.tail(1),
                                           'Performance': lambda x: x.tail(1),
                                           'SP500_Percent': lambda x: x.tail(1),
                                           'FTSE100_Percent': lambda x: x.tail(1),
                                           'FTSE250_Percent': lambda x: x.tail(1),
                                           'FTSE350_Percent': lambda x: x.tail(1),
                                           'Dividend': 'sum',
                                           'Investment_value': lambda x: x.tail(1),
                                           'NAV': lambda x: x.tail(1),
                                           'unit_val': lambda x: x.tail(1),
                                           'Week': lambda x: x.tail(1)})
df_weeks.set_index('Week', inplace=True)
print(df_weeks)
# df_weeks = df1.loc[df1['Weekday'] == "Friday"]
# df_weeks.drop('Weekday', axis=1, inplace=True)  # remove the weekday column which would consist only of Friday
# print(df_weeks['Dividend']) #PRINT------------PRINT--------------PRINT#
# print(df_weeks.tail(10)) #PRINT------------PRINT--------------PRINT#
# print(df_weeks.info()) #PRINT------------PRINT--------------PRINT#
df_weeks.to_csv('./portfolio_performance/weekly_unit_values.csv', encoding='utf-8')

# print(df_weeks['Performance'].describe()) #PRINT------------PRINT--------------PRINT#
# maxpf_weekly = df_weeks['Performance'].idxmax()
# print(df_weeks.loc[maxpf_weekly]) #PRINT------------PRINT--------------PRINT#

# Dividend calculations
dv_df = dv_df.loc[dv_df['typeid'] == "dividend_dom"]
dv_df.drop('typeid', axis=1, inplace=True)
# print(dv_df)
# dv_df.to_csv('./portfolio_performance/company_dividend_payouts.csv', encoding='utf-8')

print("================ unitValues script COMPLETE ================") #PRINT------------PRINT--------------PRINT#
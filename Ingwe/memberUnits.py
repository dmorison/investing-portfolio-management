import pandas as pd
import numpy as np

unit_values = pd.read_csv('./daily_unit_values.csv', index_col='Date', parse_dates=True)
transactions = pd.read_csv('./input_data/member_transactions.csv', index_col='date', parse_dates=True)

unit_values = unit_values[['Unit_value']]

transactions = transactions.sort_index()
transactions = transactions.rename_axis('Date')
transactions.rename(columns={'units':'ttt_units', 'value':'cash_input'}, inplace=True)

df = transactions.join(unit_values)
# print(df[df['Unit_value'].isna()])

df.fillna(method='ffill', inplace=True)

df = df.assign(Units = df['cash_input']/df['Unit_value'])

df_1 = None
member_totals = pd.DataFrame(columns=['Name', 'Total_units', 'Total_cash_input'])
members = df.name.unique()
for indx, member in enumerate(members):
    member_transactions = df[df['name'] == member]
    member_transactions = member_transactions.assign(Cumsum_Units = member_transactions['Units'].cumsum())
    member_transactions = member_transactions.assign(Cumsum_Cash = member_transactions['cash_input'].cumsum())
    member_transactions = member_transactions.assign(Value = member_transactions['Unit_value'] * member_transactions['Cumsum_Units'])
    member_transactions = member_transactions.assign(Percent_value = ((member_transactions['Value'] - member_transactions['Cumsum_Cash']) / member_transactions['Cumsum_Cash']) * 100)
    
    if indx == 0:
        df_1 = member_transactions
    else:
        df_1 = df_1.append(member_transactions, sort=False)
    
    members_total_units = member_transactions['Units'].sum()
    members_total_input = member_transactions['cash_input'].sum()
    mfdata = pd.DataFrame({'Name': [member],
                           'Total_units': [members_total_units],
                           'Total_cash_input': [members_total_input]})
    member_totals = member_totals.append(mfdata, sort=False)

print(df_1.info())
df_1.to_csv('member_transactions.csv', float_format='%.2f', encoding='utf-8')

member_totals = member_totals.assign(Date = unit_values.index[-1])
member_totals = member_totals.assign(Unit_value = unit_values['Unit_value'].iloc[-1])
member_totals = member_totals.assign(Total_cash_value = member_totals['Total_units'] * member_totals['Unit_value'])
member_totals = member_totals.assign(Yield = ((member_totals['Total_cash_value'] - member_totals['Total_cash_input']) / member_totals['Total_cash_input']) * 100)

print(member_totals)
member_totals.to_csv('member_totals.csv', float_format='%.2f', encoding='utf-8')
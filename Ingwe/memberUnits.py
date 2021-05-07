import pandas as pd

unit_values = pd.read_csv('./portfolio_performance/daily_unit_values.csv', index_col='Date', parse_dates=True)
transactions = pd.read_csv('./input_data/member_transactions.csv', index_col='date', parse_dates=True)

# print(transactions.head(20)) #PRINT------------PRINT--------------PRINT#
print(unit_values.tail()) #PRINT------------PRINT--------------PRINT#
print(unit_values.iloc[-1,:]) #PRINT------------PRINT--------------PRINT#

calc_date = unit_values.index[-1]
calc_unit_val = unit_values['unit_val'].iloc[-1]
calc_total_units = unit_values['units_cumsum'].iloc[-1]
calc_cash_balance = unit_values['Cash_balance'].iloc[-1]
calc_investment_value = unit_values['Investment_value'].iloc[-1]
calc_nav = unit_values['NAV'].iloc[-1]

ttt_date = pd.to_datetime("2021-05-01")
ttt_unit_val = 1.2493
ttt_total_units = 19942.52
ttt_cash_balance = 1529.75
ttt_investment_value = 23383.87
ttt_nav = ttt_cash_balance + ttt_investment_value

unit_values = unit_values[['unit_val']]

transactions.drop(['account', 'typeid'], axis=1, inplace=True)
transactions = transactions.sort_index()
transactions = transactions.rename_axis('Date')
transactions.rename(columns={'units':'ttt_units', 'value':'cash_input'}, inplace=True)

df = transactions.join(unit_values)
# print(df[df['unit_val'].isna()]) #PRINT------------PRINT--------------PRINT#

df.fillna(method='ffill', inplace=True)
df = df.assign(Units = df['cash_input']/df['unit_val'])
# print(df.head(20)) #PRINT------------PRINT--------------PRINT#

df_1 = None
member_totals = pd.DataFrame(columns=['Name', 'Total_units', 'Total_cash_input'])
members = df.name.unique()
for indx, member in enumerate(members):
    member_transactions = df[df['name'] == member]
    member_transactions = member_transactions.assign(Cumsum_Units = member_transactions['Units'].cumsum())
    member_transactions = member_transactions.assign(Cumsum_Cash = member_transactions['cash_input'].cumsum())
    member_transactions = member_transactions.assign(Value = member_transactions['unit_val'] * member_transactions['Cumsum_Units'])
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

print(df_1.info()) #PRINT------------PRINT--------------PRINT#
df_1.to_csv('./portfolio_performance/member_transactions.csv', float_format='%.2f', encoding='utf-8')

member_totals = member_totals.assign(Date = unit_values.index[-1])
member_totals = member_totals.assign(Unit_value = unit_values['unit_val'].iloc[-1])
member_totals = member_totals.assign(Total_value = member_totals['Total_units'] * member_totals['Unit_value'])
member_totals = member_totals.assign(Yield = ((member_totals['Total_value'] - member_totals['Total_cash_input']) / member_totals['Total_cash_input']) * 100)
member_totals = member_totals.set_index('Name')

print(member_totals) #PRINT------------PRINT--------------PRINT#
memb_total_units = member_totals['Total_units'].sum()
memb_cash_input = member_totals['Total_cash_input'].sum()
memb_investment_value = member_totals['Total_value'].sum()
member_totals.to_csv('./portfolio_performance/member_totals.csv', float_format='%.2f', encoding='utf-8')

indx_col = ['unit_val', 'total_units', 'cash_balance', 'investment_value', 'nav']
ttt_values = [ttt_unit_val, ttt_total_units, ttt_cash_balance, ttt_investment_value, ttt_nav]
calc_values = [calc_unit_val, calc_total_units, calc_cash_balance, calc_investment_value, calc_nav]

ttt_vs_calc_data = {'ttt': ttt_values,
                    'calc': calc_values}
ttt_vs_calc_df = pd.DataFrame(ttt_vs_calc_data, index = indx_col)
ttt_vs_calc_df = ttt_vs_calc_df.assign(Difference = ((ttt_vs_calc_df['calc'] - ttt_vs_calc_df['ttt']) / ttt_vs_calc_df['ttt']) * 100)
print(ttt_vs_calc_df) #PRINT------------PRINT--------------PRINT#

# # get last weeks market value to print out for updating dashboard variable
# last_week = pd.read_csv('./portfolio_performance/ttt_vs_calculations.csv')
# last_week_market_value = last_week.iloc[3,1]
# print('Previous weeks market value: ' + str(last_week_market_value))
print('Current unit value: ' + str(calc_unit_val))

ttt_vs_calc_df.to_csv('./portfolio_performance/ttt_vs_calculations.csv', float_format='%.2f', encoding='utf-8')
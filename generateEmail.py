import pandas as pd

weekly = pd.read_csv('./Ingwe/portfolio_performance/summary_stock_performance_yields.csv', index_col="Company")
portfolio_summary = pd.read_csv('./Ingwe/portfolio_performance/summary_portfolio_performance_yields.csv')

df = weekly[['Weekly_profit', 'Weekly_yield', 'Market_value', 'Profit', 'Yield']]

wowProfit = df['Weekly_profit'].sum()
wowYield = round(portfolio_summary.loc[portfolio_summary['Period'] == 'Week', 'Percent'].values[0], 1)
totalProfit = round(df['Profit'].sum(), 2)
totalYield = round(portfolio_summary.loc[portfolio_summary['Period'] == 'Total', 'Percent'].values[0], 1)

df.columns = ['Weekly P/L &pound;', 'Weekly P/L %', 'Market value &pound;', 'Total P/L &pound;', 'Total P/L %']
print(df)

html = df.to_html(escape=False)
print(html)

print('Week on week profit/loss: ' + str(wowProfit))
print('Week on week yield: ' + str(wowYield))
print('Total profit/loss: ' + str(totalProfit))
print('Total yield: ' + str(totalYield))
import pandas as pd

weekly = pd.read_csv('./Ingwe/portfolio_performance/summary_stock_performance_yields.csv', index_col="Company")
portfolio_summary = pd.read_csv('./Ingwe/portfolio_performance/summary_portfolio_performance_yields.csv')

df = weekly[['Weekly_profit', 'Weekly_yield', 'Market_value', 'Profit', 'Yield']]

wowProfit = df['Weekly_profit'].sum()
wowYield = round(portfolio_summary.loc[portfolio_summary['Period'] == 'Week', 'Percent'].values[0], 1)
totalProfit = round(df['Profit'].sum(), 2)
totalYield = round(portfolio_summary.loc[portfolio_summary['Period'] == 'Total', 'Percent'].values[0], 1)
weekPositiveStocks = weekly[weekly['Weekly_profit'] > 0]['Ticker'].count()
weekNegativeStocks = weekly[weekly['Weekly_profit'] < 0]['Ticker'].count()
weekTopYieldStock = weekly['Weekly_yield'].idxmax()
weekBottomYieldStock = weekly['Weekly_yield'].idxmin()

df = df.round({'Weekly_yield': 1, 'Yield': 1})
df['Weekly_yield'] = df['Weekly_yield'].astype(str) + '%'
df['Yield'] = df['Yield'].astype(str) + '%'

df.columns = ['Weekly P/L &pound;', 'Weekly yield', 'Market value &pound;', 'Total P/L &pound;', 'Total yield']
print(df)

html = df.to_html(escape=False)
print(html)

print('Week on week profit/loss: ' + str(wowProfit))
print('Week on week yield: ' + str(wowYield))
print('Total profit/loss: ' + str(totalProfit))
print('Total yield: ' + str(totalYield))
print('Positive stocks this week: ' + str(weekPositiveStocks))
print('Negative stocks this week: ' + str(weekNegativeStocks))
print('This weeks top yield stock: ' + weekTopYieldStock)
print('This weeks top yield stock: ' + weekBottomYieldStock)
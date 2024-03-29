import pandas as pd

weekly = pd.read_csv('./Ingwe/portfolio_performance/summary_stock_performance_yields.csv', index_col="Company")
summary = pd.read_csv('./Ingwe/portfolio_performance/portfolio_summary.csv', index_col="Company")

weekly= weekly[['Weekly_profit', 'Weekly_yield']]
summary = summary[['Market_value', 'Profit', 'Yield']]

print(weekly)
print(summary)

df = weekly.join(summary)
df.columns = ['Weekly P/L &pound;', 'Weekly P/L %', 'Market value &pound;', 'Total P/L &pound;', 'Total P/L %']
print(df)

html = df.to_html(escape=False)
print(html)
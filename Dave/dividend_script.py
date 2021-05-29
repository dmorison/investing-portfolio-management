# -*- coding: utf-8 -*-

import pandas as pd
import numpy as np
import re as re

transactions = pd.read_csv('./input_data/trading_transactions.csv', index_col='Date', parse_dates=True)
performance = pd.read_csv('./portfolio_performance/daily_portfolio_performance.csv', index_col='Date', parse_dates=True)

df = transactions[['Symbol', 'Description', 'Credit']]
df = df.sort_index()

df = df[df['Description'].str.contains("Div ")]
print(df.head())

def find_number(text):
    num = re.findall(r'[0-9]+',text)
    return num[0]

df['quantity'] = df['Description'].apply(lambda x: find_number(x))
df['quantity'] = df['quantity'].astype(int)
df['Credit'] = df['Credit'].str.replace(',', '')
df['Credit'] = df['Credit'].str.replace('£', '')
df['Credit'] = df['Credit'].astype(float)
df['Symbol'] = df['Symbol'].str.replace('.', '')
df = df.assign(price = df['Credit'] / df['quantity'])

df.rename(columns={'Credit':'dividend', 'Symbol':'symbol'}, inplace=True)
df.drop('Description', axis=1, inplace=True)
print(df)
df.to_csv('./portfolio_performance/company_dividend_payouts.csv', encoding='utf-8')
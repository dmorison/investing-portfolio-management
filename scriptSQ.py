import pandas_datareader.data as api

stk = api.DataReader('PRU.UK', 'stooq')

print(stk[:10])
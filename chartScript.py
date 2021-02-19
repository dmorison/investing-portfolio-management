#%%
import pandas as pd
import matplotlib.pyplot as plt
import matplotlib as mpl
# mpl.use('agg')
import numpy as np

# import seaborn as sns
# sns.set(rc={'figure.figsize':(11, 4)})

daily_units = pd.read_csv("./Ingwe/daily_unit_values.csv", index_col=0, parse_dates=True)
# print(daily_units.head(3))
# print(daily_units.tail(3))
# print(daily_units.dtypes)
# print(daily_units.index)
print(daily_units.loc['2020-10-29'])

daily_units['Performance'].plot()
plt.show()
plt.savefig('Performance.png')
# %%

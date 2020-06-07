import plotly.figure_factory as ff

import matplotlib.pyplot as plt
import numpy as np
import pandas as pd

key_name = 'Alameda, California, US'

df_sample = pd.read_csv('../data/csejhudump/COVID-19/csse_covid_19_data/csse_covid_19_time_series/time_series_covid19_confirmed_US.csv', index_col="Combined_Key")

lastDays=10

alameda_row = df_sample.loc[key_name]
print(alameda_row.index[len(alameda_row)-lastDays:])

print(alameda_row.values[len(alameda_row)-lastDays:])



plt.figure(figsize=(28, 8))

plt.subplot(131)
plt.plot(alameda_row.index[len(alameda_row)-lastDays:], alameda_row.values[len(alameda_row)-lastDays:])

plt.show()


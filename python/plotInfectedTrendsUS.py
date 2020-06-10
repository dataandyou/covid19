# Plotting trends on infections 
# Author : Sandip Pal & 
# Start Date: 06/06/2020
# How to use this script: TBD



import plotly.figure_factory as ff

import matplotlib.pyplot as plt
import numpy as np
import pandas as pd

key_name = 'Shasta, California, US'

df_sample = pd.read_csv('../data/csejhudump/COVID-19/csse_covid_19_data/csse_covid_19_time_series/time_series_covid19_confirmed_US.csv', index_col="Combined_Key")


lastDays=20 # Trend for the last how many days

print(df_sample)

oneRow = df_sample.loc[key_name]
#Debug prints
print(oneRow.index[len(oneRow)-lastDays:])
print(oneRow.values[len(oneRow)-lastDays:])



plt.figure(figsize=(32, 8))

plt.plot(oneRow.index[len(oneRow)-lastDays:], oneRow.values[len(oneRow)-lastDays:], 'bo-')
plt.xlabel(f'Last {lastDays}')
plt.ylabel(key_name)

# zip joins x and y coordinates in pairs
for x,y in zip(oneRow.index[len(oneRow)-lastDays:],oneRow.values[len(oneRow)-lastDays:]):

    label = "{:.2f}".format(y)

    plt.annotate(label, # this is the text
                 (x,y), # this is the point to label
                 textcoords="offset points", # how to position the text
                 xytext=(0,10), # distance from text to points (x,y)
                 ha='center') # horizontal alignment can be left, right or center



plt.show()


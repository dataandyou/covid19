# Plotting trends on infections 
# Author : Sandip Pal & 
# Start Date: 06/06/2020
# How to use this script: TBD



import plotly.figure_factory as ff
import matplotlib.pyplot as plt
import numpy as np
import pandas as pd

import sys

key_name = 'Mono, California, US'

df_sample = pd.read_csv('../data/csejhudump/COVID-19/csse_covid_19_data/csse_covid_19_time_series/time_series_covid19_confirmed_US.csv', index_col="Combined_Key")


lastDays=60 # Trend for the last how many days


print(f"Arguments count: {len(sys.argv)}")
for i, arg in enumerate(sys.argv):
	print(f"Argument {i:>6}: {arg}")
	if(i == 1):
		key_name = sys.argv[i]
	if(i == 2):
		lastDays = int(sys.argv[i])


print(df_sample)

oneRow = df_sample.loc[key_name]
#Debug prints
print(oneRow.index[len(oneRow)-lastDays:])
print(oneRow.values[len(oneRow)-lastDays:])



plt.figure(figsize=(32, 8))

plt.bar(oneRow.index[len(oneRow)-lastDays:], oneRow.values[len(oneRow)-lastDays:], width=0.8
       , color = "#00FF00")
plt.xlabel(f'Infections Last {lastDays}')
plt.ylabel(key_name)

# zip joins x and y coordinates in pairs
for x,y in zip(oneRow.index[len(oneRow)-lastDays:],oneRow.values[len(oneRow)-lastDays:]):

    label = "{:.2f}".format(y)

    plt.annotate(label, # this is the text
                 (x,y), # this is the point to label
                 textcoords="offset points", # how to position the text
		 rotation="vertical",
		 color="#FF0000",
		 weight="bold",
                 xytext=(0,10), # distance from text to points (x,y)
                 ha='center') # horizontal alignment can be left, right or center



plt.show()


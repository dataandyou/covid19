# Plotting trends on infections 
# Author : Sandip Pal  
# Start Date: 06/06/2020
# How to use this script: TBD



import plotly.figure_factory as ff

import matplotlib.pyplot as plt
import matplotlib.pyplot as plt1
import numpy as np
import pandas as pd

key_name = 'China'


df_sample = pd.read_csv('../data/csejhudump/COVID-19/csse_covid_19_data/csse_covid_19_time_series/time_series_covid19_confirmed_global.csv', index_col="Country/Region")

lastDays=20 # Trend for the last how many days

#Debug prints
#print(df_sample)

oneRow = df_sample.loc[key_name]
#Debug prints
#print(oneRow.index[len(oneRow)-lastDays:])
#print(oneRow.values[len(oneRow)-lastDays:])
print(oneRow)

aggOneRow = oneRow.groupby('Country/Region').sum()


print("Debug: After Groupby Sum")
print(aggOneRow)

print(aggOneRow.index)


res = [aggOneRow.values[i + 1] - aggOneRow.values[i] for i in range(len(aggOneRow.values)-1)]

print("Debug: After subtraction")
print(res)



plt1.figure(figsize=(24, 8))
plt1.bar(aggOneRow.index[len(aggOneRow)-lastDays:], res[len(res)-lastDays:])
plt1.xlabel(f'Last {lastDays} days')
plt1.ylabel(key_name)

# zip joins x and y coordinates in pairs
for x,y in zip(aggOneRow.index[len(aggOneRow)-lastDays:],  res[len(res)-lastDays:]):

    label = "{:.2f}".format(y)

    plt1.annotate(label, # this is the text
                 (x,y), # this is the point to label
                 textcoords="offset points", # how to position the text
                 xytext=(0,10), # distance from text to points (x,y)
                 ha='center') # horizontal alignment can be left, right or center



plt1.show()


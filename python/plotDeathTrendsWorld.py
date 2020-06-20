# Plotting trends on infections 
# Author : Sandip Pal  
# Start Date: 06/06/2020
# How to use this script: TBD



import plotly.figure_factory as ff

import matplotlib.pyplot as plt
import matplotlib.pyplot as plt1
import numpy as np
import pandas as pd
import sys

key_name = 'India'


df_sample = pd.read_csv('../data/csejhudump/COVID-19/csse_covid_19_data/csse_covid_19_time_series/time_series_covid19_deaths_global.csv', index_col="Country/Region")

lastDays=20 # Trend for the last how many days

print(f"Arguments count: {len(sys.argv)}")
for i, arg in enumerate(sys.argv):
        print(f"Argument {i:>6}: {arg}")
        if(i == 1):
                key_name = sys.argv[i]
        if(i == 2):
                lastDays = int(sys.argv[i])


#Debug prints
#print(df_sample)

oneRow = df_sample.loc[key_name]

#Debug prints
print(oneRow.shape[0])
#print(oneRow.sum(axis='rows'))
#if oneRow.shape[0] > 1 :
#	oneRow = oneRow.sum(axis='rows')

print("After Row transform")
print(oneRow)

print(oneRow.index[len(oneRow)-lastDays:])
print(oneRow.values[len(oneRow)-lastDays:])

print(type(oneRow.values[len(oneRow) -1]) )

print("Now calculate diff from cumulative")
res = [oneRow.values[i + 1] - oneRow.values[i] for i in range(len(oneRow.values)-1)] 

plt.figure(figsize=(24, 8))
plt.subplot(131)
plt.plot(oneRow.index[len(oneRow)-lastDays:], oneRow.values[len(oneRow)-lastDays:], 'bo-')
plt.xlabel(f'Last {lastDays} days')
plt.ylabel(key_name)

# zip joins x and y coordinates in pairs
for x,y in zip(oneRow.index[len(oneRow)-lastDays:],oneRow.values[len(oneRow)-lastDays:]):

    label = "{:.2f}".format(y)

    plt.annotate(label, # this is the text
                 (x,y), # this is the point to label
                 textcoords="offset points", # how to position the text
                 xytext=(0,10), # distance from text to points (x,y)
                 ha='center') # horizontal alignment can be left, right or center




plt.subplot(132)
plt.bar(oneRow.index[len(oneRow)-lastDays:], res[len(res)-lastDays:])
plt.xlabel(f'Last {lastDays} days')
plt.ylabel(key_name)

# zip joins x and y coordinates in pairs
for x,y in zip(oneRow.index[len(oneRow)-lastDays:],  res[len(res)-lastDays:]):

    label = "{:.2f}".format(y)

    plt.annotate(label, # this is the text
                 (x,y), # this is the point to label
                 textcoords="offset points", # how to position the text
                 xytext=(0,10), # distance from text to points (x,y)
                 ha='center') # horizontal alignment can be left, right or center



plt.show()


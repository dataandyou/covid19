
import numpy as np
import pandas as pd


date_str = '6/10/20'

df_sample = pd.read_csv('../../data/csejhudump/COVID-19/csse_covid_19_data/csse_covid_19_time_series/time_series_covid19_deaths_US.csv')

df_sample.dropna(subset=['FIPS'], inplace=True)
df_sample.sort_values(by=[date_str], inplace=True)
population = df_sample['Population'].tolist()
values = df_sample[date_str].tolist()
fips = df_sample['FIPS'].tolist()
county_desc = df_sample['Combined_Key'].tolist()

#debug print
#print(df_sample)

total_deaths = sum(values)
print(f"Total Deaths = {total_deaths}")


print(df_sample.tail(10)[['Combined_Key', date_str]])



for i in range(1, 11):
	sumTopN = sum(values[-i*10:])
	print(f"deaths for top {i*10} =  {sumTopN} ")
	print(f"% death of Top {i*10} = {100*sumTopN/total_deaths}")

	





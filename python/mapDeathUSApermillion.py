import plotly.figure_factory as ff

import numpy as np
import pandas as pd

import sys

ccnum = "0" ;
print(f"Arguments count: {len(sys.argv)}")
for i, arg in enumerate(sys.argv):
	print(f"Argument {i:>6}: {arg}")
	if(i == 1):
		ccnum = sys.argv[i]


df_sample = pd.read_csv('../data/time_series_covid19_deaths_US.csv')

population = df_sample['Population'].tolist()
values = df_sample['6/3/20'].tolist()
fips = df_sample['FIPS'].tolist()

valpm = [i* 1000000 / j for i, j in zip(values, population)]

cs0 = ["#f7fbff","#ebf3fb","#deebf7","#d2e3f3","#c6dbef","#b3d2e9","#9ecae1",
              "#85bcdb","#6baed6","#57a0ce","#4292c6","#3082be","#2171b5","#1361a9",
              "#08519c","#0b4083","#08306b"]

cs1 = ["#f7fbff","#ebf3fb","#c6dbef","#b3d2e9",
              "#85bcdb","#4292c6","#3082be","#1361a9",
              "#08519c","#08306b"]
cs2 = ["#f7fbff",
              "#85bcdb","#1361a9",
              "#08306b"]
print(f"ccnum: {ccnum}")

if(ccnum == "0"):
	ccscl = cs0
elif(ccnum == "1"):
	ccscl = cs1
else:
	ccscl = cs2



print(f"len(ccscl):  {len(ccscl)}" )

endpts = list(np.linspace(1, 1000, len(ccscl) - 1))

fig = ff.create_choropleth(
    fips=fips, values=valpm , show_state_data=True,
    colorscale=ccscl, binning_endpoints=endpts,
    asp=2.9,
    paper_bgcolor='rgb(229,229,229)',
    title ='USA death numbers per million',
    show_hover=True, 
    legend_title='Deaths per million',
    county_outline={'color': 'rgb(224,224,224)', 'width': 0.5}
)
fig.layout.template = None
fig.show()

import plotly.figure_factory as ff

import numpy as np
import pandas as pd


date_str = '6/7/20'

df_sample = pd.read_csv('../data/csejhudump/COVID-19/csse_covid_19_data/csse_covid_19_time_series/time_series_covid19_deaths_US.csv')

df_sample.dropna(subset=['FIPS'], inplace=True)
population = df_sample['Population'].tolist()
values = df_sample[date_str].tolist()
fips = df_sample['FIPS'].tolist()


#colorscale = ["#f7fbff","#ebf3fb","#deebf7","#d2e3f3","#c6dbef","#b3d2e9","#9ecae1",
#              "#85bcdb","#6baed6","#57a0ce","#4292c6","#3082be","#2171b5","#1361a9",
#              "#08519c","#0b4083","#08306b"]

colorscale = ["#f7fbff","#c6dbef","#b3d2e9",
              "#85bcdb","#4292c6","#1361a9",
              "#08519c","#08306b"]
#colorscale = ["#f7fbff",
#              "#85bcdb","#1361a9",
#              "#08306b"]

endpts = list(np.linspace(1, 2000, len(colorscale) - 1))

fig = ff.create_choropleth(
    fips=fips, values=values, show_state_data=True,
    colorscale=colorscale, binning_endpoints=endpts,
    asp=2.9,
    paper_bgcolor='rgb(229,229,229)',
    title ='USA death numbers per county',
    show_hover=True, centroid_marker={'opacity': 0},
    legend_title='Deaths',
    county_outline={'color': 'rgb(224,224,224)', 'width': 0.5}
)

fig.layout.template = None
fig.show()

import plotly.figure_factory as ff

import numpy as np
import pandas as pd

df_infections = pd.read_csv('../data/csejhudump/COVID-19/csse_covid_19_data/csse_covid_19_time_series/time_series_covid19_confirmed_US.csv',
                            index_col = "Combined_Key")
df_lookup = pd.read_csv('../data/csejhudump/COVID-19/csse_covid_19_data/UID_ISO_FIPS_LookUp_Table.csv', index_col = "FIPS")

# Removing all blank FIPS rows
df_infections = df_infections[df_infections['FIPS'].notna()]

#debug print
print(df_infections)
values = df_infections[df_infections.columns[-20]].tolist()
fips = df_infections['FIPS'].tolist()

#Now per million needs lookup
length = len(values);
for i in range(length):
    popu = df_lookup.loc[fips[i], "Population"]
    if pd.isna(popu)  :
        values[i] = 0 # bug +++sandip counties that have no population entries are ignored
    else :
        #debug print
        #print(popu)
        values[i] = values[i]* 1000000 /int(popu)
        if values[i] > 20000 :
            print(df_lookup.loc[fips[i], "Combined_Key"])



#colorscale = ["#f7fbff","#ebf3fb","#deebf7","#d2e3f3","#c6dbef","#b3d2e9","#9ecae1",
#              "#85bcdb","#6baed6","#57a0ce","#4292c6","#3082be","#2171b5","#1361a9",
#              "#08519c","#0b4083","#08306b"]

#colorscale = ["#f7fbff","#ebf3fb","#c6dbef","#b3d2e9",
#              "#85bcdb","#4292c6","#3082be","#1361a9",
#              "#08519c","#08306b"]
colorscale = ["#f7fbff",
              "#85bcdb",
              "#08306b", "#FF2222"]

endpts = list(np.linspace(1, 20000, len(colorscale) - 1))

fig = ff.create_choropleth(
    fips=fips, values=values, show_state_data=True,
    colorscale=colorscale, binning_endpoints=endpts,
    asp=2.9,
    paper_bgcolor='rgb(229,229,229)',
    title ='USA infected rate per million',
    show_hover=True, 
    legend_title='Infected per million',
    county_outline={'color': 'rgb(224,224,224)', 'width': 0.5}
)
fig.layout.template = None
fig.show()

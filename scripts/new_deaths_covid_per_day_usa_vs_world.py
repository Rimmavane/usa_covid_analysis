from data_load import load_covid_worldwide_data

import pandas as pd

import plotly.graph_objs as go
import plotly.express as px

usa_data = load_covid_worldwide_data('data/full_data.csv')

usa_data = usa_data[usa_data['total_cases'] > 0]
top_10_countries = usa_data[usa_data['date'] == max(usa_data['date'])].sort_values(by='total_cases').drop_duplicates('location', keep='last').tail(10).location.to_list()

usa_data = usa_data[usa_data['location'].isin(top_10_countries)].sort_values(by='date').reset_index(drop=True)

location = set(usa_data.location.to_list())
dates = set(usa_data.date.to_list())
rows = []
for i in location:
    for k in dates:
        if ((usa_data.location == i) & (usa_data.date == k)).any():
            pass
        else:
            rows.append({'location': i, "date": k, 'new_deaths': 0, 'new_cases': 0, 'total_deaths': 0, 'total_cases': 0})

usa_data = usa_data.append(pd.DataFrame(rows), sort=True, ignore_index=True)
usa_data = usa_data.sort_values(by='date').reset_index(drop=True)
usa_data["date"] = usa_data["date"].astype(str)

fig = px.line(usa_data, x="date", y='new_deaths', color="location", hover_name="location")

layout = go.Layout(
    title=go.layout.Title(
        text="Daily COVID-19 deaths count in 9 countries with most COVID-19 cases and world",
        x=0.5
    ),
    font=dict(size=14),
    width=1200,
    height=800,
    xaxis_title="Date",
    yaxis_title="Confirmed new deaths count per day",
    transition={'duration': 333}
)
fig.update_layout(layout)
fig.update_yaxes(rangemode="nonnegative")
fig.write_html('../plots/new_deaths_covid19_worldwide_with_world.html')
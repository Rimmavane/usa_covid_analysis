from data_load import load_covid_usa_data, load_most_common_death_causes

import pandas as pd
import plotly.graph_objs as go
import plotly.express as px

usa_data = load_covid_usa_data('data/us_counties_covid19_daily.csv')

usa_cumulative = usa_data.groupby(['date'])['cases', 'deaths'].sum().reset_index()
usa_cumulative = usa_cumulative.melt(id_vars='date', value_vars=['cases', 'deaths'])

### Plot for number of cumulative covid cases over time
fig = px.line(usa_cumulative, x="date", y='value', color='variable')
for trace in fig.data:
    trace.name = trace.name.split('=')[1]
layout = go.Layout(
    title=go.layout.Title(
        text="Cumulative count of confirmed COVID-19 cases and deaths in USA",
        x=0.5
    ),
    font=dict(size=14),
    width=1200,
    height=800,
    xaxis_title="Date of observation",
    yaxis_title="Number of confirmed cases"
)
fig.update_layout(layout)
fig.write_html('../plots/cumulative_casualities_covid19_usa.html')

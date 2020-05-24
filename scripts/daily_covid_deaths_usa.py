from data_load import load_covid_usa_data
import plotly.graph_objs as go
import plotly.express as px

usa_data = load_covid_usa_data('data/us_counties_covid19_daily.csv')

usa_daily = usa_data.groupby(['date'])['cases', 'deaths'].sum().reset_index()
usa_daily['cases'] = usa_daily['cases'] - usa_daily['cases'].shift(1)
usa_daily['deaths'] = usa_daily['deaths'] - usa_daily['deaths'].shift(1)
usa_daily = usa_daily.melt(id_vars='date', value_vars=['cases', 'deaths'])


### Plot for number of cumulative covid cases over time
fig = px.line(usa_daily, x="date", y='value', color='variable')
for trace in fig.data:
    trace.name = trace.name.split('=')[1]
layout = go.Layout(
    title=go.layout.Title(
        text="Daily count of confirmed COVID-19 cases and deaths in USA",
        x=0.5
    ),
    font=dict(size=14),
    width=1200,
    height=800,
    xaxis_title="Date of observation",
    yaxis_title="Number of confirmed cases"
)
fig.update_layout(layout)
fig.write_html('../plots/daily_casualities_covid19_usa.html')

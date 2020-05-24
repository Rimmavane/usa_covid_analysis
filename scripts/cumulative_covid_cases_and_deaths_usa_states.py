from data_load import load_covid_usa_data

import pandas as pd
import plotly.graph_objs as go
import plotly.express as px

usa_data = load_covid_usa_data('data/us_counties_covid19_daily.csv')

usa_cumulative_state = usa_data.groupby(['date', 'state'])['cases', 'deaths'].sum().reset_index()
states = set(usa_cumulative_state.state.to_list())
dates = set(usa_cumulative_state.date.to_list())

rows = []
for i in states:
    for k in dates:
        if ((usa_cumulative_state.state == i) & (usa_cumulative_state.date == k)).any():
            pass
            pass
        else:
            rows.append({'state': i, "date": k, 'deaths': 0, 'cases': 0})


usa_cumulative_state = usa_cumulative_state.append(pd.DataFrame(rows), ignore_index=True)

usa_cumulative_state = usa_cumulative_state.sort_values(by='date').reset_index(drop=True)
usa_cumulative_state["date"] = usa_cumulative_state["date"].astype(str)

### comparison of death causes
fig = px.scatter(usa_cumulative_state, x="cases", y='deaths', animation_frame="date", animation_group='state',
                  color="state", size='cases', hover_name="state", range_x=[0, max(usa_cumulative_state['cases'])*1.02],
                  range_y=[0, max(usa_cumulative_state['deaths'])*1.02])

layout = go.Layout(
    title=go.layout.Title(
        text="Cumulative count of confirmed COVID-19 cases and deaths in states of USA",
        x=0.5
    ),
    font=dict(size=14),
    width=1200,
    height=800,
    xaxis_title="Confirmed infection cases of COVID-19",
    yaxis_title="Deaths caused by COVID-19"
)
fig.update_layout(layout)
fig.write_html('../plots/cumulative_casualities_per_state_covid19_usa.html')

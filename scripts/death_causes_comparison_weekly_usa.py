from data_load import load_covid_usa_data, load_most_common_death_causes

import plotly.graph_objs as go
import plotly.express as px

usa_data = load_covid_usa_data('data/us_counties_covid19_daily.csv')

usa_grouped = usa_data.groupby(['date'])['cases', 'deaths'].sum().reset_index()
days_since_outbreak = usa_grouped.iloc[-1].date - usa_grouped.iloc[0].date
days = days_since_outbreak.days
weekly_casualities = int(usa_grouped.iloc[-1]["deaths"] / days * 7)

death_causes = load_most_common_death_causes('data/NCHS_-_Leading_Causes_of_Death__United_States.csv')
death_causes = death_causes[death_causes['Year'] == 2017].drop(['Year', 'State'], axis=1).reset_index(drop=True)
death_causes['Deaths_weekly'] = death_causes['Deaths'].apply(lambda x: int(x/48))   #yearly to weekly
death_causes.drop('Deaths', axis=1, inplace=True)
death_causes = death_causes.append({'Cause Name': "COVID-19",
                                    "Deaths_weekly": weekly_casualities}, ignore_index=True).sort_values(by="Deaths_weekly", ascending=False)

### Plot comparison of death causes
fig = px.bar(death_causes, x="Cause Name", y='Deaths_weekly')
layout = go.Layout(
    title=go.layout.Title(
        text="Most common death causes and COVID-19 deaths per week",
        x=0.5
    ),
    font=dict(size=14),
    width=1200,
    height=800,
    xaxis_title="Cause of death",
    yaxis_title="Average weekly number of deaths"
)
fig.update_layout(layout)
fig.write_html('../plots/deaths_causes_from_2017_usa.html')

import argparse
import datetime
import pandas as pd
import plotly.graph_objs as go
import plotly.express as px
from constants import state_code_dict


parser = argparse.ArgumentParser(description='Interactive plots.')
parser.add_argument('-m', '--mode', default=0, type=int,
                    help='If 0, show plot in interactive plot. Otherwise (1), save to file.')
args = parser.parse_args()


def main(args):
    # load data
    cases_df = pd.read_csv('../data/us_counties_covid19_daily.csv')

    # convert state names to abbrevations
    cases_df.state = [state_code_dict[state] for state in cases_df.state]

    # daily cases for each state
    cases_df = cases_df.groupby(["state", "date"])["cases", "deaths"].sum().reset_index()
    # convert date as strings to datetime objects
    cases_df["date"] = pd.to_datetime(cases_df["date"], format="%Y-%m-%d").dt.date
    # sort by date
    cases_df = cases_df.sort_values(by="date").reset_index(drop=True)

    # filter entries older than..
    cases_df = cases_df[cases_df["date"] >= datetime.date(2020, 1, 15)]
    # back to dates as strings
    cases_df["date"] = cases_df["date"].astype(str)

    fig = px.choropleth(locations=cases_df["state"], color=cases_df["cases"],
                        locationmode="USA-states", scope="usa", animation_frame=cases_df["date"],
                        color_continuous_scale='Reds', range_color=[0, 200000])

    layout = go.Layout(
        title=go.layout.Title(
            text=" COVID-19 cases in US states",
            x=0.5
        ),
        font=dict(size=14),
    )

    fig.update_layout(layout)

    if args.mode == 0:
        fig.show()
    else:
        fig.write_html("plots/usa_map_cases.html")


if __name__ == '__main__':
    main(args)
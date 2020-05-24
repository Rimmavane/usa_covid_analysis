import argparse
import datetime
import pandas as pd
import plotly.graph_objs as go
import plotly.express as px

parser = argparse.ArgumentParser(description='Interactive plots.')
parser.add_argument('-m', '--mode', default=0, type=int,
                    help='If 0, show plot in interactive plot. Otherwise (1), save to file.')
args = parser.parse_args()


def main(args):
    # load data
    cases_df = pd.read_csv('../data/us_counties_covid19_daily.csv')

    # daily cases for each state
    cases_df = cases_df.groupby(["state", "date"])["cases", "deaths"].sum().reset_index()
    # convert date as strings to datetime objects
    cases_df["date"] = pd.to_datetime(cases_df["date"], format="%Y-%m-%d").dt.date
    # sort by date
    cases_df = cases_df.sort_values(by="date").reset_index(drop=True)

    # filter entries older than..
    cases_df = cases_df[cases_df["date"] >= datetime.date(2020, 3, 12)]
    # back to dates as strings
    cases_df["date"] = cases_df["date"].astype(str)

    fig = px.scatter(cases_df, x="cases", y="deaths", animation_frame="date", animation_group="state",
                     size="cases", color="state", hover_name="state",
                     log_x=False, size_max=60, range_x=[0, 360000], range_y=[-20, 30000])

    layout = go.Layout(
        title=go.layout.Title(
            text="Cases vs deaths in US states",
            x=0.5
        ),
        font=dict(size=14),
        xaxis_title="Number of cases",
        yaxis_title="Number of deaths"
    )

    fig.update_layout(layout)

    if args.mode == 0:
        fig.show()
    else:
        fig.write_html("plots/usa_cases_deaths_animation.html")


if __name__ == '__main__':
    main(args)
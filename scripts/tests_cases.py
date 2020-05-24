import argparse
import datetime
import pandas as pd
import plotly.graph_objs as go
import plotly.express as px
from constants import state_map_dict

parser = argparse.ArgumentParser(description='Interactive plots.')
parser.add_argument('-m', '--mode', default=0, type=int,
                    help='If 0, show plot in interactive plot. Otherwise (1), save to file.')
args = parser.parse_args()


def main(args):
    # load data
    us_covid_states = pd.read_csv('../data/us_states_covid19_daily.csv').fillna(0)
    # convert date to datetime object
    us_covid_states["date"] = pd.to_datetime(us_covid_states["date"], format="%Y%m%d").dt.date
    # sort by date
    us_covid_states = us_covid_states.sort_values(by="date").reset_index(drop=True)
    # annotate state abbrevations with full names
    us_covid_states.state = [state_map_dict[state] for state in us_covid_states.state]
    # filter entries older than ..
    us_covid_states = us_covid_states[us_covid_states["date"] >= datetime.date(2020, 3, 12)]
    # convert datetime objects back to str
    us_covid_states["date"] = us_covid_states["date"].astype(str)

    # line plot
    fig = px.scatter(us_covid_states, x="total", y="positive", animation_frame="date", animation_group="state",
                     size="positive", color="state", hover_name="state",
                     log_x=False, size_max=45, range_x=[0, 1500000], range_y=[0, 360000])

    layout = go.Layout(
        title=go.layout.Title(
            text="Cases vs tests in US states",
            x=0.5
        ),
        font=dict(size=14),
        xaxis_title="Number of tests",
        yaxis_title="Number of cases"
    )

    fig.update_layout(layout)

    if args.mode == 0:
        fig.show()
    else:
        fig.write_html("plots/usa_tests.html")


if __name__ == '__main__':
    main(args)
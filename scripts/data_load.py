import pandas as pd
import datetime

DATA_FOLDER = '../data'

def load_most_common_death_causes(data_path):
    data = pd.read_csv(data_path)
    data = data[data['State'] == 'United States']
    data = data[data['Cause Name'] != 'All causes']
    data.drop(columns=['113 Cause Name', 'Age-adjusted Death Rate'], inplace=True)
    data['Deaths'] = data.Deaths.apply(lambda x: x.replace(',', ''))
    data['Deaths'] = data.Deaths.astype(int)
    data['Year'] = data.Year.astype(int)
    return data

def load_covid_worldwide_data(data_path):
    data = pd.read_csv(data_path)
    data['date'] = data['date'].apply(lambda x: datetime.datetime.strptime(x, '%Y-%m-%d'))
    return data


def load_covid_usa_data(data_path):
    data = pd.read_csv(data_path)
    data.drop(columns=['county'], inplace=True)
    data['date'] = data['date'].apply(lambda x: datetime.datetime.strptime(x, '%Y-%m-%d'))
    data.sort_values(by='date', inplace=True)
    return data

import pandas as pd
import numpy as np


def clean_data():
    df = pd.read_csv('who_suicide_statistics_modified3.csv', sep=",")
    df.rename(columns={c: c.strip() for c in df.columns},
              inplace=True)  # remove trailing and leading space in column names
    df['suicides_no'] = df['suicides_no'].apply(lambda x: x if str(x).isnumeric() else 0).apply(np.int64)
    df['HDI for year'].fillna(0, inplace=True)
    df['gdp_for_year ($)'] = df['gdp_for_year ($)'].apply(lambda x: str(x).replace(',', '')).apply(np.int64)
    return df


# get generation entry belongs to
def get_generation(year):
    if 1883 <= year <= 1900:
        return 'Lost Generation'
    elif 1901 <= year <= 1927:
        return 'G.I. Generation'
    elif 1928 <= year <= 1945:
        return 'Silent'
    elif 1946 <= year <= 1964:
        return 'Boomers'
    elif 1965 <= year <= 1980:
        return 'Generation X'
    elif 1981 <= year <= 1995:
        return 'Millennials'
    elif 1996 <= year <= 2010:
        return 'Generation Z'
    else:
        return 'Generation A'


df = clean_data()

# create and compute values for generation column
df['generation'] = df.apply(lambda x: get_generation(x['year'] - int(str(x['age']).split('-')[0]) if '-' in x['age'] else int(x['age'][:2])), axis=1)

# output values to file
df.to_csv('generation.csv', sep=',', index=False)

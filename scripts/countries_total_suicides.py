import pandas as pd
import numpy as np


def clean_data():
    df = pd.read_csv('who_suicide_statistics_modified3.csv', sep=",")
    df.rename(columns={c: c.strip() for c in df.columns}, inplace=True)
    df['suicides_no'] = df['suicides_no'].apply(lambda x: x if str(x).isnumeric() else 0).apply(np.int64)
    df['HDI for year'].fillna(0, inplace=True)
    df['gdp_for_year ($)'] = df['gdp_for_year ($)'].apply(lambda x: str(x).replace(',', '')).apply(np.int64)
    return df

# Group by country and sum suicide number
df = clean_data().groupby(['country']).agg({'suicides_no': 'sum'}).sort_values(by='suicides_no', ascending=False).reset_index()
df['rank'] = df.index + 1
df.to_csv('countries_total_suicides.csv', sep=',', index=False)

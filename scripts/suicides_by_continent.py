import pandas as pd
import numpy as np


def clean_data():
    df = pd.read_csv('who_suicide_statistics_modified3.csv', sep=",")
    df.rename(columns={c: c.strip() for c in df.columns}, inplace=True)
    df['suicides_no'] = df['suicides_no'].apply(lambda x: x if str(x).isnumeric() else 0).apply(np.int64)
    df['HDI for year'].fillna(0, inplace=True)
    df['gdp_for_year ($)'] = df['gdp_for_year ($)'].apply(lambda x: str(x).replace(',', '')).apply(np.int64)
    return df

# Read continent file
df_con = pd.read_csv('continent_mapping.csv', sep=",")

# merge and compute number of suicide per continent
df = pd.merge(clean_data(), df_con[['country', 'continent']], left_on=['country'], right_on=['country']).groupby(['continent']).agg({'suicides_no': 'sum'}).sort_values(by='suicides_no', ascending=False).reset_index()
df.to_csv('suicides_by_continent.csv', sep=',', index=False)

import pandas as pd
import numpy as np

HUND_VAL = 100000

# Clean dataset
def clean_data():
    df = pd.read_csv('who_suicide_statistics_modified3.csv', sep=",")
    df.rename(columns={c: c.strip() for c in df.columns}, inplace=True)
    df['suicides_no'] = df['suicides_no'].apply(lambda x: x if str(x).isnumeric() else 0).apply(np.int64)
    df['HDI for year'].fillna(0, inplace=True)
    df['gdp_for_year ($)'] = df['gdp_for_year ($)'].apply(lambda x: str(x).replace(',', '')).apply(np.int64)
    return df


def suicides_by(suicide_no, population):
    return suicide_no / (population / HUND_VAL)


df = clean_data()
# Create and compute suicides/100K column
df['suicides/100K'] = df.apply(lambda x: suicides_by(x['suicides_no'], x['population']), axis=1)

# Ouput result
df.to_csv('suicides_per_100K.csv', sep=',', index=False)

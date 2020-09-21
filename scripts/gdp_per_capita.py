import pandas as pd
import numpy as np

def clean_data():
    df = pd.read_csv('who_suicide_statistics_modified3.csv', sep=",")
    df.rename(columns={c: c.strip() for c in df.columns}, inplace=True) #remove trailing and leading space in column names
    df['suicides_no'] = df['suicides_no'].apply(lambda x: x if str(x).isnumeric() else 0).apply(np.int64)
    df['HDI for year'].fillna(0, inplace=True)
    df['gdp_for_year ($)'] = df['gdp_for_year ($)'].apply(lambda x: str(x).replace(',','')).apply(np.int64)
    return df


# Compute GDP per Capita for each
def compute_gdp_per_capita(df):
    df_gdp = df.groupby(['country', 'year', 'gdp_for_year ($)']).agg({'population':'sum'}).reset_index()
    df_gdp['gdb_per_capita'] = df_gdp.apply(lambda x: x['gdp_for_year ($)'] / x['population'], axis=1)
    return df_gdp

df = clean_data()
df_gdp = compute_gdp_per_capita(df)

# Merging clean dataset with computed GDP per Capita values
df = pd.merge(df, df_gdp[['country','year','gdb_per_capita']], left_on=['country','year'], right_on = ['country','year'])

# output result to file
df.to_csv('gdp_per_capita.csv', sep=',', index=False)

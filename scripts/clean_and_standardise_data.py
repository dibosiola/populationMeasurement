import pandas as pd
import numpy as np
import io

df = pd.read_csv('who_suicide_statistics_modified3.csv', sep=",")

#Remove trailing and leading space in column names
df.rename(columns={c: c.strip() for c in df.columns}, inplace=True)

#Convert all entries in suicide_no column to numeric values and replace all non numeric and null values with 0
df['suicides_no'] = df['suicides_no'].apply(lambda x: x if str(x).isnumeric() else 0).apply(np.int64)

#Replace all null values in HDI for year with 0
df['HDI for year'].fillna(0, inplace=True)

#Remove commas from entries in gdp_for_year ($) column and convert to a numeric value
df['gdp_for_year ($)'] = df['gdp_for_year ($)'].apply(lambda x: str(x).replace(',', '')).apply(np.int64)

#Write results to file
buffer = io.StringIO()
df.info(buf=buffer)
s = buffer.getvalue()
with open("clean_and_standardise_data.txt", "w", encoding="utf-8") as f:
     f.write(s)

#Write cleaned data to file
df.to_csv('clean_and_standardise_data.csv', sep=',', index=False)

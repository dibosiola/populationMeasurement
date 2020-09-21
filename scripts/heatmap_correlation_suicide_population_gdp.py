import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns

fig, ax = plt.subplots(nrows=1, ncols=1, figsize=(15, 5.95))

HUND_VAL = 100000


def clean_data():
    df = pd.read_csv('who_suicide_statistics_modified3.csv', sep=",")
    df.rename(columns={c: c.strip() for c in df.columns}, inplace=True)
    df['suicides_no'] = df['suicides_no'].apply(lambda x: x if str(x).isnumeric() else 0).apply(np.int64)
    df['HDI for year'].fillna(0, inplace=True)
    df['gdp_for_year ($)'] = df['gdp_for_year ($)'].apply(lambda x: str(x).replace(',', '')).apply(np.int64)
    return df


def suicides_by(suicide_no, population):
    return suicide_no / (population / HUND_VAL)


def compute_gdp_per_capita(df):
    df_gdp = df.groupby([df['country'], df['year'], df['gdp_for_year ($)']]).agg({'population': 'sum'}).reset_index()
    df_gdp['gdb_per_capita'] = df_gdp.apply(lambda x: x['gdp_for_year ($)'] / x['population'], axis=1)
    return df_gdp


df = clean_data()
df_gdp = compute_gdp_per_capita(df)
df = pd.merge(df, df_gdp[['country', 'year', 'gdb_per_capita']], left_on=['country', 'year'], right_on= ['country', 'year'])
df['suicides/100K'] = df.apply(lambda x: suicides_by(x['suicides_no'], x['population']), axis=1)

# Selecting columns to perform correlation on
df = df[['suicides_no', 'suicides/100K', 'population', 'gdb_per_capita', 'gdp_for_year ($)']]

# Compute Spearman Rank Correlation on columns plot result
sns.heatmap(df.corr(method='spearman'), cmap='YlGnBu', annot=True, annot_kws={"size": 20}, fmt='.2f', linewidths=1.5, ax=ax)
cbar = ax.collections[0].colorbar
cbar.ax.tick_params(labelsize=20)
ax.tick_params(axis="y", labelsize=20, labelcolor="black", direction="out", length=5, labelrotation=0)
ax.tick_params(axis="x", labelsize=20, labelcolor="black", direction="out", length=5, labelrotation=85)

# Save figure to file
plt.savefig("heatmap_correlation_suicide_population_gdp.pdf",  bbox_inches="tight")

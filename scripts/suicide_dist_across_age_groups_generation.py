import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns

# x and y axis ordering
custom_ordering_gen = {"Generation A": 1, "Generation Z": 2, "Millennials": 3, "Generation X": 4, "Boomers": 5, "Silent": 6, "G.I. Generation": 7, "Lost Generation": 8}
column_name_gen = {1: 'Generation A', 2: 'Generation Z', 3: 'Millennials', 4: 'Generation X', 5: 'Boomers', 6: 'Silent', 7: 'G.I. Generation', 8: 'Lost Generation'}

custom_ordering_age = {"5-14 years": 1, "15-24 years": 2, "25-34 years": 3, "35-54 years": 4, "55-74 years": 5, "75+ years": 6}
column_name_age = {1: '5-14 years', 2: '15-24 years', 3: '25-34 years', 4: '35-54 years', 5: '55-74 years', 6: '75+ years'}

fig, ax = plt.subplots(nrows=1, ncols=1, figsize=(15, 5.95))


def clean_data():
    df = pd.read_csv('who_suicide_statistics_modified3.csv', sep=",")
    df.rename(columns={c: c.strip() for c in df.columns}, inplace=True)
    df['suicides_no'] = df['suicides_no'].apply(lambda x: x if str(x).isnumeric() else 0).apply(np.int64)
    df['HDI for year'].fillna(0, inplace=True)
    df['gdp_for_year ($)'] = df['gdp_for_year ($)'].apply(lambda x: str(x).replace(',', '')).apply(np.int64)
    return df


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

df['generation'] = df.apply(lambda x: get_generation(x['year'] - int(str(x['age']).split('-')[0]) if '-' in x['age'] else int(x['age'][:2])), axis=1)
df['rank_age'] = df['age'].map(custom_ordering_age)

df_heat = df.groupby(['generation', 'age', 'rank_age']).agg({'suicides_no': 'sum'})

df_heat['percent_dist'] = df_heat.groupby('generation')['suicides_no'].transform(lambda x: 100 * x / x.sum())
df_heat = df_heat.reset_index()

df_heat = df_heat.pivot(index='generation', columns='rank_age', values='percent_dist').reset_index()
df_heat.rename(columns=column_name_age, inplace=True)
df_heat['rank_gen'] = df_heat['generation'].map(custom_ordering_gen)
df_heat = df_heat.sort_values(["rank_gen"], ascending=(True))

df_heat = df_heat[['generation', '5-14 years', '15-24 years', '25-34 years', '35-54 years', '55-74 years', '75+ years']]
df_heat.set_index('generation', inplace=True)
df_heat.fillna(0, inplace=True)
sns.heatmap(df_heat, annot=True, cmap='YlGnBu', annot_kws={"size": 15}, fmt='.2f', linewidths=1.5, ax=ax)
cbar = ax.collections[0].colorbar
cbar.ax.tick_params(labelsize=20)

ax.set_xlabel('Age Group', fontsize=20, fontweight="bold")
ax.set_ylabel('Generation', fontsize=20, fontweight="bold")
ax.tick_params(axis="y", labelsize=20, labelcolor="black", direction="out", length=5, labelrotation=0)
ax.tick_params(axis="x", labelsize=20, labelcolor="black", direction="out", length=5, labelrotation=85)

# output to file
plt.savefig("suicide_dist_across_age_groups_generation.pdf",  bbox_inches="tight")

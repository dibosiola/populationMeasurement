import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from matplotlib.ticker import FuncFormatter

colors = ['#1f77b4', '#ff7f0e', '#2ca02c', '#d62728', '#9467bd', '#8c564b']
plt.style.use('seaborn-whitegrid')
fig, ax = plt.subplots(nrows=2, ncols=1, figsize=(80, 40))

# Custom arrangements
custom_ordering = {"5-14 years": 1, "15-24 years": 2, "25-34 years": 3, "35-54 years": 4, "55-74 years": 5, "75+ years": 6}
column_name = {1: '5-14 years', 2: '15-24 years', 3: '25-34 years', 4: '35-54 years', 5: '55-74 years', 6: '75+ years'}


# Axis tick label formatting
def thousand(x, pos):
    return '%1.0fK' % (x * 1e-3)


def clean_data():
    df = pd.read_csv('who_suicide_statistics_modified3.csv', sep=",")
    df.rename(columns={c: c.strip() for c in df.columns}, inplace=True)
    df['suicides_no'] = df['suicides_no'].apply(lambda x: x if str(x).isnumeric() else 0).apply(np.int64)
    df['HDI for year'].fillna(0, inplace=True)
    df['gdp_for_year ($)'] = df['gdp_for_year ($)'].apply(lambda x: str(x).replace(',', '')).apply(np.int64)
    df['year'] = df['year'].astype('str')
    return df


df = clean_data().groupby(['year', 'sex', 'age']).agg({'suicides_no': 'sum'}).reset_index()
df['rank'] = df['age'].map(custom_ordering)
df = df.sort_values(["year", "rank"], ascending=(True, True))

sex = df['sex'].unique().tolist()

i = 0
for s in sex:
    df_filter = df.loc[(df['sex'] == s), ('year', 'rank', 'suicides_no')].pivot(index='year', columns='rank', values='suicides_no')
    df_filter.rename(columns=column_name, inplace=True)
    df_filter.plot(color=colors, ax=ax.flat[i], legend=False, markersize=40, lw=20, marker='o')

    ax.flat[i].yaxis.set_major_formatter(FuncFormatter(thousand))
    ax.flat[i].set_title(str(s).capitalize(), fontweight="bold", fontsize=60)
    ax.flat[i].set_xlabel('Year\n', fontsize=60, fontweight="bold")
    ax.flat[i].set_ylabel('# of Suicides (Thousands)', fontsize=60, fontweight="bold")
    ax.flat[i].tick_params(axis="x", labelsize=60, labelcolor="black", direction="out", length=5, labelrotation=0, pad=0.5)
    ax.flat[i].tick_params(axis="y", labelsize=60, labelcolor="black", direction="out", length=5)
    i += 1

h1, l1 = ax.flat[0].get_legend_handles_labels()

plt.legend(h1, l1, fontsize=60, loc='upper center', bbox_to_anchor=(0.5, -0.15), ncol=6)
plt.grid(b=True, which='major', color='#666666', linestyle='-')
plt.tight_layout()

# Output figure to file
plt.savefig("population_suicide_rate_per_year_sex_age_group.pdf", bbox_inches="tight")

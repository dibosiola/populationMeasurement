import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from matplotlib.ticker import FuncFormatter


color_bars = ['#1f77b4', '#ff7f0e']
color_lines = ['#2ca02c', '#d62728']
plt.style.use('seaborn-ticks')
fig, ax = plt.subplots(nrows=1, ncols=1, figsize=(15, 5.95))
ax2 = ax.twinx()

legend = []

# Formatting axis tick labels
def million(x, pos):
    return '%1.0fM' % (x * 1e-6)


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


df = clean_data()

df_pop = df.groupby(['year', 'sex']).agg({'population': 'sum'}).sort_values(by='year', ascending=True).reset_index().pivot(index='year', columns='sex', values='population')
df_suicide = df.groupby(['year', 'sex']).agg({'suicides_no': 'sum'}).sort_values(by='year', ascending=True).reset_index().pivot(index='year', columns='sex', values='suicides_no')

# Renaming columns for legend purpose (Population)
df_pop.rename(columns={'female': 'Female (Population)', 'male': 'Male (Population)'}, inplace=True)
df_pop.plot.bar(color=color_bars, ax=ax, legend=False)
ax.yaxis.set_major_formatter(FuncFormatter(million))

# Renaming columns for legend purpose (Suicides)
df_suicide.rename(columns={'female': 'Female (Suicide)', 'male': 'Male (Suicide)'}, inplace=True)
df_suicide.plot(color=color_lines, ax=ax2, legend=False, markersize=13, lw=5, marker='o')
ax2.yaxis.set_major_formatter(FuncFormatter(thousand))

ax.set_xlabel('Year', fontsize=20, fontweight="bold")
ax.set_ylabel('Population (Millions)', fontsize=20, fontweight="bold")
ax2.set_ylabel('# of Suicides (Thousands)', fontsize=20, fontweight="bold")

ax.tick_params(axis="x", labelsize=20, labelcolor="black", direction="out", length=5, labelrotation=85, pad=0.5)
ax.tick_params(axis="y", labelsize=20, labelcolor="black", direction="out", length=5)
ax2.tick_params(axis="y", labelsize=20, labelcolor="black", direction="out", length=5)

h1, l1 = ax.get_legend_handles_labels()
h2, l2 = ax2.get_legend_handles_labels()

ax.legend(h1 + h2, l1+l2, fontsize=18, loc='upper center', ncol=4, bbox_to_anchor=(0.5, -0.2))
plt.tight_layout()

# Output figure to file
plt.savefig("population_suicide_rate_per_year_sex.pdf",  bbox_inches="tight")

import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from matplotlib.ticker import FuncFormatter

colors = ['#1f77b4', '#ff7f0e', '#2ca02c', '#d62728', '#9467bd', '#8c564b']
plt.style.use('seaborn-ticks')


fig = plt.figure(figsize=(60, 22))
gs = fig.add_gridspec(1, 3)
ax1 = fig.add_subplot(gs[0, 0])
ax2 = fig.add_subplot(gs[0, 1:])

custom_ordering = {"Generation A": 1, "Generation Z": 2, "Millennials": 3, "Generation X": 4, "Boomers": 5, "Silent": 6,
                   "G.I. Generation": 7, "Lost Generation": 8}
column_name = {1: 'Generation A', 2: 'Generation Z', 3: 'Millennials', 4: 'Generation X', 5: 'Boomers', 6: 'Silent',
               7: 'G.I. Generation', 8: 'Lost Generation'}


def billion(x, pos):
    return '%1.0fB' % (x * 1e-9)


def million(x, pos):
    return '%1.1fM' % (x * 1e-6)


def thousand(x, pos):
    return '%1.0fK' % (x * 1e-3)


def clean_data():
    df = pd.read_csv('who_suicide_statistics_modified3.csv', sep=",")
    df.rename(columns={c: c.strip() for c in df.columns},
              inplace=True)  # remove trailing and leading space in column names
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
df['generation'] = df.apply(
    lambda x: get_generation(x['year'] - int(str(x['age']).split('-')[0]) if '-' in x['age'] else int(x['age'][:2])),
    axis=1)
df['rank'] = df['generation'].map(custom_ordering)

# Bar Graph
df_gen = df.groupby(['generation', 'rank']).agg({'population': 'sum', 'suicides_no': 'sum'}).reset_index()
df_gen = df_gen.sort_values(["rank"], ascending=(True))
df_gen.set_index('generation', inplace=True)

# Line Graph
df_gen_years = df.groupby(['generation', 'year', 'rank']).agg({'suicides_no': 'sum'}).reset_index().pivot(index='year',columns='rank',values='suicides_no')
df_gen_years.rename(columns=column_name, inplace=True)

ax1_sec = ax1.twinx()
width = 0.3
df_gen.population.plot(kind='bar', color=colors[0], ax=ax1, width=width, position=1)
df_gen.suicides_no.plot(kind='bar', color=colors[1], ax=ax1_sec, width=width, position=0)
ax1.yaxis.set_major_formatter(FuncFormatter(billion))
ax1_sec.yaxis.set_major_formatter(FuncFormatter(million))
ax1.set_xlabel('Generation\n(a)', fontsize=60, fontweight="bold")
ax1.set_ylabel('Population (Billion)', fontsize=60, fontweight="bold", color=colors[0])
ax1_sec.set_ylabel('# of Suicides (Millions)', fontsize=60, fontweight="bold", color=colors[1])
ax1.tick_params(axis="x", labelsize=60, labelcolor="black", direction="out", length=5, labelrotation=85, pad=0.5)
ax1.tick_params(axis="y", labelsize=60, labelcolor=colors[0], direction="out", length=5)
ax1_sec.tick_params(axis="y", labelsize=60, labelcolor=colors[1], direction="out", length=5)
h1, l1 = ax1.get_legend_handles_labels()
h2, l2 = ax1_sec.get_legend_handles_labels()
ax1.legend(h1 + h2, l1 + l2, fontsize=50, loc='upper left', ncol=1)

plt.style.use('seaborn-whitegrid')
df_gen_years.plot(color=colors, ax=ax2, legend=False, markersize=40, lw=15, marker='o')
ax2.yaxis.set_major_formatter(FuncFormatter(thousand))
ax2.set_xlabel('Year\n(b)', fontsize=60, fontweight="bold")
ax2.set_ylabel('# of Suicides', fontsize=60, fontweight="bold")
ax2.tick_params(axis="x", labelsize=60, labelcolor="black", direction="out", length=5, labelrotation=0, pad=0.5)
ax2.tick_params(axis="y", labelsize=60, labelcolor="black", direction="out", length=5)
h3, l3 = ax2.get_legend_handles_labels()
ax2.legend(h3, l3, fontsize=40, loc='upper center', ncol=6, bbox_to_anchor=(0.5, -0.2))

ax2.grid(b=True, which='major', color='#666666', linestyle='-')
plt.tight_layout()

# Output figure to file
plt.savefig("generation_suicide_generation.pdf", bbox_inches="tight")

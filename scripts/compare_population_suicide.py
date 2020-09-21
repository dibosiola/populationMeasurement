import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import matplotlib.patches as mpatches
import matplotlib.lines as mlines
from matplotlib.ticker import FuncFormatter

colors = ['#1f77b4', '#ff7f0e']
plt.style.use('seaborn-ticks')
fig, ax = plt.subplots(nrows=1, ncols=1, figsize=(15, 5.95))
# Creating secondary axis
ax2 = ax.twinx()

legend = []

# Formatting axis tick labels
def thousand(x, pos):
    return '%1.0fK' % (x * 1e-3)


def billion(x, pos):
    return '%1.1fB' % (x * 1e-9)


def clean_data():
    df = pd.read_csv('who_suicide_statistics_modified3.csv', sep=",")
    df.rename(columns={c: c.strip() for c in df.columns}, inplace=True)
    df['suicides_no'] = df['suicides_no'].apply(lambda x: x if str(x).isnumeric() else 0).apply(np.int64)
    df['HDI for year'].fillna(0, inplace=True)
    df['gdp_for_year ($)'] = df['gdp_for_year ($)'].apply(lambda x: str(x).replace(',', '')).apply(np.int64)
    df['year'] = df['year'].astype('str')
    return df


df = clean_data().groupby(['year']).agg({'population': 'sum', 'suicides_no': 'sum'}).sort_values(by='year', ascending=True).reset_index()

# Line Plot
df_line = df.filter(['year', 'suicides_no'], axis=1)
df_line.set_index('year', inplace=True)
df_line.plot(color=colors[0], ax=ax2, legend=False, markersize=10, lw=5, marker='o')
legend.append(mlines.Line2D([], [], color=colors[0], markersize=10, label='# of Suicide', lw=5, marker='o'))

# Bar Plot
df_bar = df.filter(['year', 'population'], axis=1)
df_bar.set_index('year', inplace=True)
df_bar.plot.bar(color=colors[1], ax=ax, legend=False)
legend.append(mpatches.Patch(color=colors[1], label='Population'))

# Applying formatting to axis tick labels
ax.yaxis.set_major_formatter(FuncFormatter(billion))
ax2.yaxis.set_major_formatter(FuncFormatter(thousand))

ax.legend(handles=legend, fontsize=18, ncol=1)
ax.set_xlabel('Year', fontsize=20, fontweight="bold")
ax.set_ylabel('Population (Billions)', fontsize=20, fontweight="bold", color=colors[1])
ax2.set_ylabel('# of Suicides (Thousands)', fontsize=20, fontweight="bold", color=colors[0])

ax.tick_params(axis="x", labelsize=20, labelcolor="black", direction="out", length=5, labelrotation=85, pad=0.5)
ax.tick_params(axis="y", labelsize=20, labelcolor=colors[1], direction="out", length=5)
ax2.tick_params(axis="y", labelsize=20, labelcolor=colors[0], direction="out", length=5)
plt.tight_layout()

# Save output to file
plt.savefig("compare_population_suicide.pdf",  bbox_inches="tight")

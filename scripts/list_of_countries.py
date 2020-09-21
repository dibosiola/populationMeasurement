import pandas as pd

df = pd.read_csv('who_suicide_statistics_modified3.csv', sep=",")[['country']].drop_duplicates()
df.to_csv('list_of_countries.csv', sep=',', index=False)

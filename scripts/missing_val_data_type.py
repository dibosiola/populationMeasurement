import pandas as pd
import io

df = pd.read_csv('who_suicide_statistics_modified3.csv', sep=",")
buffer = io.StringIO()
df.info(buf=buffer)
s = buffer.getvalue()
with open("missing_val_data_type.txt", "w",encoding="utf-8") as f: 
     f.write(s)

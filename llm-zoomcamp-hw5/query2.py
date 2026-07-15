import sqlite3
import pandas as pd

conn = sqlite3.connect("traces.db")
df = pd.read_sql_query("SELECT input_tokens FROM spans WHERE name = 'my_llm'", conn)

print(df)

min_val = df["input_tokens"].min()
max_val = df["input_tokens"].max()
mean_val = df["input_tokens"].mean()

pct_variation = (max_val - min_val) / mean_val * 100

print(f"Min: {min_val}, Max: {max_val}, Mean: {mean_val:.1f}")
print(f"Variation (max-min)/mean: {pct_variation:.1f}%")
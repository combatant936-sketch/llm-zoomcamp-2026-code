import sqlite3
import pandas as pd

conn = sqlite3.connect("traces.db")
df = pd.read_sql_query("SELECT * FROM spans where name in('my_llm','my_search')", conn)

df["duration_ms"] = (df["end_time"] - df["start_time"]) / 1e6

# filter + sort for step 1
subset = df[df["name"].isin(["my_llm", "my_search"])].sort_values("start_time")
print(subset[["name", "start_time", "end_time", "duration_ms"]])

# total duration per name for step 2
totals = df.groupby("name")["duration_ms"].sum().sort_values(ascending=False)
print(totals)
top_span = totals.idxmax()
print(f"Span type with most total time: {top_span}")
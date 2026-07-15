from starter import rag


# if __name__ == "__main__":
#     query = "How does the agentic loop keep calling the model until it stops?"
#     answer = rag.rag(query)
# #     print(answer)

# import sqlite3
# from opentelemetry.sdk.trace.export import SpanExporter, SpanExportResult


# class SQLiteSpanExporter(SpanExporter):

#     def __init__(self, db_path="traces.db"):
#         self.conn = sqlite3.connect(db_path)
#         self.conn.execute("""
#             CREATE TABLE IF NOT EXISTS spans (
#                 name TEXT,
#                 start_time INTEGER,
#                 end_time INTEGER,
#                 input_tokens INTEGER,
#                 output_tokens INTEGER,
#                 cost REAL
#             )
#         """)
#         self.conn.commit()

#     def export(self, spans):
#         for span in spans:
#             attrs = dict(span.attributes or {})
#             self.conn.execute(
#                 "INSERT INTO spans VALUES (?, ?, ?, ?, ?, ?)",
#                 (
#                     span.name,
#                     span.start_time,
#                     span.end_time,
#                     attrs.get("input_tokens"),
#                     attrs.get("output_tokens"),
#                     attrs.get("cost"),
#                 ),
#             )
#         self.conn.commit()
#         return SpanExportResult.SUCCESS

#     def shutdown(self):
#         self.conn.close()

#     def force_flush(self):
#         return True

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
import sqlite3
import pandas as pd

conn = sqlite3.connect("retail_app.db")

def run(label, query):
    print(f"===== {label} =====")
    df = pd.read_sql(query, conn)
    print(df)
    print("\n-----------------------------\n")

# A...
# B...
# etc...

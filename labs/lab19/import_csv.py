import pandas as pd
import sqlite3

# Read CSV file
df = pd.read_csv("consumption.csv")

# Create / connect to SQLite database
conn = sqlite3.connect("retail_app.db")

# Insert DataFrame into SQL database
df.to_sql("consumption", conn, if_exists="replace", index=False)

conn.commit()
conn.close()

print("consumption.csv successfully imported into retail_app.db!")

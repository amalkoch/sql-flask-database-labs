import sqlite3
import matplotlib.pyplot as plt
from datetime import datetime, date

# Connect to the database
conn = sqlite3.connect("retail_app.db")
cursor = conn.cursor()

# Get first_name, last_name, dob from customer table
cursor.execute("""
    SELECT first_name, last_name, dob
    FROM customer
    ORDER BY last_name, first_name;
""")
rows = cursor.fetchall()

names = []
ages = []

print("Customer Name (last, first) | Age")
print("---------------------------------")

today = date.today()

for first, last, dob_str in rows:
    # Full name in "last, first" format
    full_name = f"{last}, {first}"

    # Convert dob text to date and compute age
    # Your DOB format is: YYYY/DD/MM (example: 2000/23/11)
    dob_date = datetime.strptime(dob_str, "%Y/%d/%m").date()

    age = today.year - dob_date.year - (
        (today.month, today.day) < (dob_date.month, dob_date.day)
    )

    names.append(full_name)
    ages.append(age)

    print(full_name, age)

# Use numeric x positions for scatter plot
x_positions = list(range(len(names)))

# Wide figure so labels fit
plt.figure(figsize=(22, 8))

# Scatter plot: age vs customer name
plt.scatter(x_positions, ages)

plt.xlabel("Customer Name")
plt.ylabel("Age")
plt.title("Customer Age by Customer Name")

# Customer names at 45 degrees on X-axis
plt.xticks(x_positions, names, rotation=45, ha="right", fontsize=8)

plt.tight_layout()
plt.show()

# Close DB connection
conn.close()


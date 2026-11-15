from flask import Flask, render_template, request
import sqlite3
import pandas as pd
from pathlib import Path

app = Flask(__name__)

@app.route('/', methods=['GET', 'POST'])
def employee():
    if request.method == 'POST':
        # Read the form data
        last_name = request.form.get('last_name')

        # Use pathlib to construct the database file path
        # resolve() not required. It converts file relative path to absolute path
        db_file = Path(__file__).resolve().parent.parent / "retail_app.db"

        # Connect to the database
        conn = sqlite3.connect(db_file)

        # Use Pandas to retrieve the employee information from the employee table
        query = "SELECT * FROM employee WHERE last_name=?"
        df = pd.read_sql_query(query, conn, params=(last_name,))

        # Close the database connection
        conn.close()

        # Check if data exists
        if df.empty:
            employee_info = f'Employee with last name {last_name} does not exist.'
            return render_template('get_employee_by_last_name.html', employee_info=employee_info)
        else:
            employee_info = df.to_html(index=False)
            return render_template('get_employee_by_last_name.html', employee_info=employee_info)

    # GET request → show empty form
    return render_template('get_employee_by_last_name.html')

if __name__ == '__main__':
    app.run(debug=True)


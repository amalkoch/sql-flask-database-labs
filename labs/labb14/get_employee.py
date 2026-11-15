from flask import Flask, render_template, request
import sqlite3
import pandas as pd
from pathlib import Path

app = Flask(__name__)

@app.route('/', methods=['GET', 'POST'])
def employee():
    if request.method == 'POST':
        # Read the form data
        emp_id = request.form.get('employee_id')

        # Use pathlib to construct the database file path
        # (sadece parent yeterli, parent.parent fazla olur)
        db_file = Path(__file__).resolve().parent / "retail_app.db"

        # Connect to the database
        conn = sqlite3.connect(db_file)

        # Retrieve employee info
        query = "SELECT * FROM employee WHERE employee_id=?"
        df = pd.read_sql_query(query, conn, params=(emp_id,))

        conn.close()

        # Check if found
        if df.empty:
            message = f"Employee with ID {emp_id} not found."
            return render_template('get_employee.html', employee_info=message)
        else:
            # Convert to HTML table
            employee_info = df.to_html(index=False)
            return render_template('get_employee.html', employee_info=employee_info)

    # GET request → show form
    return render_template('get_employee.html')

if __name__ == '__main__':
    app.run(debug=True)

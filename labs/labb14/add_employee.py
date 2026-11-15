from flask import Flask, render_template, request
import sqlite3
import pandas as pd
from pathlib import Path

app = Flask(__name__)

@app.route('/', methods=['GET', 'POST'])
def add_employee():
    if request.method == 'POST':
        # Read the form data
        employee_first_name = request.form.get('employee_first_name')
        employee_last_name = request.form.get('employee_last_name')
        employee_gender = request.form.get('employee_gender')
        employee_dob = request.form.get('employee_dob')
        employee_hire_date = request.form.get('employee_hire_date')
        employee_salary = request.form.get('employee_salary')

        # Use pathlib to construct the database file path
        db_file = Path(__file__).resolve().parent.parent / "retail_app.db"
        conn = sqlite3.connect(db_file)

        # Next employee_id = current max + 1 (or 1 if the table is empty)
        max_id = pd.read_sql_query("SELECT MAX(employee_id) FROM employee", conn).iloc[0, 0]
        employee_id = 1 if pd.isnull(max_id) else int(max_id) + 1

        new_employee = pd.DataFrame({
            'employee_id': [employee_id],
            'first_name': [employee_first_name],
            'last_name': [employee_last_name],
            'gender': [employee_gender],
            'dob': [employee_dob],
            'hire_date': [employee_hire_date],
            'salary': [int(employee_salary) if employee_salary else None],
        })
        new_employee.to_sql('employee', conn, if_exists='append', index=False)
        conn.commit()
        conn.close()

        return '<h1>Success</h1>The employee record has been successfully added to the database.'

    # GET: show the form
    return render_template('add_employee.html')

if __name__ == '__main__':
    app.run(debug=True)






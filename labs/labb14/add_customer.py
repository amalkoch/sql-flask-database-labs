from flask import Flask, render_template, request
import sqlite3
from pathlib import Path
import pandas as pd

app = Flask(__name__)

@app.route('/', methods=['GET', 'POST'])
def add_customer():
    if request.method == 'POST':
        # Read the form data
        customer_first_name = request.form.get('customer_first_name')
        customer_last_name = request.form.get('customer_last_name')
        customer_gender = request.form.get('customer_gender')
        customer_dob = request.form.get('customer_dob')

        # File paths
       # current_dir = Path(__file__).parent
        #parent_dir = current_dir.parent
        #db_file = parent_dir / "retail_app.db"
        
        # Use pathlib to construct the database file path
        db_file = Path(__file__).resolve().parent.parent / "retail_app.db"

        # Connect to the database
        conn = sqlite3.connect(db_file)

        # Use Pandas to retrieve the maximum customer_id from the customer table
        query = "SELECT MAX(customer_id) FROM customer"
        max_customer_id = pd.read_sql_query(query, conn).iloc[0, 0]

        # If the table is empty, start with customer_id = 1
        if pd.isnull(max_customer_id):
            customer_id = 1
        else:
            customer_id = int(max_customer_id) + 1

        # Create a DataFrame with the new record
        new_customer = pd.DataFrame({
            'customer_id': [customer_id],
            'first_name': [customer_first_name],
            'last_name': [customer_last_name],
            'gender': [customer_gender],
            'dob': [customer_dob]
        })

        # Use Pandas to insert the new record into the customer table
        new_customer.to_sql('customer', conn, if_exists='append', index=False)

        # Commit the transaction and close the database connection
        conn.commit()
        conn.close()

        # Return a response to the user
        return '<h1>Success</h1>The customer record has been successfully added to the database.'

    else:
        # Render the form
        return render_template('add_customer.html')

if __name__ == '__main__':
    app.run(debug=True)

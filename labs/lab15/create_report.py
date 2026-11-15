from flask import Flask, render_template, request
import pandas as pd
from pathlib import Path
import sqlite3

app = Flask(__name__)

@app.route('/', methods=['GET', 'POST'])
def customer_invoice_report():
    if request.method == 'POST':
    
        last_name = request.form.get('last_name')

        db_file = Path(__file__).resolve().parent.parent / "retail_app.db"

     
        conn = sqlite3.connect(db_file)

        query = """
        SELECT customer.customer_id, 
               customer.last_name, 
               invoice.total 
        FROM customer 
        INNER JOIN invoice 
        ON customer.customer_id = invoice.customer_id 
        WHERE customer.last_name = ?
        """

        df = pd.read_sql_query(query, conn, params=(last_name,))

        conn.close()

        if df.empty:
            customer_invoice_info = 'No information to report.'
        else:
            customer_invoice_info = df.to_html(index=False)

       
        return render_template('create_report.html', customer_invoice_info=customer_invoice_info)
    
  
    return render_template('create_report.html')

if __name__ == '__main__':
    app.run(debug=True)

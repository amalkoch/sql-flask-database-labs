from flask import Flask, render_template
import pandas as pd
import sqlite3
from pathlib import Path
from datetime import datetime
import matplotlib
matplotlib.use('Agg')  # Use non-interactive backend
import matplotlib.pyplot as plt
import os

app = Flask(__name__)

def get_db_connection():
    """Get database connection to retail_app.db"""
    db_file = Path(__file__).resolve().parent / "retail_app.db"
    return sqlite3.connect(db_file)

def calculate_age(dob_str):
    """Calculate age from date of birth string (YYYY-MM-DD format)"""
    if pd.isna(dob_str) or dob_str is None:
        return None
    try:
        birth_date = datetime.strptime(dob_str, '%Y-%m-%d')
        today = datetime.now()
        age = today.year - birth_date.year - ((today.month, today.day) < (birth_date.month, birth_date.day))
        return age
    except:
        return None

def get_customers():
    """Retrieve customer information from retail_app.db"""
    conn = get_db_connection()
    df = pd.read_sql_query("SELECT * FROM customer", conn)
    conn.close()
    
    # Calculate age for each customer
    df['age'] = df['dob'].apply(calculate_age)
    
    return df

@app.route("/customers")
def show_customers():
    """Display customer information in a table"""
    df = get_customers()
    html_table = df.to_html(classes="table table-striped", index=False)
    return render_template("customers.html", table=html_table)

def get_customer_age_brackets():
    """Retrieve customer data and group by age brackets"""
    conn = get_db_connection()
    df = pd.read_sql_query("SELECT * FROM customer", conn)
    conn.close()
    
    # Calculate age for each customer
    df['age'] = df['dob'].apply(calculate_age)
    
    # Remove rows with missing age
    df = df.dropna(subset=['age'])
    
    # Define age brackets
    def get_age_bracket(age):
        if age <= 20:
            return '0-20'
        elif age <= 30:
            return '21-30'
        elif age <= 40:
            return '31-40'
        elif age <= 50:
            return '41-50'
        elif age <= 60:
            return '51-60'
        else:
            return '60+'
    
    # Add age bracket column
    df['age_bracket'] = df['age'].apply(get_age_bracket)
    
    # Count customers in each bracket
    bracket_counts = df['age_bracket'].value_counts().sort_index()
    
    return bracket_counts

@app.route("/customer_age_chart")
def show_customer_age_chart():
    """Display bar chart of customers by age bracket"""
    # Get age bracket data
    bracket_counts = get_customer_age_brackets()
    
    # Create the bar chart
    plt.figure(figsize=(10, 6))
    bars = plt.bar(bracket_counts.index, bracket_counts.values, color='steelblue', edgecolor='black')
    
    # Add labels and title
    plt.xlabel('Age Brackets', fontsize=12, fontweight='bold')
    plt.ylabel('Number of Customers', fontsize=12, fontweight='bold')
    plt.title('Customer Distribution by Age Bracket', fontsize=14, fontweight='bold')
    
    # Add value labels on top of bars
    for bar in bars:
        height = bar.get_height()
        plt.text(bar.get_x() + bar.get_width()/2., height,
                f'{int(height)}',
                ha='center', va='bottom', fontsize=10)
    
    # Add grid for better readability
    plt.grid(axis='y', alpha=0.3, linestyle='--')
    
    # Adjust layout
    plt.tight_layout()
    
    # Save the chart
    chart_path = Path(__file__).resolve().parent / 'static' / 'customer_age_chart.png'
    chart_path.parent.mkdir(exist_ok=True)  # Create static directory if it doesn't exist
    plt.savefig(chart_path, dpi=300, bbox_inches='tight')
    plt.close()
    
    return render_template("customer_age_chart.html", chart_path='static/customer_age_chart.png')

if __name__ == "__main__":
    app.run(debug=True, port=5002)


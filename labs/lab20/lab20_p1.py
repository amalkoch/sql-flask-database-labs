import sqlite3
import matplotlib.pyplot as plt

conn = sqlite3.connect("retail_app.db")
cursor = conn.cursor()

def question1():
    
    cursor.execute("""
        SELECT invoice_number, SUM(total) AS invoice_total
        FROM invoice
        GROUP BY invoice_number
        ORDER BY invoice_number;
    """)

    rows = cursor.fetchall()

    invoice_numbers = []
    invoice_totals = []

    print("Invoice Totals:")
    for inv, tot in rows:
        print(inv, tot)
        invoice_numbers.append(str(inv))
        invoice_totals.append(tot)

   
    plt.bar(invoice_numbers, invoice_totals)
    plt.xlabel("Invoice Number")
    plt.ylabel("Invoice Total")
    plt.title("Invoice Totals by Invoice Number")
    plt.xticks(rotation=45)
    plt.tight_layout()
    plt.show()


question1()

import sqlite3
import matplotlib.pyplot as plt

conn = sqlite3.connect("retail_app.db")
cursor = conn.cursor()

def question2():
    cursor.execute("""
        SELECT name, price
        FROM product
        ORDER BY name;
    """)

    rows = cursor.fetchall()

    product_names = []
    product_prices = []

    print("Product Prices:")
    for name, price in rows:
        print(name, price)
        product_names.append(name)
        product_prices.append(price)

    x = list(range(len(product_names)))

    # WIDER chart so 45° labels fit
    plt.figure(figsize=(22, 8))

    plt.plot(x, product_prices, marker="o")
    plt.xticks(x, product_names, rotation=45, ha="right", fontsize=8)
    plt.xlabel("Product Name")
    plt.ylabel("Price")
    plt.title("Product Price by Product Name")
    plt.tight_layout()
    plt.show()

question2()
conn.close()


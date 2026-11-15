from flask import Flask, render_template, request
import sqlite3, matplotlib.pyplot as plt, io, base64, matplotlib
matplotlib.use('Agg')

app = Flask(__name__)

@app.route('/', methods=['GET','POST'])
def chart():
    chart_image = None
    if request.method == 'POST':
        conn = sqlite3.connect("retail_app.db")
        cur = conn.cursor()
        # product table columns: product_id, inventory
        cur.execute("SELECT product_id, inventory FROM product")
        data = cur.fetchall()
        conn.close()

        if data:
            codes, stock = zip(*data)
        else:
            codes, stock = [], []

        fig, ax = plt.subplots()
        ax.bar([str(c) for c in codes], stock)
        ax.set_xlabel("Product Code")
        ax.set_ylabel("Units in Stock")
        ax.set_title("Products Inventory")
        plt.xticks(rotation=45)

        buf = io.BytesIO()
        plt.savefig(buf, format="png", bbox_inches="tight")
        buf.seek(0)
        chart_image = "data:image/png;base64," + base64.b64encode(buf.getvalue()).decode()

    return render_template("bar_chart_inventory.html", chart_image=chart_image)

if __name__ == '__main__':
    app.run(debug=True, port=5001)

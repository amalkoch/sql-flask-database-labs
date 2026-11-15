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
        # units sold per product come from the invoice table
        cur.execute("""
            SELECT product_id, SUM(units)
            FROM invoice
            GROUP BY product_id
        """)
        data = cur.fetchall()
        conn.close()

        if data:
            codes, units = zip(*data)
        else:
            codes, units = [], []

        fig, ax = plt.subplots()
        ax.plot(range(len(codes)), units, marker="o")
        ax.set_xticks(range(len(codes)))
        ax.set_xticklabels([str(c) for c in codes], rotation=45)
        ax.set_xlabel("Product Code")
        ax.set_ylabel("Units Sold")
        ax.set_title("Units Sold vs Product Code")

        buf = io.BytesIO()
        plt.savefig(buf, format="png", bbox_inches="tight")
        buf.seek(0)
        chart_image = "data:image/png;base64," + base64.b64encode(buf.getvalue()).decode()

    return render_template("line_chart_units_sold.html", chart_image=chart_image)

if __name__ == '__main__':
    app.run(debug=True, port=5002)

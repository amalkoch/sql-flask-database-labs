from flask import Flask, render_template, request
import sqlite3, matplotlib.pyplot as plt, io, base64, matplotlib
matplotlib.use('Agg')

app = Flask(__name__)

@app.route('/', methods=['GET', 'POST'])
def chart():
    chart_image = None
    if request.method == 'POST':
        conn = sqlite3.connect("retail_app.db")
        cur = conn.cursor()
        cur.execute("SELECT gender, COUNT(*) FROM customer GROUP BY gender")
        data = cur.fetchall()
        conn.close()

        if data:
            genders, counts = zip(*data)
        else:
            genders, counts = [], []

        fig, ax = plt.subplots()
        ax.bar(genders, counts)
        ax.set_xlabel("Gender")
        ax.set_ylabel("Count")
        ax.set_title("Customer Gender")

        buf = io.BytesIO()
        plt.savefig(buf, format='png')
        buf.seek(0)
        chart_image = "data:image/png;base64," + base64.b64encode(buf.getvalue()).decode()

    return render_template('bar_chart_gender.html', chart_image=chart_image)

if __name__ == '__main__':
    app.run(debug=True)

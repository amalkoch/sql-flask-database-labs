from flask import Flask, render_template, request
import pandas as pd
from pathlib import Path
import sqlite3
import matplotlib.pyplot as plt
import io
import base64
import matplotlib
matplotlib.use('Agg')

app = Flask(__name__)

@app.route('/', methods=['GET', 'POST'])
def index():
    if request.method == 'POST':

        # Use pathlib to construct the database file path
        db_file = Path(__file__).resolve().parent.parent / "retail_app.db"
        
                # Connect to the database
        conn = sqlite3.connect(db_file)

        # Use Pandas to retrieve the customer information from the customer table
        query = "SELECT degree, COUNT(*) FROM employee GROUP BY degree"
        df = pd.read_sql_query(query, conn)

        # Close the database connection
        conn.close()

        # Extract the data from the retrieved rows
        degrees = []
        counts = []

        # Extract the data from the DataFrame
        data = df.to_dict('split')['data']
        for item in data:
            degrees.append(item[0])
            counts.append(item[1])

        # Plotting the line chart for employee degrees (fresh figure each request)
        plt.figure()
        plt.plot(degrees, counts, marker='o', linestyle='-', color='blue')

        # Adding labels and title
        plt.xlabel('Degree Type')
        plt.ylabel('Count')
        plt.title('Employee Degree Distribution')
        plt.xticks(rotation=30, ha='right')

        # Save the chart image to a buffer
        buffer = io.BytesIO()
        plt.savefig(buffer, format='png', bbox_inches='tight')
        plt.close()
        buffer.seek(0)

        # Convert the image buffer to base64 string
        image_base64 = base64.b64encode(buffer.getvalue()).decode()

        # Generate the chart image URL
        chart_image = f"data:image/png;base64,{image_base64}"

        # Render the template with the chart image URL
        return render_template('create_degree_line_chart.html', chart_image=chart_image)

    # Render the template with the initial form
    return render_template('create_degree_line_chart.html')

if __name__ == '__main__':
    app.run(debug=True)

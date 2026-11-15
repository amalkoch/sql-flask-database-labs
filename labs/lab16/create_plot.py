import matplotlib
matplotlib.use('Agg')
from flask import Flask, render_template, request
import matplotlib.pyplot as plt
import io
import base64

app = Flask(__name__)

@app.route('/', methods=['GET', 'POST'])
def create_plot():
    if request.method == 'POST':
        # Generate the plot
        fig, ax = plt.subplots()
        ax.plot([1, 2, 3], [4, 5, 6])
        ax.set_title('Sample Plot')

        # Save the plot to a bytes buffer
        buffer = io.BytesIO()
        plt.savefig(buffer, format='png')
        buffer.seek(0)

        # Encode the bytes as a base64 string
        img_base64 = base64.b64encode(buffer.getvalue()).decode()

        # Create the data URI string for embedding the image in the HTML
        img_uri = 'data:image/png;base64,' + img_base64

        # Pass the image URI to the HTML template
        return render_template('create_plot.html', img_uri=img_uri)

    # If the request method is GET, render the HTML template without the image
    return render_template('create_plot.html')

if __name__ == '__main__':
    app.run(debug=True)

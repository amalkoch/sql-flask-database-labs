from flask import Flask, request, render_template

app = Flask(__name__)

@app.route("/", methods=["GET", "POST"])
def process_form():
    if request.method == "POST":

        # 1. Textboxes
        f_name = request.form.get("fName")
        l_name = request.form.get("lName")
        password = request.form.get("pass")

        # 2. Radio button
        gender = request.form.get("gender")

        # 3. Checkboxes (getlist!)
        sports = request.form.getlist("sport")
        if len(sports) == 0:
            sports = ["None selected"]

        # 4. Dropdown (single)
        junk_food = request.form.get("junk")

        # 5. Textarea
        feedback = request.form.get("feedback")

        # OUTPUT HTML
        return f"""
        <h1>Form Results</h1>
        <table border="2" cellpadding="10">
            <tr><th>Field</th><th>Value</th></tr>

            <tr><td>First Name</td><td>{f_name}</td></tr>
            <tr><td>Last Name</td><td>{l_name}</td></tr>
            <tr><td>Password</td><td>{password}</td></tr>

            <tr><td>Gender</td><td>{gender}</td></tr>
            <tr><td>Favorite Sports</td><td>{", ".join(sports)}</td></tr>

            <tr><td>Favorite Junk Food</td><td>{junk_food}</td></tr>
            <tr><td>Feedback</td><td>{feedback}</td></tr>
        </table>
        """

    return render_template("lab18.html")

if __name__ == "__main__":
    app.run(debug=True)

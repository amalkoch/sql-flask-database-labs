from flask import Flask, render_template, request
import sqlite3
from pathlib import Path
import pandas as pd

app = Flask(__name__)

@app.route('/', methods=['GET', 'POST'])
def manager():
    if request.method == 'POST':
        # read the form data
        id = request.form.get('manager_id')

        # --------------------------------------------
        # old way of hard code path ignore
        #db_file = 'C:/Users/Abe/db_course/retail_app.db'
        # ---------------------------------------------
        # Assuming xxx.py is in the "desktop/db_course/lab14" folder
        #current_dir = Path(__file__).parent
        #print(current_dir.as_posix())

        # Assuming "db_course" is a folder inside "desktop"
        #parent_dir = current_dir.parent
        #print(parent_dir.as_posix())

        # Assuming db_file is the path to your SQLite database file inside "db_course"
        db_file = Path(__file__).parent.parent/"retail_app.db"
        #print(db_file.as_posix())

        # connect to the database
        conn = sqlite3.connect(db_file)
        
        query = "SELECT manager.manager_id, employee.first_name, employee.last_name FROM manager \
        INNER JOIN employee ON manager.employee_id = employee.employee_id WHERE manager.manager_id = ?"
        
        df = pd.read_sql_query(query, conn, params=(id,))
        conn.close()

        #print(len(df))
        if len(df) == 0:
            message = 'Manager with ID {} does not exist.'.format(id)
            #print(message)
            return render_template('get_manager.html', manager_info=message)
        else:
            manager_info = df.to_html(index=False)
            return render_template('get_manager.html', manager_info=manager_info)
    else:
        return render_template('get_manager.html')

if __name__ == '__main__':
    app.run(debug=True)

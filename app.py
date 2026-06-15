from flask import Flask
from flask import render_template

import sqlite3
import os

app = Flask(__name__)

#Finding the database path in Python and PhythonAnywhere
BASE_DIR = os.path.dirname(
    os.path.abspath(__file__)
)

DB_PATH = os.path.join(
    BASE_DIR,
    "race.db"
)



@app.route("/")
def home():
    return render_template("home.html")


#drivers route
@app.route("/drivers")
def drivers():

    conn = sqlite3.connect(
        DB_PATH
    )

    cursor = conn.cursor()

    cursor.execute(
        """
        SELECT *
        FROM drivers
        """
    )

    rows = cursor.fetchall()

    conn.close()

    return render_template(
        "drivers.html",
        drivers=rows
    )



#runs route
@app.route("/runs")
def runs():

    conn = sqlite3.connect(
        DB_PATH
    )

    cursor = conn.cursor()

    cursor.execute(
        """

        SELECT

        runs.id,

        drivers.name,

        courses.course_name,

        runs.run_time,

        runs.cones

        FROM runs

        JOIN drivers

        ON runs.driver_id = drivers.id

        JOIN courses

        ON runs.course_id = courses.id

        LIMIT 50

        """

    )

    rows = cursor.fetchall()

    conn.close()

    return render_template(
        "runs.html",
        runs=rows
    )


if __name__ == "__main__":
    app.run(debug=True)
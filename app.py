from flask import Flask
from flask import render_template
from flask import request
from flask import redirect


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

        

        """

    )

    rows = cursor.fetchall()

    conn.close()

    return render_template(
        "runs.html",
        runs=rows
    )




#add driver route
@app.route(
    "/add_driver",
    methods=["GET", "POST"]
)

def add_driver():

    if request.method == "POST":

        name = request.form["name"]

        license_type = request.form["license_type"]

        if len(name.strip()) == 0:

            return render_template(
                "add_driver.html",
                error="Driver name required."
            )

        conn = sqlite3.connect(DB_PATH)

        cursor = conn.cursor()

        cursor.execute(

            """

            SELECT *

            FROM drivers

            WHERE LOWER(name) = LOWER(?)

            """,

            (name,)

        )

        existing_driver = cursor.fetchone()

        if existing_driver:

            conn.close()

            return render_template(
                "add_driver.html",
                error="Driver already exists."
            )

        cursor.execute(

            """

            INSERT INTO drivers

            (

                name,

                license_type

            )

            VALUES (?,?)

            """,

            (

                name,

                license_type

            )

        )

        conn.commit()

        conn.close()

        return redirect("/drivers")

    return render_template(
        "add_driver.html",
        error=None
    )




#add run route
@app.route(
    "/add_run",
    methods=["GET", "POST"]
)

def add_run():
    if request.method == "POST":

        try:
            
            driver_id = int(request.form["driver_id"])
            course_id = int(request.form["course_id"])
            run_time = float(request.form["run_time"])
            cones = int(request.form["cones"])
        except ValueError:
            return "Invalid input. Please enter valid numbers."
        if run_time <= 0:
            return "Run time must be a non-negative number."
        if cones < 0:
            return "Number of cones must be a non-negative integer."



        conn = sqlite3.connect(DB_PATH)
        cursor = conn.cursor()

               
        cursor.execute(

            """

            INSERT INTO runs

            (

                driver_id,

                course_id,

                run_time,

                cones

            )

            VALUES (?,?,?,?)

            """,

            (

                driver_id,

                course_id,

                run_time,

                cones

            )

        )

        conn.commit()
        conn.close()
        return redirect("/runs")

        
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
      
    cursor.execute(
        "SELECT * FROM drivers"
    )
    drivers = cursor.fetchall()
            
    cursor.execute(
        "SELECT * FROM courses"
    )
    courses = cursor.fetchall()
    
    return render_template(
        "add_run.html",
        drivers=drivers,
        courses=courses
    )



#Search route
@app.route(
    "/search",
    methods=["GET", "POST"]
)
def search():

    results = []
    
    message = None
    
    if request.method == "POST":

        search_term = request.form[
            "search_term"
        ].strip()

        conn = sqlite3.connect(
            DB_PATH
        )

        cursor = conn.cursor()

        cursor.execute(

            """

            SELECT *

            FROM drivers

            WHERE name

            LIKE ?

            """,

            (

                f"%{search_term}%",

            )

        )

        results = cursor.fetchall()

        conn.close()
        
        if not results:
            message = "No drivers found."

    return render_template(

        "search.html",

        results=results,

        message=message

    )





if __name__ == "__main__":
    app.run(debug=True)
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


@app.route("/results")
def results():

    conn = sqlite3.connect(DB_PATH)

    cursor = conn.cursor()

    # Load drivers

    cursor.execute(
        """
        SELECT *
        FROM drivers
        """
    )

    drivers = cursor.fetchall()

    # Load runs with course names

    cursor.execute(
        """

        SELECT

        runs.driver_id,

        courses.course_name,

        runs.run_time,

        runs.cones

        FROM runs

        JOIN courses

        ON runs.course_id = courses.id

        """
    )

    runs = cursor.fetchall()

    conn.close()

    driver_results_list = []

    for driver_id, name, license_type in drivers:

        adjusted_time_a = None

        adjusted_time_b = None

        for d_id, course_name, run_time, cones in runs:

            if d_id == driver_id:

                current_adjusted_time = (
                    run_time + (cones * 2)
                )

                if course_name == "Course A":

                    if (
                        adjusted_time_a is None
                        or current_adjusted_time < adjusted_time_a
                    ):

                        adjusted_time_a = (
                            current_adjusted_time
                        )

                elif course_name == "Course B":

                    if (
                        adjusted_time_b is None
                        or current_adjusted_time < adjusted_time_b
                    ):

                        adjusted_time_b = (
                            current_adjusted_time
                        )

        # Determine best overall time

        if (
            adjusted_time_a is not None
            and adjusted_time_b is not None
        ):

            best_overall_time = min(
                adjusted_time_a,
                adjusted_time_b
            )

        elif adjusted_time_a is not None:

            best_overall_time = adjusted_time_a

        elif adjusted_time_b is not None:

            best_overall_time = adjusted_time_b

        else:

            best_overall_time = "N/A"

        driver_results_list.append(

            (

                driver_id,

                name,

                license_type,

                best_overall_time

            )

        )

    # Sort by best overall time

    sorted_driver_results = sorted(

        driver_results_list,

        key=lambda x:

        (

            x[3]

            if isinstance(
                x[3],
                (int, float)
            )

            else float("inf")

        )

    )

    return render_template(

        "results.html",

        results=sorted_driver_results

    )


@app.route("/cones")
def cones():

    conn = sqlite3.connect(
        DB_PATH
    )

    cursor = conn.cursor()

    # Load drivers

    cursor.execute(
        """
        SELECT *
        FROM drivers
        """
    )

    drivers = cursor.fetchall()

    # Load runs

    cursor.execute(
        """
        SELECT

        driver_id,

        cones

        FROM runs
        """
    )

    runs = cursor.fetchall()

    conn.close()

    cones_stats_list = []

    for driver_id, name, license_type in drivers:

        cones_counter = 0

        for d_id, cones in runs:

            if d_id == driver_id:

                cones_counter += cones

        if cones_counter > 0:

            cones_stats_list.append(

                (

                    name,

                    cones_counter,

                    "∆" * cones_counter

                )

            )

    return render_template(

        "cones.html",

        stats=cones_stats_list

    )


@app.route(
    "/remove_run",
    methods=["GET", "POST"]
)

def remove_run():

    message = None

    if request.method == "POST":

        try:

            run_id = int(
                request.form["run_id"]
            )

        except ValueError:

            return render_template(

                "remove_run.html",

                message="Run ID must be a number."

            )

        conn = sqlite3.connect(
            DB_PATH
        )

        cursor = conn.cursor()

        cursor.execute(

            """

            SELECT *

            FROM runs

            WHERE id = ?

            """,

            (run_id,)

        )

        run = cursor.fetchone()

        if run is None:

            conn.close()

            return render_template(

                "remove_run.html",

                message="Run ID not found."

            )

        cursor.execute(

            """

            DELETE FROM runs

            WHERE id = ?

            """,

            (run_id,)

        )

        conn.commit()

        conn.close()

        return render_template(

            "remove_run.html",

            message=f"Run {run_id} deleted successfully."

        )

    return render_template(

        "remove_run.html",

        message=None

    )



if __name__ == "__main__":
    app.run(debug=True)
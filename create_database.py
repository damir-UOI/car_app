import sqlite3

conn = sqlite3.connect(
    "race.db"
)

cursor = conn.cursor()

cursor.execute("""

CREATE TABLE IF NOT EXISTS drivers (

    id INTEGER PRIMARY KEY,

    name TEXT NOT NULL,

    license_type TEXT NOT NULL

)

""")



cursor.execute("""

CREATE TABLE IF NOT EXISTS courses (

    id INTEGER PRIMARY KEY,

    course_name TEXT NOT NULL

)

""")




cursor.execute("""

CREATE TABLE IF NOT EXISTS runs (

    id INTEGER PRIMARY KEY,

    driver_id INTEGER,

    course_id INTEGER,

    run_time REAL,

    cones INTEGER,

    FOREIGN KEY(driver_id)
        REFERENCES drivers(id),

    FOREIGN KEY(course_id)
        REFERENCES courses(id)

)

""")


conn.commit()

conn.close()

print("Database created.")    
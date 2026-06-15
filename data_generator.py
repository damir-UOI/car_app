import sqlite3
import random

from faker import Faker

fake = Faker()

conn = sqlite3.connect("race.db")
cursor = conn.cursor()

#drivers licese types
license_types = ["Learner", "Restricted", "Full"]

#generate random driver data
for i in range(20):

    cursor.execute(

        """

        INSERT INTO drivers

        (name, license_type)

        VALUES (?,?)

        """,

        (

            fake.name(),

            random.choice(
                license_types
            )

        )

    )

#courses
cursor.execute(

    """
    INSERT INTO courses
    (course_name)

    VALUES
    ('Course A')
    """

)

cursor.execute(

    """
    INSERT INTO courses
    (course_name)

    VALUES
    ('Course B')
    """

)

#generate random run data
for i in range(100):

    cursor.execute(

        """

        INSERT INTO runs

        (

            driver_id,

            course_id,

            run_time,

            cones

        )

        VALUES

        (?,?,?,?)

        """,

        (

            random.randint(1,20),

            random.randint(1,2),

            round(

                random.uniform(
                    45,
                    70
                ),

                2

            ),

            random.randint(0,5)

        )

    )


conn.commit()

conn.close()

print("Data generated.")


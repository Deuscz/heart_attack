import sqlite3

with sqlite3.connect("db.sqlite3") as db:
    cursor = db.cursor()
    cursor.execute("""create table heart_predicts(
        id integer primary key,
        name varchar(38),
        age real,
        sex real,
        cp real,
        trestbps real,
        chol real,
        fbs real,
        restecg real,
        thalach real,
        exang real,
        oldpeak real,
        slope real,
        ca real,
        thal real,
        result integer
    )""")
    cursor.close()

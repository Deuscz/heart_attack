from flask import g

ITEMS_PER_PAGE = 2


def delete_from_db(id_):
    cursor = g.db.cursor()
    cursor.execute(
        """delete from heart_predicts where id=?""",
        (id_,))
    g.db.commit()
    cursor.close()


def select_by_id(id_):
    cursor = g.db.cursor()
    cursor.execute(
        """select name, age, sex, cp, trestbps, chol, fbs, restecg, thalach, exang, oldpeak, slope, ca, thal, result from heart_predicts where id=?""",
        (id_,))
    row = cursor.fetchone()
    cursor.close()
    return row


def select_with_offset(p):
    cursor = g.db.cursor()
    cursor.execute(
        """select id, name, age, sex, cp, trestbps, chol, fbs, restecg, thalach, exang, oldpeak, slope, ca, thal, result from heart_predicts order by id limit ? offset ?""",
        (ITEMS_PER_PAGE, ITEMS_PER_PAGE * (p - 1)))
    rows = cursor.fetchall()
    cursor.close()
    return rows


def update_by_id(id_, name, age, sex, cp, trestbps, chol, fbs, restecg, thalach, exang, oldpeak, slope, ca, thal,
                 result):
    cursor = g.db.cursor()
    cursor.execute(
        """update heart_predicts set name=?, age=?, sex=?, cp=?, trestbps=?, chol=?, fbs=?, restecg=?, thalach=?, exang=?, oldpeak=?, slope=?, ca=?, thal=?, result=? where id=?""",
        (
            name, age, sex, cp, trestbps, chol, fbs, restecg, thalach, exang, oldpeak, slope, ca, thal, result,
            id_))
    g.db.commit()
    cursor.close()


def create_new(name, age, sex, cp, trestbps, chol, fbs, restecg, thalach, exang, oldpeak, slope, ca, thal, result):
    cursor = g.db.cursor()
    cursor.execute("""insert into heart_predicts (name, age, sex, cp, trestbps, chol, fbs, restecg, thalach, exang, oldpeak, slope, ca, thal, result)
    values (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)""", (
        name, age, sex, cp, trestbps, chol, fbs, restecg, thalach, exang, oldpeak, slope, ca, thal, result))
    id_ = cursor.lastrowid
    g.db.commit()
    cursor.close()
    return id_

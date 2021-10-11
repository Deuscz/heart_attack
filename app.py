import sqlite3
from flask import Flask, render_template, request, redirect, abort, g
from model import model, scaler

app = Flask(__name__)

ITEMS_PER_PAGE = 2


@app.before_request
def create_db():
    g.db = sqlite3.connect('db.sqlite3')


@app.teardown_request
def close_db(exc):
    g.db.close()


@app.route('/add', methods=["GET", "POST"])
def add():
    result = 'None'
    if request.method == 'POST':
        try:
            name = request.form.get('name', '')
            age = float(request.form.get('age', ''))
            sex = float(request.form.get('sex', ''))
            cp = float(request.form.get('cp', ''))
            trestbps = float(request.form.get('trestbps', ''))
            chol = float(request.form.get('chol', ''))
            fbs = float(request.form.get('fbs', ''))
            restecg = float(request.form.get('restecg', ''))
            thalach = float(request.form.get('thalach', ''))
            exang = float(request.form.get('exang', ''))
            oldpeak = float(request.form.get('oldpeak', ''))
            slope = float(request.form.get('slope', ''))
            ca = float(request.form.get('ca', ''))
            thal = float(request.form.get('thal', ''))
            value_list = scaler.transform(
                [[age, sex, cp, trestbps, chol, fbs, restecg, thalach, exang, oldpeak, slope, ca, thal]])
            result = int(model.predict(value_list)[0])
        except ValueError:
            return render_template('add.html', **request.form, result=result)
        cursor = g.db.cursor()
        cursor.execute("""insert into heart_predicts (name, age, sex, cp, trestbps, chol, fbs, restecg, thalach, exang, oldpeak, slope, ca, thal, result)
        values (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)""", (
            name, age, sex, cp, trestbps, chol, fbs, restecg, thalach, exang, oldpeak, slope, ca, thal, result))
        id_ = cursor.lastrowid
        g.db.commit()
        cursor.close()
        return redirect(f"/result/{id_}")
    return render_template('add.html', **request.form, result=result)


@app.route('/result/<id_>')
def result(id_):
    cursor = g.db.cursor()
    cursor.execute(
        """select name, age, sex, cp, trestbps, chol, fbs, restecg, thalach, exang, oldpeak, slope, ca, thal, result from heart_predicts where id=?""",
        (id_,))
    row = cursor.fetchone()
    cursor.close()
    if row is None:
        abort(404)
    name, age, sex, cp, trestbps, chol, fbs, restecg, thalach, exang, oldpeak, slope, ca, thal, result = row
    return render_template("result.html", result=result, id_=id_,
                           name=name,
                           age=age,
                           sex=sex,
                           cp=cp,
                           trestbps=trestbps,
                           chol=chol,
                           fbs=fbs,
                           restecg=restecg,
                           thalach=thalach,
                           exang=exang,
                           oldpeak=oldpeak,
                           slope=slope,
                           ca=ca,
                           thal=thal)


@app.route('/update/<id_>', methods=['GET', 'POST'])
def update(id_):
    cursor = g.db.cursor()
    if request.method == 'POST':
        try:
            name = request.form.get('name', '')
            age = float(request.form.get('age', ''))
            sex = float(request.form.get('sex', ''))
            cp = float(request.form.get('cp', ''))
            trestbps = float(request.form.get('trestbps', ''))
            chol = float(request.form.get('chol', ''))
            fbs = float(request.form.get('fbs', ''))
            restecg = float(request.form.get('restecg', ''))
            thalach = float(request.form.get('thalach', ''))
            exang = float(request.form.get('exang', ''))
            oldpeak = float(request.form.get('oldpeak', ''))
            slope = float(request.form.get('slope', ''))
            ca = float(request.form.get('ca', ''))
            thal = float(request.form.get('thal', ''))
            value_list = scaler.transform(
                [[age, sex, cp, trestbps, chol, fbs, restecg, thalach, exang, oldpeak, slope, ca, thal]])
            result = int(model.predict(value_list)[0])
        except ValueError:
            return render_template('add.html', **request.form, result=result)
        cursor.execute(
            """update heart_predicts set name=?, age=?, sex=?, cp=?, trestbps=?, chol=?, fbs=?, restecg=?, thalach=?, exang=?, oldpeak=?, slope=?, ca=?, thal=?, result=? where id=?""",
            (
                name, age, sex, cp, trestbps, chol, fbs, restecg, thalach, exang, oldpeak, slope, ca, thal, result,
                id_))
        g.db.commit()
        cursor.close()
        return redirect(f"/result/{id_}")
    cursor.execute(
        """select name, age, sex, cp, trestbps, chol, fbs, restecg, thalach, exang, oldpeak, slope, ca, thal, result from heart_predicts where id=?""",
        (id_,))
    row = cursor.fetchone()
    cursor.close()
    if row is None:
        abort(404)
    name, age, sex, cp, trestbps, chol, fbs, restecg, thalach, exang, oldpeak, slope, ca, thal, result = row
    return render_template("update.html",
                           result=result,
                           name=name,
                           age=age,
                           sex=sex,
                           cp=cp,
                           trestbps=trestbps,
                           chol=chol,
                           fbs=fbs,
                           restecg=restecg,
                           thalach=thalach,
                           exang=exang,
                           oldpeak=oldpeak,
                           slope=slope,
                           ca=ca,
                           thal=thal)


@app.route('/delete/<id_>')
def delete(id_):
    cursor = g.db.cursor()
    cursor.execute(
        """delete from heart_predicts where id=?""",
        (id_,))
    g.db.commit()
    cursor.close()
    return redirect(f"/")


@app.route("/")
def index():
    p = max(1, int(request.args.get('p', 1)))
    cursor = g.db.cursor()
    cursor.execute(
        """select id, name, age, sex, cp, trestbps, chol, fbs, restecg, thalach, exang, oldpeak, slope, ca, thal, result from heart_predicts order by id limit ? offset ?""",
        (ITEMS_PER_PAGE, ITEMS_PER_PAGE * (p - 1)))
    rows = cursor.fetchall()
    cursor.close()
    return render_template("index.html", rows=rows, next=p + 1, prev=p - 1, curr=p)


if __name__ == "__main__":
    app.run(debug=True)

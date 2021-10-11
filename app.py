from flask import Flask, render_template, request, redirect, abort, g
from model import model, scaler
from db import delete_from_db, select_by_id, update_by_id, create_new, select_with_offset
import sqlite3

app = Flask(__name__)


@app.before_request
def create_db():
    g.db = sqlite3.connect('db.sqlite3')


@app.teardown_request
def close_db(exc):
    g.db.close()


def get_args_list(request):
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
    return name, age, sex, cp, trestbps, chol, fbs, restecg, thalach, exang, oldpeak, slope, ca, thal


@app.route('/add', methods=["GET", "POST"])
def add():
    result = 'None'
    if request.method == 'POST':
        try:
            name, age, sex, cp, trestbps, chol, fbs, restecg, thalach, exang, oldpeak, slope, ca, thal = get_args_list(
                request)
            value_list = scaler.transform(
                [[age, sex, cp, trestbps, chol, fbs, restecg, thalach, exang, oldpeak, slope, ca, thal]])
            result = int(model.predict(value_list)[0])
        except ValueError:
            return render_template('add.html', **request.form, result=result)
        id_ = create_new(name, age, sex, cp, trestbps, chol, fbs, restecg, thalach, exang, oldpeak, slope, ca, thal,
                         result)
        return redirect(f"/result/{id_}")
    return render_template('add.html', **request.form, result=result)


@app.route('/result/<id_>')
def result(id_):
    row = select_by_id(id_)
    if row is None:
        abort(404)
    name, age, sex, cp, trestbps, chol, fbs, restecg, thalach, exang, oldpeak, slope, ca, thal, result = row
    return render_template("result.html",
                           result=result,
                           id_=id_,
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
    if request.method == 'POST':
        try:
            name, age, sex, cp, trestbps, chol, fbs, restecg, thalach, exang, oldpeak, slope, ca, thal = get_args_list(
                request)
            value_list = scaler.transform(
                [[age, sex, cp, trestbps, chol, fbs, restecg, thalach, exang, oldpeak, slope, ca, thal]])
            result = int(model.predict(value_list)[0])
        except ValueError:
            return render_template('add.html', **request.form, result=result)
        update_by_id(id_, name, age, sex, cp, trestbps, chol, fbs, restecg, thalach, exang, oldpeak, slope, ca, thal,
                     result)
        return redirect(f"/result/{id_}")
    row = select_by_id(id_)
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
    try:
        delete_from_db(id_)
    except:
        abort(404)
    return redirect(f"/")


@app.route("/")
def index():
    p = max(1, int(request.args.get('p', 1)))
    rows = select_with_offset(p)
    return render_template("index.html", rows=rows, next=p + 1, prev=p - 1, curr=p)


if __name__ == "__main__":
    app.run(debug=True)

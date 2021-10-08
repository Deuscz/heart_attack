from flask import Flask, render_template, request
from model import model, scaler

app = Flask(__name__)


@app.route('/', methods=["GET", "POST"])
def index():
    result = 'None'
    if request.method == 'POST':
        value_list = []
        for key in request.form:
            try:
                value_list.append(float(request.form.get(key, '')))
            except ValueError:
                pass
        value_list = scaler.transform([value_list])
        result = model.predict(value_list)[0]
    return render_template('index.html', **request.form, result=result)


if __name__ == "__main__":
    app.run(debug=True)

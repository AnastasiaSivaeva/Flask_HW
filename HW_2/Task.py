#Создать страницу, на которой будет форма для ввода имени и электронной почты, при отправке которой будет создан 
#cookie-файл с данными пользователя, а также будет произведено перенаправление на страницу приветствия, где будет 
#отображаться имя пользователя. На странице приветствия должна быть кнопка «Выйти», при нажатии на которую будет 
#удалён cookie-файл с данными пользователя и произведено перенаправление на страницу ввода имени и электронной почты

from flask import Flask
from flask import render_template

app = Flask(__name__)

@app.route('/form/')
def form_page():
    return render_template('form_page.html')

app.run(debug=True)

@app.route("/cookie_task/", methods=["GET", "POST"])
def cookie_task():

    if request.method == "POST":
        session['user_name'] = request.form.get("name")
        session['user_email'] = request.form.get("email")
        name = session['user_name']
        return redirect(url_for("hello_page"))

    return render_template("cookie_task.html")


@app.route("/cookie_task/hello_page/")
def hello_page():
    context = {
        "title": "Успешный вход",
        "name": session['user_name'],
    }

    return render_template("hello_page.html", **context)

@app.route("/cookie_task/logout/")
def logout():
    context = {
        "title": "Успешный выход",
        "name": session['user_name']
    }
    session.pop('user_name', None)
    session.pop('user_email', None)

    return render_template('logout.html', **context)


app.run(debug=True)
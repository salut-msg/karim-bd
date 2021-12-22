import os
from flask import *
import pygame as pg
app = Flask(__name__)
app.secret_key = os.urandom(128)
players = {
    "@Roma": 0,
    "@Rayan": 0,
    # TODO:  Тех, кто не админы, очень мало. Будет скучно :(
}
pg.init()
player = pg.mixer.Channel(0)
codes = """
CODE5739
BEST4247
WIN56142
GO654854
KARIM666
GAME2890
FIRE2576
LINUX210
ULTRA365
MEGA2560
SUPER190
RUNNER31
MAXIMUM7
WAR01945
EXTERME6
BATTLE60
YEAR1720
HACK3456
HYPER987
CRASH084
SECRET12
THEBEST1
JOKER154
CHEAT431
GETTER87
DEVELOP2
PROGRAM3
"""
used = []
state = []


@app.route("/admpass.html")
def redir_admin():
    psw = session.args.get("psw")
    if psw == "KarimChik":
        return redirect("/")
    else:
        return render_template("nosuch.html")

# Вход в аккаунт админа
@app.route("/admin-password/")
def admin_check():
    return f"""<form action="/admpass.html">
    <p>Введите пароль админа</p>
    <p>
    <input type="password" name="psw" placeholder="Введите пароль">
    <input type="submit">
    </p>
</form>"""


# Корень сайта
@app.route("/")
def index():
    if session["adm"] == "True":
        return render_template("admin-ui.html")
    if "username" not in session or session["username"] not in players:
        return render_template("login.html", **state)
    return render_template("game.html")


@app.route("/login/")
def login():
    uname = request.args.get("username")
    if uname == "@Admin":
        return redirect("/admin-password/")
    if uname in players:
        session["username"] = uname
        session.modified = True
        return redirect("/")
    else:
        return render_template("nosuch.html", username=uname)


@app.route("/api-check")
def api_check():
    code = request.args.get("code")
    if code == "BESTCODE":
        return "YES"
    elif code in used:
        return "NON"
    elif code in codes:
        used.append(code)
        return "YES"

app.run(host="0.0.0.0", port=8000)

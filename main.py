import os
from flask import *
import pygame as pg
app = Flask(__name__)
app.secret_key = os.urandom(128)
players = {
    "@Roma": 0,
    "@Rayan": 0,
    "@Timur": 0
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
""".strip().split()
used = []
state = 0
music = pg.mixer.Sound("bg.wav")


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
    return render_template("game.html", username=session["username"])


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
        return render_template("nosuch.html")


@app.route("/api/<act>")
def do_action(act):
    global state
    if act == "check":
        return api_check()
    if act == "start":
        music.play(-1)
        state = 1
    if act == "stop":
        music.stop()
        state = 0
    if act == "list":
        res = ""
        for i in players:
            res += i
            res += ": "
            res += str(players[i])
            res += "<br>"
        return res
    return "OK"


def api_check():
    code = request.args.get("code")
    uname = request.args.get("uname")
    if code == "BESTCODE":
        players[uname] += 60
        return "YES"
    elif code in used:
        return "NON"
    elif code in codes:
        used.append(code)
        players[uname] += sum(os.urandom(24)) % 20 + 1
        return "YES"

app.run(host="0.0.0.0", port=8000)

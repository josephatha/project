import os
from cs50 import SQL
from flask import Flask, flash, jsonify, redirect, render_template, request, session
from flask_session import Session
from werkzeug.security import check_password_hash, generate_password_hash

# Configure application
app = Flask(__name__)

app.config["SESSION_PERMANENT"] = False
app.config["SESSION_TYPE"] = "filesystem"
Session(app)

db = SQL("sqlite:///soccer.db")

# Ensure templates are auto-reloaded
app.config["TEMPLATES_AUTO_RELOAD"] = True


@app.route("/", methods=["GET", "POST"])
def index():
    return render_template("index.html")

@app.route("/laliga", methods=["GET", "POST"])
def laliga():
    if request.method == "GET":
        rows = db.execute("SELECT * FROM laliga")

        return render_template("laliga.html", rows=rows)

@app.route("/premiere", methods=["GET", "POST"])
def premiere():
    if request.method == "GET":
        rows = db.execute("SELECT * FROM premiere")

    return render_template("premiere.html", rows=rows)



@app.route("/seriea", methods=["GET", "POST"])
def serie():
    if request.method == "GET":
        rows = db.execute("SELECT * FROM seriea")

    return render_template("seriea.html", rows=rows)



@app.route("/one", methods=["GET", "POST"])
def one():
    if request.method == "GET":
        rows = db.execute("SELECT * FROM one")

    return render_template("one.html", rows=rows)

@app.route("/bundes", methods=["GET", "POST"])
def bundes():
     if request.method == "GET":
        rows = db.execute("SELECT * FROM bundesliga")

        return render_template("bundes.html", rows=rows)

@app.route("/register", methods=["GET", "POST"])
def register():
    """Register user"""
    if request.method == 'POST':
        name = request.form.get("username")
        password = request.form.get("password")
        contra = request.form.get("contra")

        repetido = db.execute("SELECT username FROM users WHERE username=:username", username=name)

        if len(repetido) > 0:
            return render_template("register.html", msg = "username is already used")

        flag = False;

        for char in password:
            if char.isdigit() == True:
                flag = True;


        if flag == False:
            return render_template("register.html", msg = "information requiered")

        hash = generate_password_hash(password)

        if password == contra:
            db.execute("INSERT INTO users (username, password) VALUES (:name, :password)", name=name, password=hash)
            return redirect("/login")
        else:
            return render_template("register.html", msg = "passwords do not match")

        # return render_template("register.html")
    else:
        return render_template("register.html")

@app.route("/login", methods=["GET", "POST"])
def login():
    """Log user in"""
    session.clear()

    if request.method == "POST":
        # Ensure username was submitted
        if not request.form.get("username"):
            return render_template("login.html", msg = "must provide username")


        # Ensure password was submitted
        elif not request.form.get("password"):
            return render_template("login.html", msg = "must provide password")

        rows = db.execute("SELECT * FROM users WHERE username = ?", request.form.get("username"))

        print(rows)

        if len(rows) != 1 or not check_password_hash(
            rows[0]["password"], request.form.get("password")
        ):
            return render_template("login.html", msg = "Invalid username/password")

        session["user_id"] = rows[0]["id"]

        return redirect("/general")
    else:
        return render_template("login.html")

@app.route("/general", methods=["GET", "POST"])
def general():
    return render_template("general.html")

@app.route("/logout")
def logout():
    session.clear()
    return redirect("/")

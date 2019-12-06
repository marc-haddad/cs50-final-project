import os
import mpld3 as mpld3
from matplotlib import pyplot as plt
from cs50 import SQL
from flask import Flask, flash, jsonify, redirect, render_template, request, session
from flask_session import Session
from tempfile import mkdtemp
from werkzeug.exceptions import default_exceptions, HTTPException, InternalServerError
from werkzeug.security import check_password_hash, generate_password_hash

from helpers import apology, login_required
from ineq_mat_plot import graph, line_plot, d3_plot

D3_LIST = []

# Configure application
app = Flask(__name__)

# Ensure templates are auto-reloaded
app.config["TEMPLATES_AUTO_RELOAD"] = True

# Ensure responses aren't cached
@app.after_request
def after_request(response):
    response.headers["Cache-Control"] = "no-cache, no-store, must-revalidate"
    response.headers["Expires"] = 0
    response.headers["Pragma"] = "no-cache"
    return response


# Configure session to use filesystem (instead of signed cookies)
app.config["SESSION_FILE_DIR"] = mkdtemp()
app.config["SESSION_PERMANENT"] = False
app.config["SESSION_TYPE"] = "filesystem"
Session(app)

# Configure CS50 Library to use SQLite database
db = SQL("sqlite:///resources/ineq.db")


@app.route("/")
@login_required
def index():
    plt.clf()
    plt.cla()
    plt.close()
    if (len(D3_LIST) < 1):
        return redirect("/selection")
    else:
        custom_graph = graph(D3_LIST)
        return render_template("index.html", custom_graph=custom_graph)

@app.route("/selection", methods=["GET", "POST"])
@login_required
def selection():
    # Make graph customization selections
    if request.method == "GET":
        D3_LIST.clear()
        return render_template("selection.html")

    elif request.method == "POST":
        states_form = request.form.getlist("states")

        if not states_form:
            return apology("How did you even get this error?!")

        else:
            for state in states_form:
                D3_LIST.append(state)
            return redirect('/')


@app.route("/about")
def about():
    return render_template("about.html")

@app.route("/login", methods=["GET", "POST"])
def login():

    # Forget any user_id
    session.clear()

    # User reached route via POST (as by submitting a form via POST)
    if request.method == "POST":

        # Ensure username was submitted
        if not request.form.get("username"):
            return apology("must provide username", 403)

        # Ensure password was submitted
        elif not request.form.get("password"):
            return apology("must provide password", 403)

        # Query database for username
        rows = db.execute("SELECT * FROM users WHERE username = :username",
                          username=request.form.get("username"))

        # Ensure username exists and password is correct
        if len(rows) != 1 or not check_password_hash(rows[0]["hash"], request.form.get("password")):
            return apology("invalid username and/or password", 403)

        # Remember which user has logged in
        session["user_id"] = rows[0]["user_id"]

        # Redirect user to home page
        return redirect("/selection")

    # User reached route via GET (as by clicking a link or via redirect)
    else:
        return render_template("login.html")


@app.route("/logout")
def logout():
    """Log user out"""

    # Forget any user_id
    session.clear()

    # Redirect user to login form
    return redirect("/")


@app.route("/register", methods=["GET", "POST"])
def register():
    """Register user"""
    if request.method == "POST":
    # Require user to input a username as a text field whose name is username
        if not request.form.get("username"):
            return apology("you must provide a username", 400)

        # Ensure password and confirmation was submitted
        elif not request.form.get("password"):
            return apology("you must provide a password", 400)

        elif request.form.get("password") != request.form.get("confirmation"):
            return apology("passwords must match", 400)

        rows = db.execute("SELECT * FROM users WHERE username = :username",
                          username=request.form.get("username"))
        if len(rows) == 1:
            return apology("sorry, that username is already taken", 400)
        else:
            username = request.form.get('username')
            password = generate_password_hash(request.form.get('password'), method='pbkdf2:sha256', salt_length=8)
            newuser = db.execute("INSERT INTO users ('username', 'hash') VALUES (:username, :hash)",
                                 username=username, hash=password)
            return redirect("/login")
    # code to reset id count: sqlite3 update sqlite_sequence set seq = 0 where name = 'users'
    else:
        return render_template("register.html")


def errorhandler(e):
    """Handle error"""
    if not isinstance(e, HTTPException):
        e = InternalServerError()
    return apology(e.name, e.code)


# Listen for errors
for code in default_exceptions:
    app.errorhandler(code)(errorhandler)

from flask import Blueprint, render_template, abort, request, redirect, url_for, flash, session, g
import os
import psycopg2
from werkzeug.security import generate_password_hash, check_password_hash
import functools
from dotenv import load_dotenv, find_dotenv

load_dotenv(find_dotenv())
bp = Blueprint("auth", __name__, url_prefix="/auth")

def get_db_connection():
    return psycopg2.connect(
        port=5432,
        host=os.getenv('HOST'),
        dbname=os.getenv('DBNAME'),
        user=os.getenv('DB_USERNAME'),
        password=os.getenv('DB_PASSWORD')
    )

def login_required(view):
    @functools.wraps(view)
    def wrapped_view(**kwargs):
        if g.user is None:
            return redirect(url_for("auth.login"))
        return view(**kwargs)
    return wrapped_view

@bp.before_app_request
def load_logged_in_user():
    user_id = session.get("user_id")

    if user_id is None:
        g.user = None
    else:
        conn = get_db_connection()
        cur = conn.cursor()

        cur.execute("SELECT id, username FROM users WHERE id = %s", (user_id,))
        user = cur.fetchone()

        cur.close()
        conn.close()

        if user:
            g.user = {"id": user[0], "username": user[1]}
        else:
            g.user = None

@bp.route("/register", methods=["GET", "POST"])
def register():
    if request.method == "POST":
        username = request.form["username"]
        password = request.form["password"]

        password_hash = generate_password_hash(password)

        conn = get_db_connection()
        cur = conn.cursor()

        cur.execute("SELECT id FROM users WHERE username = %s", (username,))
        existing_user = cur.fetchone()

        if existing_user:
            flash("User with this username already exists!")
            cur.close()
            conn.close()
            return redirect(url_for("auth.register"))

        cur.execute("INSERT INTO users (username, password_hash) VALUES (%s, %s)", (username, password_hash))

        conn.commit()
        cur.close()
        conn.close()

        flash("Registration is successful. Please log in!")
        return redirect(url_for("auth.login"))
    return render_template("auth/register.html")

@bp.route("/login", methods=["GET", "POST"])
def login():
    if request.method == "POST":
        username = request.form["username"]
        password = request.form["password"]

        conn = get_db_connection()
        cur = conn.cursor()

        cur.execute("SELECT id, username, password_hash FROM users WHERE username = %s", (username,))
        user = cur.fetchone()

        cur.close()
        conn.close()

        if user is None:
            flash("User can't be found.")
            return redirect(url_for("auth.register"))
        elif not check_password_hash(user[2], password):
            flash("Wrong password.")
            return redirect(url_for("auth.login"))
        else:
            session.clear()
            session["user_id"] = user[0]
            return redirect(url_for("blog.home"))

    return render_template("auth/login.html")

@bp.route("/logout")
def logout():
    session.clear()
    flash("You have been logged out.")
    return redirect(url_for("blog.home"))
from flask import Blueprint, render_template, request, redirect, url_for, flash, session, g
from werkzeug.security import generate_password_hash, check_password_hash
from .querys import get_user_by_id, get_user_by_username, create_user
from .utils import user_to_g

bp = Blueprint("auth", __name__, url_prefix="/auth")

@bp.before_app_request
def load_logged_in_user():
	user_id = session.get("user_id")

	if user_id is None:
		g.user = None
	else:
		user = get_user_by_id(user_id)
		g.user = user_to_g(user)

@bp.route("/register", methods=["GET", "POST"])
def register():
	if request.method == "POST":
		username = request.form["username"]
		password = request.form["password"]

		if get_user_by_username(username):
			flash("User with this username already exists!")
			return redirect(url_for("auth.register"))

		password_hash = generate_password_hash(password)
		create_user(username, password_hash)

		flash("Registration is successful. Please log in!")
		return redirect(url_for("auth.login"))

	return render_template("auth/register.html")


@bp.route("/login", methods=["GET", "POST"])
def login():
	if request.method == "POST":
		username = request.form["username"]
		password = request.form["password"]

		user = get_user_by_username(username)

		if user is None:
			flash("User can't be found.")
			return redirect(url_for("auth.register"))

		if not check_password_hash(user[2], password):
			flash("Wrong password.")
			return redirect(url_for("auth.login"))

		session.clear()
		session["user_id"] = user[0]
		return redirect(url_for("blog.home"))

	return render_template("auth/login.html")


@bp.route("/logout")
def logout():
	session.clear()
	flash("You have been logged out.")
	return redirect(url_for("blog.home"))
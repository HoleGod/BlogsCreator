from flask import Blueprint, render_template, abort, request, redirect, url_for

bp = Blueprint("other", __name__, url_prefix="/other")

@bp.route("/about")
def about():
    return render_template("other/about.html")

@bp.route("/politics")
def politics():
    return render_template("other/politics.html")
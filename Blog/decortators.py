from functools import wraps
from flask import Blueprint, render_template, abort, request, redirect, url_for, current_app, flash, g

def login_required(view):
	@wraps(view)
	def wrapper(*args, **kwargs):
		if g.user is None:
			flash("You must log in to create posts!")
			return redirect(url_for("auth.login"))
		return view(*args, **kwargs)
	return wrapper
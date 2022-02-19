from flask import Blueprint, render_template, request, redirect, url_for
from werkzeug.security import generate_password_hash
from flask_login import login_user, logout_user

from forms import LoginForm, SignupForm
from models import User
from db import db

main_views = Blueprint("main", __name__)


@main_views.route("/")
def index():
    return render_template("index.html")


@main_views.route("/login", methods=["GET", "POST"])
def login():
    form = LoginForm()
    if form.validate_on_submit():
        user = User.query.filter_by(email=form.email.data).first()
        login_user(user)
        next_url = request.args.get("next")
        return redirect(next_url or url_for("main.index"))

    return render_template("registration/login.html", form=form)


@main_views.route("/register", methods=["GET", "POST"])
def register():
    form = SignupForm()
    if form.validate_on_submit():
        user = User(
            email=form.email.data,
            password=generate_password_hash(form.password.data)
        )
        db.session.add(user)
        db.session.commit()
        return redirect(url_for("main.login"))

    return render_template("registration/signup.html", form=form)


@main_views.route("/logout")
def logout():
    logout_user()
    return redirect(url_for("main.login"))

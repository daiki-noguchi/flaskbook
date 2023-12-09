from typing import Union

import werkzeug
from flask import Blueprint, flash, redirect, render_template, request, url_for
from flask_login import login_user, logout_user
from flask_webapp.app import db
from flask_webapp.auth.forms import LoginForm, SignUpForm
from flask_webapp.crud.models import User

auth = Blueprint(
    "auth",
    __name__,
    template_folder="templates",
    static_folder="static",
)


@auth.route("/signup", methods=["GET", "POST"])
def signup() -> Union[str, "werkzeug.wrappers.response.Response"]:
    form = SignUpForm()
    if form.validate_on_submit():
        user = User(
            username=form.username.data,
            email=form.email.data,
            password=form.password.data,
        )
        if user.is_duplicate_email():
            flash("指定のメールアドレスは登録済みです")
            return redirect(url_for("auth.signup"))
        db.session.add(user)
        db.session.commit()
        login_user(user)
        next_ = request.args.get("next")
        if next_ is None or not next_.startswith("/"):
            next_ = url_for("detector.index")
        return redirect(next_)
    return render_template("auth/signup.html", form=form)


@auth.route("/login", methods=["GET", "POST"])
def login() -> Union[str, "werkzeug.wrappers.response.Response"]:
    form = LoginForm()
    if form.validate_on_submit():
        user = User.query.filter_by(email=form.email.data).first()
        if user is not None and user.verify_password(form.password.data):
            login_user(user)
            return redirect(url_for("detector.index"))
        flash("メールアドレスかパスワードか不正です")
    return render_template("auth/login.html", form=form)


@auth.route("/logout")
def logout() -> "werkzeug.wrappers.response.Response":
    logout_user()
    return redirect(url_for("auth.login"))

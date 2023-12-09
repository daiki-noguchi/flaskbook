from flask import Blueprint, redirect, render_template, url_for
from flask_login import login_required
from flask_webapp.app import db
from flask_webapp.crud.forms import UserForm
from flask_webapp.crud.models import User

crud = Blueprint(
    "crud",
    __name__,
    template_folder="templates",
    static_folder="static",
)


@crud.route("/")
@login_required
def index():
    return render_template("crud/index.html")


@crud.route("/sql")
@login_required
def sql():
    db.session.query(User).all()
    return "コンソールログを確認"


@crud.route("/users/new", methods=["GET", "POST"])
@login_required
def create_user():
    form = UserForm()
    if form.validate_on_submit():
        user = User(
            username=form.username.data,
            email=form.email.data,
            password=form.password.data,
        )
        db.session.add(user)
        db.session.commit()
        return redirect(url_for("crud.users"))
    return render_template("crud/create.html", form=form)


@crud.route("/users")
@login_required
def users():
    """ユーザーの一覧を取得する"""
    users = User.query.all()
    return render_template("crud/index.html", users=users)


@crud.route("/users/<user_id>", methods=["GET", "POST"])
@login_required
def edit_user(user_id):
    user = User.query.get(user_id)
    form = UserForm(obj=user)
    if form.validate_on_submit():
        form.populate_obj(user)
        db.session.commit()
        return redirect(url_for("crud.users"))
    return render_template("crud/edit.html", user=user, form=form)


@crud.route("/users/<user_id>/delete", methods=["POST"])
@login_required
def delete_user(user_id):
    user = User.query.filter_by(id=user_id).first()
    db.session.delete(user)
    db.session.commit()
    return redirect(url_for("crud.users"))

from datetime import datetime
from typing import Any

from flask_login import UserMixin
from flask_webapp.app import db, login_manager
from werkzeug.security import check_password_hash, generate_password_hash


class User(db.Model, UserMixin):  # type: ignore
    __tablename__ = "users"
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(64), index=True)
    email = db.Column(db.String(120), unique=True, index=True)
    password_hash = db.Column(db.String(128))
    created_at = db.Column(db.DateTime, default=datetime.now)
    updated_at = db.Column(db.DateTime, default=datetime.now, onupdate=datetime.now)

    @property
    def password(self) -> str:
        raise AttributeError("読み取り不可")

    @password.setter
    def password(self, password: str) -> None:
        self.password_hash = generate_password_hash(password)

    def verify_password(self, password: str) -> bool:
        return check_password_hash(self.password_hash, password)

    def is_duplicate_email(self) -> bool:
        return User.query.filter_by(email=self.email).first() is not None


@login_manager.user_loader
def load_user(user_id: int) -> Any:
    return User.query.get(user_id)

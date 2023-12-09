from flask_wtf import FlaskForm
from wtforms import PasswordField, StringField, SubmitField
from wtforms.validators import DataRequired, Email, length


class UserForm(FlaskForm):  # type: ignore[misc]
    username = StringField(
        "Username",
        validators=[
            DataRequired(message="ユーザー名は必須です"),
            length(max=30, message="30文字以内で入力してください"),
        ],
    )
    email = StringField(
        "Email",
        validators=[
            DataRequired(message="メールアドレスは必須です"),
            Email(message="メールアドレスの形式で入力してください"),
        ],
    )
    password = PasswordField(
        "Password", validators=[DataRequired(message="パスワードは必須です")]
    )
    submit = SubmitField("Register")

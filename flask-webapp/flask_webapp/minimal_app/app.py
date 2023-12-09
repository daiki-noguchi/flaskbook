import logging
import os

import werkzeug
from email_validator import EmailNotValidError, validate_email
from flask import (
    Flask,
    flash,
    make_response,
    redirect,
    render_template,
    request,
    session,
    url_for,
)
from flask_mail import Mail, Message

app = Flask(__name__)

app.config["SECRET_KEY"] = "2AZSMss3p5QPbcY2hBsJ"
app.logger.setLevel(logging.DEBUG)
# リダイレクトを中断しないようにする
app.config["DEBUG_TB_INTERCEPT_REDIRECTS"] = False

# Mailクラスのコンフィグを追加する
app.config["MAIL_SERVER"] = os.environ.get("MAIL_SERVER")
app.config["MAIL_PORT"] = os.environ.get("MAIL_PORT")
app.config["MAIL_USE_TLS"] = os.environ.get("MAIL_USE_TLS")
app.config["MAIL_USERNAME"] = os.environ.get("MAIL_USERNAME")
app.config["MAIL_PASSWORD"] = os.environ.get("MAIL_PASSWORD")
app.config["MAIL_DEFAULT_SENDER"] = os.environ.get("MAIL_DEFAULT_SENDER")
mail = Mail(app)


@app.route("/")
def index() -> str:
    return "Hello, Flaskbook!"


@app.route("/hello/<name>", methods=["GET", "POST"], endpoint="hello-endpoint")
def hello(name: str) -> str:
    return f"Hello, {name}!"


@app.route("/name/<name>")
def show_name(name: str) -> str:
    return render_template("index.html", name=name)


with app.test_request_context():
    print(url_for("index"))
    print(url_for("hello-endpoint", name="world"))
    print(url_for("show_name", name="ichiro", page="1"))


@app.route("/contact")
def contact() -> "werkzeug.wrappers.response.Response":
    response = make_response(render_template("contact.html"))
    response.set_cookie("flaskbook key", "flaskbook value")
    session["username"] = "flaskbook"
    return response


@app.route("/contact/complete", methods=["GET", "POST"])
def contact_complete() -> str | "werkzeug.wrappers.response.Response":
    if request.method == "POST":
        # フォームの値を取得する
        username = request.form["username"]
        email = request.form["email"]
        description = request.form["description"]

        # 入力チェック
        is_valid = True
        if not username:
            flash("ユーザ名は必須です")
            is_valid = False

        if not email:
            flash("メールアドレスは必須です")
            is_valid = False

        try:
            validate_email(email)
        except EmailNotValidError:
            flash("メールアドレスの形式で入力してください")
            is_valid = False

        if not description:
            flash("問い合わせ内容は必須です")
            is_valid = False

        if not is_valid:
            return redirect(url_for("contact"))

        # メール送信
        send_email(
            email,
            "お問い合わせありがとうございました。",
            "contact_mail",
            username=username,
            description=description,
        )

        # contactエンドポイントへリダイレクトする
        return redirect(url_for("contact_complete"))

    return render_template("contact_complete.html")


def send_email(to: str, subject: str, template: str, **kwargs: str) -> None:
    """メールを送信する関数"""
    msg = Message(subject, recipients=[to])
    msg.body = render_template(template + ".txt", **kwargs)
    msg.html = render_template(template + ".html", **kwargs)
    mail.send(msg)

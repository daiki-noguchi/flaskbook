from flask_wtf.file import FileAllowed, FileField, FileRequired
from flask_wtf.form import FlaskForm
from wtforms.fields.simple import SubmitField


class UploadImageForm(FlaskForm):  # type: ignore[misc]
    image = FileField(
        validators=[
            FileRequired("画像ファイルを指定してください。"),
            FileAllowed(["png", "jps", "jpes"], "サポートされていない画像形式です。"),
        ]
    )
    submit = SubmitField("アップロード")

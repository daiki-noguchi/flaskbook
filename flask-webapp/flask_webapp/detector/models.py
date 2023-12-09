from flask_webapp.app import db


class UserImage(db.Model):
    __tablename__ = 'user_images'

    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'))
    image_url = db.Column(db.String(500))

    user = db.relationship('User', backref=db.backref('images', lazy=True))

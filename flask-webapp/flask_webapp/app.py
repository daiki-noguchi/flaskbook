from flask import Flask
from flask_login import LoginManager
from flask_migrate import Migrate
from flask_sqlalchemy import SQLAlchemy
from flask_webapp.config import config
from flask_wtf.csrf import CSRFProtect

db = SQLAlchemy()
csrf = CSRFProtect()
login_manager = LoginManager()
login_manager.login_view = 'auth.signup'
login_manager.login_message = ''

def create_app(config_key):
    app = Flask(__name__)

    from flask_webapp.crud import views as crud_views

    app.config.from_object(config[config_key])
    db.init_app(app)
    csrf.init_app(app)
    login_manager.init_app(app)
    Migrate(app, db)
    app.register_blueprint(crud_views.crud, url_prefix="/crud")

    from flask_webapp.auth import views as auth_views

    app.register_blueprint(auth_views.auth, url_prefix="/auth")
    return app

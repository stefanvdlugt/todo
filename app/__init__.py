import os
from config import Config
from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from flask_login import LoginManager

db = SQLAlchemy()
migrate = Migrate()
login = LoginManager()

def create_app(config_class=Config):
    app = Flask(__name__)
    app.config.from_object(config_class)

    db.init_app(app)
    migrate.init_app(app,db)

    login.login_view = 'auth.login'
    login.init_app(app)

    from app.main import main
    app.register_blueprint(main)

    from app.auth import auth
    app.register_blueprint(auth,url_prefix='/auth')

    return app

from app import models
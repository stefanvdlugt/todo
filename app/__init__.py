import os
from config import Config
from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from flask_login import LoginManager
from flask_mail import Mail
from flask_apscheduler import APScheduler

db = SQLAlchemy()
migrate = Migrate()
login = LoginManager()
login.login_view = 'auth.login'
login.login_message = 'Please log in to access this page.'
mail = Mail()
scheduler = APScheduler()

def create_app(config_class=Config):
    app = Flask(__name__)
    app.config.from_object(config_class)

    db.app = app
    db.init_app(app)
    migrate.init_app(app,db)

    from app.main import main
    app.register_blueprint(main)

    from app.auth import auth
    app.register_blueprint(auth,url_prefix='/auth')

    from app.admin import admin
    app.register_blueprint(admin,url_prefix='/admin')

    login.init_app(app)

    mail.init_app(app)

    scheduler.init_app(app)
    scheduler.start()

    return app

from app import models, tasks

import os
from dotenv import load_dotenv

basedir = os.path.abspath(os.path.dirname(__file__))
load_dotenv(os.path.join(basedir,'.env'))

class Config(object):
    
    SERVER_NAME = os.environ.get('SERVER_NAME')

    SECRET_KEY = os.environ.get('SECRET_KEY', 'secret-key')

    SQLALCHEMY_DATABASE_URI = os.environ.get('DATABASE_URL', 'sqlite:///'+os.path.join(basedir,'app.db'))
    SQLALCHEMY_TRACK_MODIFICATIONS = False

    MAIL_SERVER = os.environ.get('MAIL_SERVER')
    MAIL_PORT = int(os.environ.get('MAIL_PORT') or 25)
    MAIL_USE_TLS = os.environ.get('MAIL_USE_TLS','').lower() in ['1', 'true', 'yes', 'y']
    MAIL_USERNAME = os.environ.get('MAIL_USERNAME')
    MAIL_PASSWORD = os.environ.get('MAIL_PASSWORD')
    MAIL_FROM = os.environ.get('MAIL_FROM')

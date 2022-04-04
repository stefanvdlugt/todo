import os
import urllib.parse
from dotenv import load_dotenv
from uuid import uuid4

basedir = os.environ.get('BASEDIR',os.path.abspath(os.path.dirname(__file__)))
load_dotenv(os.path.join(basedir,'todo.env'))

def generate_db_uri():
    if os.environ.get('MYSQL_HOST'):
        # Use MySQL database
        host = os.environ.get('MYSQL_HOST')
        user = os.environ.get('MYSQL_USER', 'todo')
        passwd = os.environ.get('MYSQL_PASSWORD', 'password')
        dbname = os.environ.get('MYSQL_DATABASE', 'todo')
        passwd_enc = urllib.parse.quote_plus(passwd)
        return f'mysql+pymysql://{user}:{passwd_enc}@{host}/{dbname}'
    else:
        # Use SQLite database
        dbpath = os.environ.get('SQLITE_DATABASE_PATH',os.path.join(basedir, 'app.db'))
        return 'sqlite:///' + dbpath

def get_secret_key():
    # Try reading secret key from environment
    key = os.environ.get('SECRET_KEY')
    if not key:
        # If a secret key is not defined in the environment, try reading one
        # from a file, and otherwise, generate a key and store it in a file. 
        keyfile = os.path.join(basedir,'secret_key')
        if os.path.isfile(keyfile):
            with open(keyfile,'r') as f:
                key = f.read().rstrip('\n')
        else:
            key = str(uuid4())
            um = os.umask(0o077) # don't give other users read access
            with open(keyfile,'w') as f:
                f.write(key)
            os.umask(um) # revert umask to original
    return key

                            
class Config(object):
    
    SERVER_NAME = os.environ.get('SERVER_NAME')

    SECRET_KEY = get_secret_key()

    SQLALCHEMY_DATABASE_URI = generate_db_uri()
    SQLALCHEMY_TRACK_MODIFICATIONS = False

    MAIL_SERVER = os.environ.get('MAIL_SERVER')
    MAIL_PORT = int(os.environ.get('MAIL_PORT') or 25)
    MAIL_USE_TLS = os.environ.get('MAIL_USE_TLS','').lower() in ['1', 'true', 'yes', 'y']
    MAIL_USERNAME = os.environ.get('MAIL_USERNAME')
    MAIL_PASSWORD = os.environ.get('MAIL_PASSWORD')
    MAIL_FROM = os.environ.get('MAIL_FROM')

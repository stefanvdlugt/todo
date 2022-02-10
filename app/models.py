from app import db, login
from werkzeug.security import generate_password_hash, check_password_hash
from flask_login import UserMixin
import jwt
from flask import current_app

from time import time as time_
from os import urandom

def keygen():
    '''
    Returns a 16 bytes string.
    The first 6 bytes give a timestamp (# milliseconds since 1 Jan 1970),
    and the last 10 bytes are random.
    '''
    return int(time_()*1000).to_bytes(6,byteorder='big') + urandom(10)

class User(UserMixin, db.Model):
    id = db.Column(db.BINARY(length=16), primary_key=True, default=keygen)
    username = db.Column(db.String(32), index=True, unique=True)
    email = db.Column(db.String(256), index=True, unique=True)
    password_hash = db.Column(db.String(128))

    tasks = db.relationship('Task', backref='owner', lazy='dynamic')

    def __repr__(self):
        return f"<User {self.username}>"

    def set_password(self, password):
        self.password_hash = generate_password_hash(password)

    def verify_password(self, password):
        return check_password_hash(self.password_hash, password)

    def get_id(self):
        return self.id.hex()

    def get_tasks(self):
        return Task.query.filter_by(owner_id=self.id).order_by(
            Task.favorite.desc(),
            Task.deadline.is_(None),
            Task.deadline.asc()
        )

    def generate_token(self, lifespan=600):
        d = {
            'id': self.id.hex(),
            'expires': int(time_()+lifespan),
        }
        return jwt.encode(d, current_app.config['SECRET_KEY'], algorithm='HS256')

    @staticmethod
    def get_from_token(token):
        try:
            payload = jwt.decode(token, current_app.config['SECRET_KEY'],
                                algorithms=['HS256'])
            id = bytes.fromhex(payload['id'])
            if time_() > payload['expires']:
                return None
        except (jwt.exceptions.InvalidTokenError, KeyError):
            return None
        return User.query.get(id)
        


@login.user_loader
def load_user(id):
    return User.query.get(bytes.fromhex(id))

class Task(db.Model):
    id = db.Column(db.BINARY(length=16), primary_key=True, default=keygen)
    owner_id = db.Column(db.BINARY(length=16), db.ForeignKey('user.id'))
    name = db.Column(db.String(100))
    deadline = db.Column(db.DateTime)
    saved_timezone = db.Column(db.String(100))
    favorite = db.Column(db.Boolean(), default=False)

    def __repr__(self):
        return f"<Task {self.id}: {self.name}>"

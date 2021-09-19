from app import db, login
from werkzeug.security import generate_password_hash, check_password_hash
from flask_login import UserMixin

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

@login.user_loader
def load_user(id):
    return User.query.get(bytes.fromhex(id))

class Task(db.Model):
    id = db.Column(db.BINARY(length=16), primary_key=True, default=keygen)
    owner_id = db.Column(db.Integer, db.ForeignKey('user.id'))
    name = db.Column(db.String(100))
    deadline = db.Column(db.DateTime)

    def __repr__(self):
        return f"<Task {self.id}: {self.name}>"

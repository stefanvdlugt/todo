from app.auth import auth
from app import db

@auth.route('/register',methods=['GET','POST'])
def register():
    return 'Register'

@auth.route('/login',methods=['GET','POST'])
def login():
    return 'Login'

@auth.route('/logout')
def logout():
    return 'Logout'
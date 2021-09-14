from app.auth import auth
from app import db
from flask import render_template, redirect, url_for, flash
from flask_login import current_user, login_user, logout_user
from app.auth.forms import RegistrationForm, LoginForm
from app.models import User

@auth.route('/register',methods=['GET','POST'])
def register():
    form = RegistrationForm()
    if form.validate_on_submit():
        user = User(username=form.username.data, email=form.email.data)
        user.set_password(form.password.data)
        db.session.add(user)
        db.session.commit()
        flash(f'Welcome, {form.username.data}, you are now a registered user. Please log in.')
        return redirect(url_for('auth.login'))
    return render_template('auth/register.html', form=form)

@auth.route('/login',methods=['GET','POST'])
def login():
    form = LoginForm()
    login_error = None
    if form.validate_on_submit():
        user = User.query.filter_by(username=form.username.data).first()
        if user is None or not user.verify_password(form.password.data):
            login_error = "Incorrect username or password."
        else:
            # Login
            login_user(user, remember=form.remember_me.data)
            flash("Login successful")
            return redirect(url_for('auth.login'))
    return render_template('auth/login.html', form=form, login_error=login_error)

@auth.route('/logout')
def logout():
    logout_user()
    return redirect(url_for('main.index'))
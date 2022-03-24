from app.auth import auth
from app import db
from flask import render_template, redirect, url_for, flash, request
from flask_login import current_user, login_user, logout_user
from app.auth.forms import LoginForm, PasswordResetForm, RegistrationForm, RequestPasswordResetForm
from app.models import User
from werkzeug.urls import url_parse
from app.auth.email import send_password_reset_email

@auth.route('/register',methods=['GET','POST'])
def register():
    if current_user.is_authenticated:
        return redirect(url_for('main.index'))
    form = RegistrationForm()
    if form.validate_on_submit():
        user = User(username=form.username.data, email=form.email.data)
        user.set_password(form.password.data)
        user.admin = (User.query.first() is None) # First registered user gets admin status
        db.session.add(user)
        db.session.commit()
        flash(f'Welcome, {form.username.data}, you are now a registered user. Please log in.')
        if user.admin:
            flash(f'As you are the first user to register, you have obtained admin rights.')
        return redirect(url_for('auth.login'))
    return render_template('auth/register.html', form=form)

@auth.route('/login',methods=['GET','POST'])
def login():
    if current_user.is_authenticated:
        return redirect(url_for('main.index'))
    form = LoginForm()
    if form.validate_on_submit():
        user = User.query.filter_by(username=form.username.data).first()
        if user is None or not user.verify_password(form.password.data):
            flash('Incorrect username or password.')
            return redirect(url_for('auth.login'))
        else:
            # Login
            login_user(user, remember=form.remember_me.data)
            next_page = request.args.get('next')
            if not next_page or url_parse(next_page).netloc!='':
                next_page = url_for('main.index')
            return redirect(next_page)
    return render_template('auth/login.html', form=form)

@auth.route('/logout')
def logout():
    logout_user()
    return redirect(url_for('main.index'))

@auth.route('/request_password_reset', methods=['GET','POST'])
def request_password_reset():
    if current_user.is_authenticated:
        return redirect(url_for('main.index'))
    form = RequestPasswordResetForm()
    if form.validate_on_submit():
        user = User.query.filter_by(email=form.email.data).first()
        if user:
            send_password_reset_email(user)
        flash('If the provided mail address is associated to any user, a link will be sent that can be used to reset the password.')
        return redirect(url_for('auth.login'))
            
    return render_template('auth/request_password_reset.html', form=form)


@auth.route('/reset_password/<token>', methods=['GET', 'POST'])
def reset_password(token):
    if current_user.is_authenticated:
        return redirect(url_for('main.index'))
    user = User.get_from_token(token)
    if not user:
        flash('The password reset link is invalid or has expired. Please request a new link.')
        return redirect(url_for('auth.request_password_reset'))
    form = PasswordResetForm()
    if form.validate_on_submit():
        user.set_password(form.password.data)
        db.session.commit()
        flash('Your password has been reset. Please log in.')
        return redirect(url_for('auth.login'))
    return render_template('auth/reset_password.html', form=form)


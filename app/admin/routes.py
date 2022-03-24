from app.admin import admin, admin_required
from app import db
from flask import render_template, redirect, url_for, flash, request, abort
from flask_login import current_user, login_user, logout_user
#from app.auth.forms import LoginForm, PasswordResetForm, RegistrationForm, RequestPasswordResetForm
from app.models import User
from werkzeug.urls import url_parse

@admin.route('/users')
@admin_required
def users():
    page = request.args.get('page',1,type=int)
    userlist = User.query.order_by(User.username).all()
    return render_template('admin/users.html', users=userlist)

@admin.route('/delete_user/<user_id>')
@admin_required
def delete_user(user_id):
    try:
        b = bytes.fromhex(user_id)
    except:
        print("Cannot convert to bytes.")
        abort(404)
    user = User.query.get(b)
    if user is not None:
        if user == current_user:
            flash('It is impossible to delete the current user.')
            return redirect(url_for('admin.users'))
        else:
            db.session.delete(user)
            db.session.commit()
            flash(f'Successfully deleted user {user.username}.')
            return redirect(url_for('admin.users'))
    else:
        print("User not found.")
        abort(404)
        
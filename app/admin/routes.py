from app.admin import admin, admin_required
from app import db
from flask import render_template, redirect, url_for, flash, request, abort
from flask_login import current_user, login_user, logout_user
#from app.auth.forms import LoginForm, PasswordResetForm, RegistrationForm, RequestPasswordResetForm
from app.admin.forms import DeleteUserForm, MakeAdminForm
from app.models import User
from werkzeug.urls import url_parse

@admin.route('/users')
@admin_required
def users():
    userlist = User.query.order_by(User.username).all()
    rows = []
    for user in userlist:
        userid = user.id.hex()
        rows.append((
            user, 
            DeleteUserForm(userid=userid),
            MakeAdminForm(userid=userid, status='0' if user.admin else '1')
        ))
    return render_template('admin/users.html', rows=rows)

@admin.route('/delete_user', methods=['POST'])
@admin_required
def delete_user():
    form = DeleteUserForm()
    if form.validate_on_submit():
        b = bytes.fromhex(form.userid.data)
        user = User.query.get(b)
        if user is not None:
            if user == current_user:
                flash('It is impossible to delete the current user.')
            else:
                db.session.delete(user)
                db.session.commit()
                flash(f'Successfully deleted user {user.username}.')
            return redirect(url_for('admin.users'))
        else:
            abort(404)
    else:
        return redirect(url_for('admin.users'))
    
        
@admin.route('/make_admin',methods=['POST'])
@admin_required
def make_admin():
    form = MakeAdminForm()
    if form.validate_on_submit():
        b = bytes.fromhex(form.userid.data)
        user = User.query.get(b)
        if user is not None:
            if user == current_user:
                flash("You cannot change your own admin status.")
            else:
                status = form.status.data
                user.admin = (status=='1')
                db.session.commit()
                if status=='1':
                    flash(f"User '{user.username}' is now an admin.")
                else:
                    flash(f"User '{user.username}' is no longer an admin.")
            return(redirect(url_for('admin.users')))
        else:
            abort(404)
    else:
        return redirect(url_for('admin.users'))
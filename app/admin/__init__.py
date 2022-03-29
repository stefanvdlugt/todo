from flask import Blueprint, url_for, request, redirect
from flask_login import current_user
from functools import wraps

admin = Blueprint('admin',__name__)

def admin_required(f):
    @wraps(f)
    def decorated_function(*args,**kwargs):
        if not current_user.is_authenticated:
            return redirect(url_for('auth.login', next=request.url))
        if not current_user.admin:
            return redirect(url_for('main.index'))
        return f(*args, **kwargs)
    return decorated_function





from app.admin import routes, context
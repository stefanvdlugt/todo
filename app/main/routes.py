from flask_login import login_required
from app.main import main
from flask import render_template, redirect, url_for, flash
from flask_login import current_user

@main.route('/')
@main.route('/index')
@login_required
def index():
    return render_template('index.html')

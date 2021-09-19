from flask_login import login_required
from app.main import main
from flask import render_template, redirect, url_for, flash, request
from flask_login import current_user
from app.models import Task
from app import db

@main.route('/')
@main.route('/index')
@login_required
def index():
    tasks = current_user.tasks
    return render_template('index.html',tasks=tasks)

@main.route('/add_task', methods=['POST'])
@login_required
def add_task():
    name = request.form.get('task')
    if name:
        t = Task(name=name, owner=current_user)
        db.session.add(t)
        db.session.commit()
    return redirect(url_for('main.index'))

@main.route('/delete_task/<task_id>')
@login_required
def delete_task(task_id):
    task=Task.query.get(int(task_id))
    if task is not None and task.owner==current_user:
        return f"Deleting task {task.id}..."
    return redirect(url_for('main.index'))

@main.route('/edit_task/<task_id>')
@login_required
def edit_task(task_id):
    return redirect(url_for('main.index'))
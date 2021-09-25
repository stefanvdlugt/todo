from flask_login import login_required
from app.main import main
from flask import render_template, redirect, url_for, flash, request, abort
from flask_login import current_user
from app.models import Task
from app import db
from app.main.forms import TaskEditForm

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
    try:
        b = bytes.fromhex(task_id)
    except:
        abort(404)
    task=Task.query.get(b)
    if task is not None and task.owner==current_user:
        db.session.delete(task)
        db.session.commit()
        return redirect(url_for('main.index'))
    else:
        abort(404)

@main.route('/edit_task/<task_id>', methods=['POST','GET'])
@login_required
def edit_task(task_id):
    try:
        b = bytes.fromhex(task_id)
    except:
        abort(404)
    task=Task.query.get(b)
    if task is not None and task.owner==current_user:
        form = TaskEditForm(taskname=task.name)
        if form.validate_on_submit():
            task.name = form.taskname.data
            db.session.commit()
            return redirect(url_for('main.index'))
        else:
            return render_template('task.html',task=task, form=form)
    else:
        abort(404)
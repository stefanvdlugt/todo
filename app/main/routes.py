from flask_login import login_required
from app.main import main
from flask import render_template, redirect, url_for, flash, request, abort
from flask_login import current_user
from app.models import Task, Reminder
from app import db
import re
from app.main.forms import TaskEditForm, re_date, re_time, DeleteTaskForm, FavoriteTaskForm, MarkTaskForm, AddReminderForm, DeleteReminderForm
from datetime import datetime
import pytz

def to_utc(datetime, timezone):
    tz = pytz.timezone(timezone)
    return tz.normalize(tz.localize(datetime)).astimezone(pytz.utc)

def from_utc(datetime, timezone):
    tz = pytz.timezone(timezone)
    return tz.fromutc(datetime)


@main.route('/')
@main.route('/index')
@login_required
def index():
    tasks = current_user.get_tasks()
    rows = [ (
        task,
        MarkTaskForm(taskid=task.id.hex(), status='0' if task.done else '1'),
        FavoriteTaskForm(taskid=task.id.hex(), status='0' if task.favorite else '1'),
        DeleteTaskForm(taskid=task.id.hex()),
    ) for task in tasks ]
    return render_template('index.html',rows=rows)

@main.route('/add_task', methods=['POST'])
@login_required
def add_task():
    name = request.form.get('task')
    if name:
        t = Task(name=name, owner=current_user)
        db.session.add(t)
        db.session.commit()
    return redirect(url_for('main.index'))

@main.route('/mark_task', methods=['POST'])
@login_required
def mark_task():
    form = MarkTaskForm()
    if form.validate_on_submit():
        b = bytes.fromhex(form.taskid.data)
        task = Task.query.get(b)
        if task is not None and task.owner==current_user:
            task.done = (form.status.data=='1')
            db.session.commit()
            return(redirect(url_for('main.index')))
    abort(404)

@main.route('/delete_task', methods=['POST'])
@login_required
def delete_task():
    form = DeleteTaskForm()
    if form.validate_on_submit():
        b = bytes.fromhex(form.taskid.data)
        task = Task.query.get(b)
        if task is not None and task.owner==current_user:
            db.session.delete(task)
            db.session.commit()
            return redirect(url_for('main.index'))
        else:
            abort(404)

@main.route('/favorite', methods=['POST'])
@login_required
def favorite():
    form = FavoriteTaskForm()
    if form.validate_on_submit():
        b = bytes.fromhex(form.taskid.data)
        task = Task.query.get(b)
        if task is not None and task.owner==current_user:
            task.favorite = (form.status.data=='1')
            db.session.commit()
            return(redirect(url_for('main.index')))
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
        t = dict()
        if task.deadline is not None:
            tz = task.saved_timezone or 'UTC'
            t['timezone'] = tz
            tlocal = from_utc(task.deadline, tz)
            t['date'] = tlocal.strftime('%d/%m/%Y')
            t['time'] = tlocal.strftime('%H:%M')
        else:
            tz = None

        form = TaskEditForm(taskname=task.name,due=t)
        remform = AddReminderForm(taskid = task_id, time={'timezone': tz})
        if form.validate_on_submit():
            # Convert user's datetime to UTC
            dt = form.due.parse_utc()
            if dt is not None:
                timezone = form.due.timezone.data
            else:
                timezone = None
            task.name = form.taskname.data
            task.deadline = dt
            task.saved_timezone = timezone
            db.session.commit()
            if form.submitclose.data:
                return redirect(url_for('main.index'))
            return redirect(url_for('main.edit_task', task_id=task_id))
        elif remform.validate_on_submit():
            dt = remform.time.parse_utc()
            if dt is not None:
                timezone = remform.time.timezone.data
                rem = Reminder(task=task, time=dt, saved_timezone=timezone)
                db.session.add(rem)
                db.session.commit()
                return redirect(url_for('main.edit_task', task_id=task_id))
        else:
            reminders = task.get_reminders()
            remrows = [(
                rem,
                DeleteReminderForm(reminderid=rem.id.hex())
            ) for rem in reminders]
            return render_template('task.html',task=task, form=form, remform=remform, remrows=remrows)
    else:
        abort(404)

@main.route('/delete_reminder', methods=['POST'])
@login_required
def delete_reminder():
    form = DeleteReminderForm()
    if form.validate_on_submit():
        b = bytes.fromhex(form.reminderid.data)
        rem = Reminder.query.get(b)
        if rem is not None and rem.task.owner==current_user:
            db.session.delete(rem)
            db.session.commit()
            return redirect(url_for('main.edit_task', task_id=rem.task.id.hex()))
        else:
            abort(404)
    else:
        abort(404)
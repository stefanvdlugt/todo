from flask_login import login_required
from app.main import main
from flask import render_template, redirect, url_for, flash, request, abort
from flask_login import current_user
from app.models import Task
from app import db
import re
from app.main.forms import TaskEditForm, re_date, re_time
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

@main.route('/favorite/<task_id>/<fav>')
@login_required
def favorite(task_id,fav):
    try:
        b = bytes.fromhex(task_id)
    except:
        abort(404)
    task=Task.query.get(b)
    if task is not None and task.owner==current_user:
        task.favorite = bool(int(fav))
        db.session.commit()
        return(redirect(url_for('main.index')))
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
        t = dict()
        if task.deadline is not None:
            tz = task.saved_timezone or 'UTC'
            t['timezone'] = tz
            tlocal = from_utc(task.deadline, tz)
            t['date'] = tlocal.strftime('%d/%m/%Y')
            t['time'] = tlocal.strftime('%H:%M')

        form = TaskEditForm(taskname=task.name,due=t)
        if form.validate_on_submit():
            # Convert user's datetime to UTC
            if form.due.date.data and form.due.time.data:
                # Parse timezone, date, and time
                timezone = form.due.timezone.data
                ddmmyyyy = re.match(re_date, form.due.date.data).groups()
                day, month, year = int(ddmmyyyy[0]),int(ddmmyyyy[1]), int(ddmmyyyy[2])
                hm = re.match(re_time, form.due.time.data).groups()
                hour,minute = int(hm[0]), int(hm[1])
                # Convert to a datetime object
                dt = to_utc(datetime(year,month,day,hour,minute), timezone)
            else:
                timezone = None
                dt = None

            task.name = form.taskname.data
            task.deadline = dt
            task.saved_timezone = timezone
            db.session.commit()
            return redirect(url_for('main.index'))
        else:
            return render_template('task.html',task=task, form=form)
    else:
        abort(404)
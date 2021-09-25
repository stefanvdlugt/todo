from flask_wtf import FlaskForm
from wtforms.fields import StringField, SubmitField
from wtforms.validators import DataRequired, Length
from app.models import Task


class TaskEditForm(FlaskForm):
    taskname = StringField('Task name', validators=[DataRequired(), Length(max=100)])
    submit = SubmitField('Save')

from flask_wtf import FlaskForm
from wtforms.fields import StringField, SubmitField, SelectField, IntegerField, FormField
from wtforms.validators import DataRequired, Length, Regexp, ValidationError
import re
import datetime, pytz

months = ['Jan', 'Feb', 'Mar', 'Apr', 'May', 'Jun', 'Jul', 'Aug', 'Sep', 'Oct', 'Nov', 'Dec']

re_date = r'^(0?[1-9]|[12]\d|3[01])\/(0?[1-9]|1[012])\/(\d\d\d\d)$'
re_time = r'^([01]?\d|2[0-3]):([0-5]\d)$'

tz_choices = [('','Select...')] + [(s,s.replace('_',' ')) for s in pytz.all_timezones]

class IsHex(object):
    def __init__(self, message="Not a valid hexadecimal string."):
        self.message = message

    def __call__(self,form,field):
        try:
            bytes.fromhex(field.data)
        except:
            raise ValidationError(self.message)

class DateTimeForm(FlaskForm):
    date = StringField('Date', render_kw={'placeholder': 'dd/mm/yyyy', 'class': 'input'})
    time = StringField('Time', render_kw={'placeholder': 'hh:mm', 'class': 'input'})
    timezone = SelectField('Timezone', choices=tz_choices)

    def validate_date(form, field):
        if bool(field.data) != bool(form.time.data):
            raise ValidationError('Date and time fields should both be empty or filled in.')
        elif field.data:
            m = re.match(re_date, field.data)
            if m:
                dd,mm,yyyy = m.groups()
                try:
                    datetime.datetime(int(yyyy),int(mm),int(dd))
                except ValueError:
                    raise ValidationError('Not a valid date.')
            else:
                raise ValidationError('Date should be in dd/mm/yyyy format.')

    def validate_time(form, field):
        if bool(field.data) != bool(form.date.data):
            raise ValidationError('Date and time fields should both be empty or filled in.')
        elif field.data:
            if not re.match(re_time, field.data):
                raise ValidationError('Time should be in hh:mm format.')
    
    def validate_timezone(form, field):
        if field.data not in pytz.all_timezones:
            raise ValidationError('Not a valid timezone.')




class TaskEditForm(FlaskForm):
    taskname = StringField('Task name', validators=[DataRequired(), Length(max=100)])
    due = FormField(DateTimeForm, label='Due date')
    submit = SubmitField('Save')


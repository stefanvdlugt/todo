from flask_wtf import FlaskForm
from wtforms.fields import HiddenField, SubmitField, SelectField
from wtforms.validators import DataRequired, InputRequired, Regexp, Email, ValidationError, EqualTo
from app.models import User
from app.main.forms import IsHex
import json

class DeleteUserForm(FlaskForm):
    userid = HiddenField(validators=[DataRequired(), IsHex()])
    
class MakeAdminForm(FlaskForm):
    userid = HiddenField(validators=[DataRequired(), IsHex()])
    status = HiddenField(validators=[DataRequired(), Regexp('^[01]$')])
    
class SettingsForm(FlaskForm):
    enableregistration = SelectField(
        'Allow registration of new users',
        choices = [("1", 'Enable'),("0", 'Disable')],
        validators=[InputRequired()]
    )
    submit = SubmitField('Save settings')
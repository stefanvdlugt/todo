from flask_wtf import FlaskForm
from wtforms.fields import HiddenField, SubmitField
from wtforms.validators import DataRequired, Regexp, Email, ValidationError, EqualTo
from app.models import User
from app.main.forms import IsHex

class DeleteUserForm(FlaskForm):
    userid = HiddenField(validators=[DataRequired(), IsHex()])
    
class MakeAdminForm(FlaskForm):
    userid = HiddenField(validators=[DataRequired(), IsHex()])
    status = HiddenField(validators=[DataRequired(), Regexp('^[01]$')])
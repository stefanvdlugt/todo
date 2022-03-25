from flask_wtf import FlaskForm
from wtforms.fields import HiddenField, SubmitField
from wtforms.validators import DataRequired, Regexp, Email, ValidationError, EqualTo
from app.models import User

class IsHex(object):
    def __init__(self, message="Not a valid hexadecimal string."):
        self.message = message

    def __call__(self,form,field):
        try:
            bytes.fromhex(field.data)
        except:
            raise ValidationError(self.message)

class DeleteUserForm(FlaskForm):
    userid = HiddenField(validators=[DataRequired(), IsHex()])
    
class MakeAdminForm(FlaskForm):
    userid = HiddenField(validators=[DataRequired(), IsHex()])
    status = HiddenField(validators=[DataRequired(), Regexp('^[01]$')])
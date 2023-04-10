from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, PasswordField, SelectField
from wtforms.validators import InputRequired

class UserForm(FlaskForm):
    username = StringField(
        'Username',
        [InputRequired()]
    )
    password = PasswordField(
        'Password',
        [InputRequired()]
    )
    email = StringField(
        'Email',
        [InputRequired()]
    )
    confirmed = SelectField(
        'Confirmed'
    )
    submit = SubmitField(
        'Submit',
        [InputRequired()]
    )

class ChangeRoleForm(FlaskForm):
    role = SelectField(
        'Role',
        [InputRequired()]
    )
    submit = SubmitField(
        'Submit',
        [InputRequired()]
    )
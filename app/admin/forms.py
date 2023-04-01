from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, PasswordField
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
    submit = SubmitField(
        'Submit',
        [InputRequired()]
    )
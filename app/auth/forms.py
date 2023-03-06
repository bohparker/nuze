from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField
from wtforms.validators import InputRequired, EqualTo

class RegistrationForm(FlaskForm):
    username = StringField(
        'Username',
        [InputRequired('Please choose a username')]
    )
    password = PasswordField(
        'Password', [
            InputRequired('Please choose a password'),
            EqualTo('confirm', message='Passwords must match')
        ]
    )
    confirm = PasswordField(
        'Confirm Password',
        [InputRequired('Please confirm password')]
    )
    email = StringField(
        'Email',
        [InputRequired('Please enter your email address')]
    )
    submit = SubmitField('Register')

class LoginForm(FlaskForm):
    username = StringField(
        'Username',
        [InputRequired('Please enter your username')]
    )
    password = PasswordField(
        'Password',
        [InputRequired('Please enter your password')]
    )
    submit = SubmitField('Login')
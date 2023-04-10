from flask_wtf import FlaskForm
from flask_ckeditor import CKEditorField
from wtforms import StringField, SubmitField, TextAreaField, PasswordField
from wtforms.validators import InputRequired, EqualTo

class ArticleForm(FlaskForm):
    title = StringField(
        'Title',
        [InputRequired()]
    )
    body = CKEditorField('Body')
    submit = SubmitField(
        'Submit',
        [InputRequired()]
    )

class BioForm(FlaskForm):
    bio = TextAreaField(
        'Bio',
        [InputRequired()]
    )
    submit = SubmitField(
        'Submit',
        [InputRequired()]
    )

class ChangePasswordForm(FlaskForm):
    password = PasswordField(
        'Enter Current Password', [
            InputRequired('Enter your current password.'),
            EqualTo('confirm', message='Passwords must match.')
        ]
    )
    confirm = PasswordField(
        'Confirm Current Password',
        [InputRequired('Confirm current password.')]
    )
    new = PasswordField(
        'New Password',
        [InputRequired('Enter new password.')]
    )
    submit = SubmitField('Submit')

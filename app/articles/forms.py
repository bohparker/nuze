from flask_wtf import FlaskForm
from flask_ckeditor import CKEditorField
from wtforms import StringField, SubmitField
from wtforms.validators import InputRequired

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
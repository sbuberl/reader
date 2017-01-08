from constants import ALLOWED_EXTENSIONS
from flask_wtf import FlaskForm
from flask_wtf.file import FileField, FileAllowed, FileRequired
from wtforms import StringField, IntegerField
from wtforms.fields.html5 import DateField
from wtforms.validators import DataRequired, Optional


class UploadForm(FlaskForm):
    uploaded_file = FileField('Your document', validators=[
        FileRequired(),
        FileAllowed(list(ALLOWED_EXTENSIONS), 'Comics, epubs, and pdf only!')
    ])


class ComicMetadataForm(FlaskForm):
    series = StringField('Series', validators=[DataRequired()])
    issue = IntegerField('Issue', validators=[DataRequired()])
    author = StringField('Author')
    publisher = StringField('Publisher')
    release_date = DateField('Release Date', validators=[Optional()])


class DocumentMetadataForm(FlaskForm):
    name = StringField('Name', validators=[DataRequired()])
    author = StringField('Author')
    publisher = StringField('Publisher')
    release_date = DateField('Release Date', validators=[Optional()])


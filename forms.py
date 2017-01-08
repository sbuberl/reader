from constants import ALLOWED_EXTENSIONS
from flask_wtf import FlaskForm
from flask_wtf.file import FileField, FileAllowed, FileRequired
import imghdr
from wtforms import StringField, IntegerField
from wtforms.fields.html5 import DateField
from wtforms.validators import DataRequired, Optional, StopValidation


class CoverImageValidator(object):
    def __init__(self, message=None):
        self.message = message

    def __call__(self, form, field):
        if field.data and imghdr.what('unused', field.data.read()) is None:
            message = self.message or 'Uploaded cover is not an image'
            raise StopValidation(message)

        field.data.seek(0)


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
    cover_file = FileField('Cover', validators=[CoverImageValidator()])


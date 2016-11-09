from constants import ALLOWED_EXTENSIONS
from flask_wtf import FlaskForm
from flask_wtf.file import FileField, FileAllowed, FileRequired


class UploadForm(FlaskForm):
    uploaded_file = FileField('Your document', validators=[
        FileRequired(),
        FileAllowed(list(ALLOWED_EXTENSIONS), 'Comics, epubs, and pdf only!')
    ])



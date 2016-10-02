import os

DATA_FOLDER =  "data"
UPLOAD_FOLDER = os.path.join(DATA_FOLDER, 'uploads')
LIBRARY_FOLDER = os.path.join(DATA_FOLDER, 'library')
THUMBNAILS = os.path.join(DATA_FOLDER, 'thumbnails')
ALLOWED_EXTENSIONS = set(['.cbr', '.cbz', '.cbt', '.epub', '.pdf'])
COMIC_EXTENSIONS = set(['.cbr', '.cbz', '.cbt' ])
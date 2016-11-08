import os
import sys

CURRENT_PATH = os.path.realpath(os.path.dirname(sys.argv[0]))
DATA_FOLDER = os.path.join(CURRENT_PATH, "data")
UPLOAD_FOLDER = os.path.join(DATA_FOLDER, 'uploads')
LIBRARY_FOLDER = os.path.join(DATA_FOLDER, 'library')
THUMBNAILS = os.path.join(DATA_FOLDER, 'thumbnails')
ALLOWED_EXTENSIONS = {'.cbr', '.cbz', '.cbt', '.epub', '.pdf'}
COMIC_EXTENSIONS = {'.cbr', '.cbz', '.cbt'}
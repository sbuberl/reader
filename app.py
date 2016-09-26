from flask import Flask, render_template, request, flash, redirect, url_for
from flask_sqlalchemy import SQLAlchemy
import imghdr
from models import db, FileType, File, ComicPage, Comic
import os
import re
from zipfile import ZipFile

dbName = 'test.db'
UPLOAD_FOLDER = 'uploads'
ALLOWED_EXTENSIONS = set(['.cbr', '.cbz', '.epub'])

app = Flask(__name__)
app.secret_key = '\x1f\x14E\x95\xd86\xb2\x08\xa5\xe4\x8a\xcf\xd8f\xb8\xfdS<\xa3\xc2\x00\x1d\x99\xca`\xcc_6\xee\xa3\xd0;'
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///' + dbName
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = True

if not os.path.isdir(UPLOAD_FOLDER):
    os.makedirs(UPLOAD_FOLDER)


def add_and_refresh(object):
    db.session.add(object)
    db.session.flush()
    db.session.refresh(object)


def path_leaf(path):
    head, tail = os.path.split(path)
    return tail or os.path.basename(head)

@app.route('/')
def index():
    return render_template('index.html')

def allowed_file(filename):
    return '.' in filename and \
       filename.rsplit('.', 1)[1] in ALLOWED_EXTENSIONS

@app.route('/upload', methods=['GET', 'POST'])
def upload_file():
    if request.method == 'POST':
        file = request.files['file']
        if file:
            filename = file.filename
            uploaded_file_path = os.path.join(app.config['UPLOAD_FOLDER'], filename)
            file.save(uploaded_file_path)
            basename, extension = os.path.splitext(filename)
            if extension in ALLOWED_EXTENSIONS:
                extracted_path = os.path.join(app.config['UPLOAD_FOLDER'], basename)
                if extension == '.cbz':
                    comic = Comic(name=basename)
                    match = re.match("(.+?)\s+(\d+)\.", filename)
                    if match:
                        comic.series = match.group(1)
                        comic.issue = match.group(2)
                    add_and_refresh(comic)
                    image_type = FileType.query.filter_by(category='image').first()
                    with ZipFile(uploaded_file_path) as zip:
                        zip_list = zip.infolist()
                        page_number = 1
                        for zipinfo in zip_list:
                            page_path = zip.extract(zipinfo.filename, extracted_path)
                            page_type = imghdr.what(page_path)
                            if page_type:
                                page_file_name = path_leaf(zipinfo.filename)
                                page_path = os.path.join(extracted_path, zipinfo.filename)
                                page_file = File(name=page_file_name, path=page_path, size=zipinfo.file_size, type=image_type.id)
                                add_and_refresh(page_file)
                                page = ComicPage(page_number=page_number, comic_id=comic.id, file_id=page_file.id)
                                add_and_refresh(page)
                                page_number += 1
                                comic.add_page(page)
                    db.session.commit()
                return redirect(url_for('index'))
    return render_template('upload.html')


if __name__ == '__main__':
    db.init_app(app)
    if not os.path.isfile(dbName):
        with app.app_context():
            db.create_all()
            db.session.add(FileType(category='comic'))
            db.session.add(FileType(category='epub'))
            db.session.add(FileType(category='image'))
            db.session.commit()
    app.run(debug=True)

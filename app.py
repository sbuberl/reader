from flask import Flask, render_template, request, flash, redirect, url_for
from flask_sqlalchemy import SQLAlchemy
from models import db, FileType, File, ComicPage, Comic
import os
import zipfile
import imghdr

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
            zipFilePath = os.path.join(app.config['UPLOAD_FOLDER'], filename)
            file.save(zipFilePath)
            basename, extension = os.path.splitext(filename)
            if extension in ALLOWED_EXTENSIONS:
                extractedPath = os.path.join(app.config['UPLOAD_FOLDER'], basename)
                if extension == '.cbz':
                    comic = Comic()
                    imageType = FileType.query.filter_by(category='image').first()
                    with zipfile.ZipFile(zipFilePath) as zip:
                        for zipinfo in zip.infolist():
                            pagePath = zip.extract(zipinfo.filename, extractedPath)
                            pageType = imghdr.what(pagePath)
                            if pageType is not None:
                                pageFileName = path_leaf(zipinfo.filename)
                                pagePath = os.path.join(extractedPath, zipinfo.filename)
                                pageFile = File(name=pageFileName, path=pagePath, size=zipinfo.file_size, type=imageType)
                                page = ComicPage(file_id=pageFile.id)
                                comic.add_page(page)
                    db.session.add(comic)
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

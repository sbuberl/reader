from constants import *
from flask import Flask, render_template, redirect, url_for, send_file, send_from_directory
from forms import UploadForm
from handlers import CbzHandler, CbrHandler, CbtHandler, PdfHandler, EpubHandler
from models import db, FileType, File, ComicPage, Comic, DocumentType, Pdf, Epub
import os

db_name = os.path.join(CURRENT_PATH, 'test.db')

app = Flask(__name__)
app.secret_key = '\x1f\x14E\x95\xd86\xb2\x08\xa5\xe4\x8a\xcf\xd8f\xb8\xfdS<\xa3\xc2\x00\x1d\x99\xca`\xcc_6\xee\xa3\xd0;'
WTF_CSRF_SECRET_KEY = '\x19B\xe3\xe0v\x1du\xd4\xb7G\x04\xe3-\xddD\xe8\xde+@\xd7$Ixsp]\xf0\xb5z\xcfO[\x90\xdd\xf8\xcd'
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///' + db_name
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = True

if not os.path.isdir(UPLOAD_FOLDER):
    os.makedirs(UPLOAD_FOLDER)
if not os.path.isdir(LIBRARY_FOLDER):
    os.makedirs(LIBRARY_FOLDER)
if not os.path.isdir(THUMBNAILS):
    os.makedirs(THUMBNAILS)


@app.route('/')
def index():
    comics = db.session.query(Comic.id, Comic.name, DocumentType.category, Comic.cover_id).join(DocumentType)
    pdfs = db.session.query(Pdf.id, Pdf.name, DocumentType.category, Pdf.cover_id).join(DocumentType)
    epubs = db.session.query(Epub.id, Epub.name, DocumentType.category, Epub.cover_id).join(DocumentType)
    docs = comics.union(pdfs).union(epubs).all()
    return render_template('index.html', documents=docs)


@app.route('/file/<int:file_id>')
def get_file(file_id):
    found_file = File.query.filter_by(id=file_id).one()
    return send_file(found_file.path)


@app.route('/read/comic/<int:comic_id>')
def read_comic(comic_id):
    comic = Comic.query.filter_by(id=comic_id).one()
    return render_template('read_comic.html', comic=comic)


@app.route('/read/epub/<int:book_id>')
def read_epub(book_id):
    epub = Epub.query.filter_by(id=book_id).one()
    return render_template('read_epub.html', book=epub)


@app.route('/epub/<int:book_id>/<path:filename>')
def epub_file(book_id, filename):
    epub = Epub.query.filter_by(id=book_id).one()
    return send_from_directory(epub.extracted_path, filename=filename)


@app.route('/read/pdf/<int:book_id>')
def read_pdf(book_id):
    book = Pdf.query.filter_by(id=book_id).one()
    return render_template('read_pdf.html', file_id=book.file_id)


@app.route('/comic/<int:comic_id>/page/<int:page_number>')
def get_comic_page(comic_id, page_number):
    page = ComicPage.query.filter(ComicPage.comic_id == comic_id).filter(ComicPage.page_number == page_number).one()
    return get_file(page.file_id)


@app.route('/upload', methods=['GET', 'POST'])
def upload_file():
    form = UploadForm()
    if form.validate_on_submit():
        uploaded_file = form.uploaded_file.data
        filename = uploaded_file.filename
        uploaded_file_path = os.path.join(UPLOAD_FOLDER, filename)
        uploaded_file.save(uploaded_file_path)
        basename, extension = os.path.splitext(filename)
        extension = extension[1:]
        if extension in ALLOWED_EXTENSIONS:
            if extension in COMIC_EXTENSIONS:
                if extension == 'cbz':
                    handler = CbzHandler()
                elif extension == 'cbr':
                    handler = CbrHandler()
                elif extension == 'cbt':
                    handler = CbtHandler()
            elif extension == 'epub':
                handler = EpubHandler()
            else:
                handler = PdfHandler()
            handler.handle_file(basename, uploaded_file_path)
            db.session.commit()
            return redirect(url_for('index'))
    return render_template('upload.html', form=form)


def populate_db():
    db.create_all()
    db.session.add(DocumentType(category='comic'))
    db.session.add(DocumentType(category='epub'))
    db.session.add(DocumentType(category='pdf'))
    db.session.add(FileType(category='comic'))
    db.session.add(FileType(category='epub'))
    db.session.add(FileType(category='image'))
    db.session.add(FileType(category='pdf'))
    db.session.commit()


if __name__ == '__main__':
    db.init_app(app)
    if not os.path.isfile(db_name):
        with app.app_context():
            populate_db()
    app.run(host='0.0.0.0', debug=True)

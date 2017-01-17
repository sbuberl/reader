from api import ComicResource, DocumentResource, DocumentListResource, FileResource
from constants import *
from flask import Flask, render_template, redirect, url_for, send_file, send_from_directory
from flask_restful import Api
from forms import UploadForm, ComicMetadataForm, DocumentMetadataForm
from handlers import get_handler
from models import db, File, ComicPage, Comic, Pdf, Epub
import os
from PIL import Image
from utils import add_and_refresh

db_name = os.path.join(CURRENT_PATH, 'test.db')

app = Flask(__name__)
app.secret_key = '\x1f\x14E\x95\xd86\xb2\x08\xa5\xe4\x8a\xcf\xd8f\xb8\xfdS<\xa3\xc2\x00\x1d\x99\xca`\xcc_6\xee\xa3\xd0;'
WTF_CSRF_SECRET_KEY = '\x19B\xe3\xe0v\x1du\xd4\xb7G\x04\xe3-\xddD\xe8\xde+@\xd7$Ixsp]\xf0\xb5z\xcfO[\x90\xdd\xf8\xcd'
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///' + db_name
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = True

api = Api(app)

if not os.path.isdir(UPLOAD_FOLDER):
    os.makedirs(UPLOAD_FOLDER)
if not os.path.isdir(LIBRARY_FOLDER):
    os.makedirs(LIBRARY_FOLDER)
if not os.path.isdir(THUMBNAILS):
    os.makedirs(THUMBNAILS)

api.add_resource(FileResource, '/api/files/<int:file_id>')
api.add_resource(DocumentListResource, '/api/documents')
api.add_resource(DocumentResource, '/api/documents/<int:doc_id>')
api.add_resource(ComicResource, '/api/comics/<int:comic_id>')


@app.route('/')
def index():
    return render_template('react_index.html')


@app.route('/library')
def library():
    comics = db.session.query(Comic.id, Comic.name, Comic.type, Comic.cover_id)
    pdfs = db.session.query(Pdf.id, Pdf.name, Pdf.type, Pdf.cover_id)
    epubs = db.session.query(Epub.id, Epub.name, Epub.type, Epub.cover_id)
    docs = comics.union(pdfs).union(epubs).all()
    docs.sort(key=lambda x: x.name)
    return render_template('index.html', docs=docs)


@app.route('/file/<int:file_id>')
def get_file(file_id):
    found_file = File.query.filter_by(id=file_id).one()
    return send_file(found_file.path)


@app.route('/download/<string:doc_type>/<int:doc_id>')
def download(doc_type, doc_id):
    if doc_type == COMIC_TYPE:
        clazz = Comic
        mimetype = None
    elif doc_type == EPUB_TYPE:
        clazz = Epub
        mimetype = "application/epub+zip"
    else:
        clazz = Pdf
        mimetype = "application/pdf"
    document = clazz.query.filter_by(id=doc_id).one()
    doc_file = File.query.filter_by(id=document.file_id).one()
    return send_file(doc_file.path, mimetype=mimetype, as_attachment=True)


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
        handler = get_handler(extension)
        if handler:
            document = handler.handle_file(basename, uploaded_file_path)
            db.session.commit()
            return redirect(url_for('edit_metadata', doc_type=document.type, doc_id=document.id))
    return render_template('upload.html', form=form)


@app.route('/metadata/<string:doc_type>/<int:doc_id>', methods=['GET', 'POST'])
def edit_metadata(doc_type, doc_id):
    is_comic = False
    if doc_type == COMIC_TYPE:
        clazz = Comic
        is_comic = True
    elif doc_type == EPUB_TYPE:
        clazz = Epub
    else:
        clazz = Pdf
    document = clazz.query.filter_by(id=doc_id).one()
    if is_comic:
        form = ComicMetadataForm(obj=document)
    else:
        form = DocumentMetadataForm(obj=document)

    if document.cover_id:
        cover_path = url_for('get_file', file_id=document.cover_id)
    else:
        cover_path = url_for('static', filename='images/no_cover.jpg')

    if form.validate_on_submit():
        document.author = form.author.data
        document.publisher = form.publisher.data
        if is_comic:
            document.series = form.series.data
            document.issue = form.issue.data
            document.name = document.series + ' ' + '{:03d}'.format(document.issue)
        else:
            document.name = form.name.data

        if is_comic is False and form.cover_file.data:
            uploaded_file = form.cover_file.data
            cover_name = uploaded_file.filename
            uploaded_file_path = os.path.join(UPLOAD_FOLDER, cover_name)
            uploaded_file.save(uploaded_file_path)
            cover_extension = os.path.splitext(cover_name)[1]
            thumbnail_name = '{0}{1}'.format(document.name, cover_extension)
            thumbnail_path = os.path.join(THUMBNAILS, thumbnail_name)
            if os.path.exists(thumbnail_path):
                os.remove(thumbnail_path)
            im = Image.open(uploaded_file_path)
            im.thumbnail((200, 200))
            im.save(thumbnail_path)
            thumbnail = File(name=cover_name, path=thumbnail_path, size=os.path.getsize(thumbnail_path),
                             type=IMAGE_TYPE)
            add_and_refresh(thumbnail)
            os.remove(uploaded_file_path)
            document.cover_id = thumbnail.id
        db.session.commit()
        return redirect(url_for('index'))
    return render_template('edit_metadata.html', form=form, cover_path=cover_path)


def populate_db():
    db.create_all()
    db.session.commit()


if __name__ == '__main__':
    db.init_app(app)
    if not os.path.isfile(db_name):
        with app.app_context():
            populate_db()
    app.run(host='0.0.0.0', debug=True)

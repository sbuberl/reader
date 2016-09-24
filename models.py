from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()

class File(db.Model):
    __tablename__ = "files"
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String)
    path = db.Column(db.String)
    size = db.Column(db.Integer)
    type = db.Column(db.Integer, db.ForeignKey('file_types.id'))

class FileType(db.Model):
    __tablename__ = "file_types"
    id = db.Column(db.Integer, primary_key=True)
    category = db.Column(db.String)

class Comic(db.Model):
    __tablename__ = "comics"
    id = db.Column(db.Integer, primary_key=True)
    series = db.Column(db.String)
    issue = db.Column(db.Integer)
    publisher = db.Column(db.String)
    release_date = db.Column(db.DateTime)
    pages = db.relationship('ComicPage', backref='pages_ref',
                                lazy='dynamic')

    def add_page(self, page):
        self.pages.append(page)

class ComicPage(db.Model):
    __tablename__ = "comic_pages"
    id = db.Column(db.Integer, primary_key=True)
    comic_id = db.Column(db.Integer, db.ForeignKey('comics.id'))
    file_id = db.Column(db.Integer, db.ForeignKey('files.id'))

class Book(db.Model):
    __tablename__ = "books"
    id = db.Column(db.Integer, primary_key=True)
    book = db.Column(db.String)
    author = db.Column(db.String)
    file_id = db.Column(db.Integer, db.ForeignKey('files.id'))


from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.ext.declarative import declared_attr

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


class DocumentType(db.Model):
    __tablename__ = "doc_types"
    id = db.Column(db.Integer, primary_key=True)
    category = db.Column(db.String)


class Document(db.Model):
    __abstract__ = True
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String)
    author = db.Column(db.String)
    publisher = db.Column(db.String)
    release_date = db.Column(db.DateTime)

    @declared_attr
    def cover_id(cls):
        return db.Column(db.Integer, db.ForeignKey('files.id'))

    @declared_attr
    def type(cls):
        return db.Column(db.Integer, db.ForeignKey('doc_types.id'))


class Comic(Document):
    __tablename__ = "comics"
    series = db.Column(db.String)
    issue = db.Column(db.Integer)
    pages = db.relationship("ComicPage", back_populates="comic")
    db.UniqueConstraint('series', 'issue')

    def add_page(self, page):
        self.pages.append(page)


class ComicPage(db.Model):
    __tablename__ = "comic_pages"
    id = db.Column(db.Integer, primary_key=True)
    page_number = db.Column(db.Integer)
    comic_id = db.Column(db.Integer, db.ForeignKey('comics.id'))
    file_id = db.Column(db.Integer, db.ForeignKey('files.id'))
    comic = db.relationship("Comic", back_populates="pages")

    db.UniqueConstraint('comic_id', 'page_number')


class Book(Document):
    __tablename__ = "books"
    file_id = db.Column(db.Integer, db.ForeignKey('files.id'))


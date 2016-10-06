from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.ext.declarative import declared_attr

db = SQLAlchemy()

class File(db.Model):
    __tablename__ = "files"
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String, nullable=False)
    path = db.Column(db.String, nullable=False)
    size = db.Column(db.Integer, nullable=False)
    type = db.Column(db.Integer, db.ForeignKey('file_types.id'), nullable=False)


class FileType(db.Model):
    __tablename__ = "file_types"
    id = db.Column(db.Integer, primary_key=True)
    category = db.Column(db.String, nullable=False)


class DocumentType(db.Model):
    __tablename__ = "doc_types"
    id = db.Column(db.Integer, primary_key=True)
    category = db.Column(db.String, nullable=False)


class Document(db.Model):
    __abstract__ = True
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String, nullable=False)
    author = db.Column(db.String)
    publisher = db.Column(db.String)
    release_date = db.Column(db.DateTime)

    @declared_attr
    def cover_id(cls):
        return db.Column(db.Integer, db.ForeignKey('files.id'))

    @declared_attr
    def type(cls):
        return db.Column(db.Integer, db.ForeignKey('doc_types.id'), nullable=False)

    @declared_attr
    def file_id(cls):
        return db.Column(db.Integer, db.ForeignKey('files.id'), nullable=False)


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
    page_number = db.Column(db.Integer, nullable=False)
    comic_id = db.Column(db.Integer, db.ForeignKey('comics.id'), nullable=False)
    file_id = db.Column(db.Integer, db.ForeignKey('files.id'), nullable=False)
    comic = db.relationship("Comic", back_populates="pages")

    db.UniqueConstraint('comic_id', 'page_number')


class Epub(Document):
    __tablename__ = "epubs"


class Pdf(Document):
    __tablename__ = "pdf"


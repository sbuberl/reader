from marshmallow_sqlalchemy import ModelSchema

from constants import COMIC_TYPE, EPUB_TYPE, PDF_TYPE, IMAGE_TYPE
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.ext.declarative import declared_attr

db = SQLAlchemy()


class File(db.Model):
    __tablename__ = "files"
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String, nullable=False)
    path = db.Column(db.String, nullable=False)
    size = db.Column(db.Integer, nullable=False)
    type = db.Column(db.Enum(COMIC_TYPE, EPUB_TYPE, PDF_TYPE, IMAGE_TYPE), nullable=False)


class Document(db.Model):
    __tablename__ = "documents"
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String, nullable=False)
    type = db.Column(db.Enum(COMIC_TYPE, EPUB_TYPE, PDF_TYPE), nullable=False)
    author = db.Column(db.String)
    publisher = db.Column(db.String)
    release_date = db.Column(db.DateTime)
    __mapper_args__ = {
        'polymorphic_identity': 'documents',
        'polymorphic_on': type
    }

    @declared_attr
    def cover_id(cls):
        return db.Column(db.Integer, db.ForeignKey('files.id'))

    @declared_attr
    def file_id(cls):
        return db.Column(db.Integer, db.ForeignKey('files.id'), nullable=False)


class Comic(Document):
    __tablename__ = 'comics'
    __mapper_args__ = {'polymorphic_identity': COMIC_TYPE}
    id = db.Column(db.Integer, db.ForeignKey('documents.id'), primary_key=True)
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
    __tablename__ = 'epubs'
    __mapper_args__ = {'polymorphic_identity': EPUB_TYPE}
    id = db.Column(db.Integer, db.ForeignKey('documents.id'), primary_key=True)
    extracted_path = db.Column(db.String, nullable=False)


class Pdf(Document):
    __tablename__ = 'pdfs'
    __mapper_args__ = {'polymorphic_identity': PDF_TYPE}
    id = db.Column(db.Integer, db.ForeignKey('documents.id'), primary_key=True)


class DocumentSchema(ModelSchema):
    class Meta:
        model = Document


class FileSchema(ModelSchema):
    class Meta:
        model = File


class ComicSchema(ModelSchema):
    class Meta:
        model = Comic


class ComicPageSchema(ModelSchema):
    class Meta:
        model = ComicPage


class EpubSchema(ModelSchema):
    class Meta:
        model = Epub


class PdfSchema(ModelSchema):
    class Meta:
        model = Pdf


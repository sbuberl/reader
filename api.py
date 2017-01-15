import os

from flask import make_response
from flask import request, jsonify
from flask_restful import Resource
from flask_restful import reqparse
from marshmallow import ValidationError
from sqlalchemy.exc import SQLAlchemyError
from werkzeug.datastructures import FileStorage

from constants import UPLOAD_FOLDER
from handlers import get_handler
from models import ComicSchema, Comic, Pdf, Epub, db, DocumentSchema, File, ComicPage, Document


class DocumentListResource(Resource):
    def __init__(self):
        self.schema = DocumentSchema()

    def get(self):
        documents = Document.query.all()
        json = self.schema.dump(documents, True)
        return make_response(jsonify({"documents": json.data}), 200)

    def post(self):
        parser = reqparse.RequestParser()
        parser.add_argument('uploaded_file', type=FileStorage, location='files')
        args = parser.parse_args()
        uploaded_file = args['uploaded_file']
        filename = uploaded_file.filename
        uploaded_file_path = os.path.join(UPLOAD_FOLDER, filename)
        uploaded_file.save(uploaded_file_path)
        basename, extension = os.path.splitext(filename)
        extension = extension[1:]
        handler = get_handler(extension)
        if handler:
            document = handler.handle_file(basename, uploaded_file_path)
            db.session.commit()
        json = self.schema.dump(document)
        return jsonify({"document": json.data}), 200


class DocumentResource(Resource):
    def __init__(self, schema, model_class):
        self.schema = schema
        self.model_class = model_class

    def _serialize(self, document):
        json = self.schema.dump(document)
        return jsonify({"document": json.data}), 200

    def get(self, doc_id):
        document = self.model_class.query.get(doc_id)
        if document is None:
            return jsonify({"error": "Document was not found"}), 404
        return self._serialize(document)

    def put(self, doc_id):
        document = self.model_class.query.get(doc_id)
        if document is None:
            return jsonify({"error": "Document was not found"}), 404

        raw_dict = request.get_json(force=True)
        try:
            self.schema.validate(raw_dict)
            user_dict = raw_dict['data']['attributes']
            for key, value in user_dict.items():
                setattr(document, key, value)

            document.update()
            return self._serialize(document)

        except ValidationError as err:
                resp = jsonify({"error": err.messages})
                resp.status_code = 401
                return resp

        except SQLAlchemyError as e:
                db.session.rollback()
                resp = jsonify({"error": str(e)})
                resp.status_code = 401
                return resp

    def delete(self, doc_id):
        document = self.model_class.query.filter_by(id=doc_id).one()
        if document.cover_id:
            cover_file = File.query.filter_by(id=document.cover_id).one()
            db.session.delete(cover_file)
        document_file = File.query.filter_by(id=document.file_id).one()
        db.session.delete(document_file)
        db.session.delete(document)
        db.session.commit()


class ComicResource(DocumentResource):
    def __init__(self):
        super(ComicResource, self).__init__(ComicSchema(), Comic)

    def delete(self, doc_id):
        comic = self.model_class.query.filter_by(id=doc_id).one()
        for page in comic.pages:
            page_file = File.query.filter_by(id=page.file_id).one()
            db.session.delete(page_file)
            db.session.delete(page)

        super(ComicResource, self).delete(doc_id)


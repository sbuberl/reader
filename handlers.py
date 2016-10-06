from constants import LIBRARY_FOLDER, THUMBNAILS
import imghdr
from models import Comic, ComicPage, File, FileType, DocumentType, Epub, Pdf
import os
from PIL import Image
from rarfile import RarFile
import re
from shutil import copyfile
from tarfile import TarFile
from utils import add_and_refresh, path_leaf
from zipfile import ZipFile

class BaseHandler:
    def make_cover_thumbnail(self, cover_name, cover_path, book_name, image_type):
        cover_extension = os.path.splitext(cover_name)[1]
        thumbnail_name = '{0}{1}'.format(book_name, cover_extension)
        thumbnail_path = os.path.join(THUMBNAILS, thumbnail_name)
        if os.path.exists(thumbnail_path):
            os.remove(thumbnail_path)
        im = Image.open(cover_path)
        im.thumbnail((200, 200))
        im.save(thumbnail_path)
        thumbnail = File(name=cover_name, path=thumbnail_path, size=os.path.getsize(thumbnail_path), type=image_type)
        add_and_refresh(thumbnail)
        return thumbnail

    def save_original_file(self, uploaded_file, type_value):
        file_name = path_leaf(uploaded_file)
        library_path = os.path.join(LIBRARY_FOLDER, file_name)
        copyfile(uploaded_file, library_path)
        file_type = FileType.query.filter_by(category=type_value).one()
        size = os.path.getsize(library_path)
        new_file = File(name=file_name, path=library_path, size=size, type=file_type.id)
        add_and_refresh(new_file)
        return new_file


class ComicHandler(BaseHandler):
    def _get_info_filename(self, info):
        return info.filename

    def _get_info_size(self, info):
        return info.file_size

    def _get_info_list(self, archive):
        return archive.infolist()

    def handle_file(self, name, comic_file_path):
        comic_doc = DocumentType.query.filter_by(category='comic').one()
        comic_file = self.save_original_file(comic_file_path, 'comic')
        comic = Comic(name=name, type=comic_doc.id, file_id=comic_file.id)
        match = re.match("(.+?)\s+(\d+)\.", comic_file_path)
        if match:
            comic.series = match.group(1)
            comic.issue = match.group(2)
        add_and_refresh(comic)
        image_type = FileType.query.filter_by(category='image').one()
        extracted_path = os.path.join(LIBRARY_FOLDER, name)
        self.extract_file(comic, comic_file_path, extracted_path, image_type)

    def _extract_archve_info(self, archive, comic, extracted_path, image_type):
        page_number = 1
        info_list = self._get_info_list(archive)
        is_zip = isinstance(archive, ZipFile)
        for info in info_list:
            info_file_name = self._get_info_filename(info)
            info_head = os.path.split(info_file_name)[0]
            if info_head:
                extracted_sub_dir = os.path.join(extracted_path, info_head)
                if not os.path.isdir(extracted_sub_dir):
                    os.makedirs(extracted_sub_dir)
            page_path = os.path.join(extracted_path, info_file_name)
            if not is_zip and info.isdir():
                continue
            archive.extract(info_file_name, extracted_path)
            page_type = imghdr.what(page_path)
            if page_type:
                page_file_name = path_leaf(info_file_name)
                page_path = os.path.join(extracted_path, info_file_name)
                page_size = self._get_info_size(info)
                page_file = File(name=page_file_name, path=page_path, size=page_size, type=image_type.id)
                add_and_refresh(page_file)
                page = ComicPage(page_number=page_number, comic_id=comic.id, file_id=page_file.id)
                page_number += 1
                add_and_refresh(page)
        first_page_index = 0
        first_page = self._get_info_filename(info_list[first_page_index])
        while not is_zip and info_list[first_page_index].isdir():
            first_page_index += 1
            first_page = self._get_info_filename(info_list[first_page_index])
        first_page_path = os.path.join(extracted_path, first_page)
        cover = self.make_cover_thumbnail(first_page, first_page_path, comic.name, image_type.id)
        comic.cover_id = cover.id


class CbzHandler(ComicHandler):
    def extract_file(self, comic, comic_file_path, extracted_path, image_type):
        with ZipFile(comic_file_path) as zip:
            self._extract_archve_info(zip, comic, extracted_path, image_type)


class CbrHandler(ComicHandler):
    def extract_file(self, comic, comic_file_path, extracted_path, image_type):
        with RarFile(comic_file_path) as rar:
            self._extract_archve_info(rar, comic, extracted_path, image_type)


class CbtHandler(ComicHandler):
    def _get_info_filename(self, info):
        return info.name

    def _get_info_size(self, info):
        return info.size

    def _get_info_list(self, archive):
        return archive.getmembers()

    def extract_file(self, comic, comic_file_path, extracted_path, image_type):
        with TarFile(comic_file_path) as tar:
            self._extract_archve_info(tar, comic, extracted_path, image_type)


class EpubHandler(BaseHandler):

    def handle_file(self, name, epub_file_path):
        epub_file = self.save_original_file(epub_file_path, 'epub')
        epub_doc = DocumentType.query.filter_by(category='epub').one()
        extracted_path = os.path.join(LIBRARY_FOLDER, name)
        self._extract_zip(epub_file.path, extracted_path)
        epub = Epub(name=name, file_id=epub_file.id, type=epub_doc.id, extracted_path=extracted_path)
        add_and_refresh(epub)

    def _extract_zip(self, epub_library_file, extracted_path):
        with ZipFile(epub_library_file) as archive:
            archive.extractall(extracted_path)

class PdfHandler(BaseHandler):
    def handle_file(self, name, pdf_file_path):
        pdf_file = self.save_original_file(pdf_file_path, 'pdf')
        pdf_doc = DocumentType.query.filter_by(category='pdf').one()
        pdf = Pdf(name=name, file_id=pdf_file.id, type=pdf_doc.id)
        add_and_refresh(pdf)




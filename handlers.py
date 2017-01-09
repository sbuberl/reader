import abc
from constants import LIBRARY_FOLDER, THUMBNAILS, IMAGE_TYPE, PDF_TYPE, EPUB_TYPE, COMIC_TYPE
from datetime import datetime
import dateutil.parser
import epub
import imghdr
from models import Comic, ComicPage, File, Epub, Pdf
import os
from PIL import Image
from PyPDF2 import PdfFileReader
from rarfile import RarFile
import re
from tarfile import TarFile
from utils import add_and_refresh, path_leaf
from zipfile import ZipFile


ABC = abc.ABCMeta('ABC', (object,), {})  # compatible with Python 2 *and* 3


class BaseHandler(ABC):
    def __init__(self):
        pass

    @abc.abstractmethod
    def handle_file(self, name, upload_file_path):
        pass

    @staticmethod
    def _make_cover_thumbnail(cover_name, cover_path, book_name):
        cover_extension = os.path.splitext(cover_name)[1]
        thumbnail_name = '{0}{1}'.format(book_name, cover_extension)
        thumbnail_path = os.path.join(THUMBNAILS, thumbnail_name)
        if os.path.exists(thumbnail_path):
            os.remove(thumbnail_path)
        im = Image.open(cover_path)
        im.thumbnail((200, 200))
        im.save(thumbnail_path)
        thumbnail = File(name=cover_name, path=thumbnail_path, size=os.path.getsize(thumbnail_path), type=IMAGE_TYPE)
        add_and_refresh(thumbnail)
        return thumbnail

    @staticmethod
    def _save_original_file(uploaded_file, file_type):
        file_name = path_leaf(uploaded_file)
        library_path = os.path.join(LIBRARY_FOLDER, file_name)
        os.rename(uploaded_file, library_path)
        size = os.path.getsize(library_path)
        new_file = File(name=file_name, path=library_path, size=size, type=file_type)
        add_and_refresh(new_file)
        return new_file


class ComicHandler(BaseHandler):
    def _get_info_filename(self, info):
        return info.filename

    def _get_info_size(self, info):
        return info.file_size

    def _get_info_list(self, archive):
        return archive.infolist()

    def handle_file(self, name, upload_file_path):
        comic_file = self._save_original_file(upload_file_path, COMIC_TYPE)
        comic = Comic(name=name, type=COMIC_TYPE, file_id=comic_file.id)
        match = re.match("(.+?)\s+(\d+)$", name)
        if match:
            comic.series = match.group(1)
            comic.issue = match.group(2)
        add_and_refresh(comic)
        extracted_path = os.path.join(LIBRARY_FOLDER, name)
        self.extract_file(comic, comic_file.path, extracted_path)
        return comic

    def _extract_archive_info(self, archive, comic, extracted_path):
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
                page_file = File(name=page_file_name, path=page_path, size=page_size, type=IMAGE_TYPE)
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
        cover = self._make_cover_thumbnail(first_page, first_page_path, comic.name)
        comic.cover_id = cover.id


class CbzHandler(ComicHandler):
    def extract_file(self, comic, comic_file_path, extracted_path):
        with ZipFile(comic_file_path) as zip_file:
            self._extract_archive_info(zip_file, comic, extracted_path)


class CbrHandler(ComicHandler):
    def extract_file(self, comic, comic_file_path, extracted_path):
        with RarFile(comic_file_path) as rar_file:
            self._extract_archive_info(rar_file, comic, extracted_path)


class CbtHandler(ComicHandler):
    def _get_info_filename(self, info):
        return info.name

    def _get_info_size(self, info):
        return info.size

    def _get_info_list(self, archive):
        return archive.getmembers()

    def extract_file(self, comic, comic_file_path, extracted_path):
        with TarFile(comic_file_path) as tar_file:
            self._extract_archive_info(tar_file, comic, extracted_path)


class EpubHandler(BaseHandler):
    def handle_file(self, name, epub_file_path):
        epub_file = self._save_original_file(epub_file_path, EPUB_TYPE)
        extracted_path = os.path.join(LIBRARY_FOLDER, name)
        self._extract_zip(epub_file.path, extracted_path)
        (title, creators, publisher, release_date, cover_id) = self._read_epub_meta(epub_file.path, extracted_path)
        epub_obj = Epub(name=title, file_id=epub_file.id, type=EPUB_TYPE, extracted_path=extracted_path,
                        author=creators, publisher=publisher, release_date=release_date, cover_id=cover_id)
        add_and_refresh(epub_obj)
        return epub_obj

    @staticmethod
    def _read_epub_meta(epub_library_file, extracted_path):
        with epub.open_epub(epub_library_file, 'r') as epub_file:
            metadata = epub_file.opf.metadata
            title = metadata.titles[0][0]                                       # (title, lang)
            creators = ', '.join([x[0] for x in metadata.creators])             # (name, role, file_as)
            publisher = metadata.publisher
            release_date = None
            if metadata.dates:
                try:
                    release_date = dateutil.parser.parse(metadata.dates[0][0])  # (date, event)
                except (ValueError, OverflowError):
                    pass

            cover_id = next((x[1] for x in metadata.metas if x[0] == 'cover'), None)     # {name, value)
            thumbnail_id = None
            if cover_id:
                cover_manifest = epub_file.get_item(cover_id)
                cover_rel_path = cover_manifest.href
                if os.name == 'nt':
                    cover_rel_path = cover_rel_path.replace("/", "\\")
                cover_file_name = path_leaf(cover_rel_path)
                cover_path = os.path.join(extracted_path, epub_file.content_path, cover_rel_path)
                thumbnail = BaseHandler._make_cover_thumbnail(cover_file_name, cover_path, title)
                thumbnail_id = thumbnail.id
            return title, creators, publisher, release_date, thumbnail_id

    @staticmethod
    def _extract_zip(epub_library_file, extracted_path):
        with ZipFile(epub_library_file) as archive:
            archive.extractall(extracted_path)


class PdfHandler(BaseHandler):
    def handle_file(self, name, pdf_file_path):
        pdf_file = self._save_original_file(pdf_file_path, PDF_TYPE)
        (title, author, release_date) = self._read_pdf_meta(pdf_file.path, name)
        pdf = Pdf(name=title, file_id=pdf_file.id, type=PDF_TYPE, author=author, release_date=release_date)
        add_and_refresh(pdf)
        return pdf

    @staticmethod
    def _read_pdf_meta(pdf_file_path, name):
        pdf_stream = open(pdf_file_path, "rb")
        pdf_reader = PdfFileReader(pdf_stream)
        pdf_info = pdf_reader.getDocumentInfo()
        title = name
        author = None
        release_date = None
        if '/Title' in pdf_info:
            title = pdf_info['/Title']
        if '/Author' in pdf_info:
            author = pdf_info['/Author']
        if '/CreationDate' in pdf_info:
            date_string = pdf_info['/CreationDate'].replace("'", '')        # D:YYYYMMDDHHmmSSOHH'mm'
            release_date = datetime.strptime(date_string, 'D:%Y%m%d%H%M%S')
        return title, author, release_date


_handler_lookup = {'cbr': CbrHandler, 'cbt': CbtHandler, 'cbz': CbzHandler, 'epub': EpubHandler, 'pdf': PdfHandler}


def get_handler(extension):
    handler = _handler_lookup[extension]
    if handler:
        return handler()
    else:
        return None

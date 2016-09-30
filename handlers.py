from constants import LIBRARY_FOLDER, THUMBNAILS
import imghdr
from models import Comic, ComicPage, File, FileType
import os
from PIL import Image
from rarfile import RarFile
import re
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


class ComicHandler(BaseHandler):
    def handle_file(self, name, comic_file_path):
        comic = Comic(name=name)
        match = re.match("(.+?)\s+(\d+)\.", comic_file_path)
        if match:
            comic.series = match.group(1)
            comic.issue = match.group(2)
        add_and_refresh(comic)
        image_type = FileType.query.filter_by(category='image').first()
        extracted_path = os.path.join(LIBRARY_FOLDER, name)
        self.extract_file(comic, comic_file_path, extracted_path, image_type)


class CbrCbzBaseHandler(ComicHandler):
    def extract_archve_info(self, archive, comic, extracted_path, image_type):
        page_number = 1
        info_list = archive.infolist()
        is_rar = isinstance(archive, RarFile)
        for info in info_list:
            info_file_name = info.filename
            info_head = os.path.split(info_file_name)[0]
            if info_head:
                extracted_sub_dir = os.path.join(extracted_path, info_head)
                if not os.path.isdir(extracted_sub_dir):
                    os.makedirs(extracted_sub_dir)
            page_path = os.path.join(extracted_path, info_file_name)
            if is_rar and info.isdir():
                continue
            archive.extract(info_file_name, extracted_path)
            page_type = imghdr.what(page_path)
            if page_type:
                page_file_name = path_leaf(info_file_name)
                page_path = os.path.join(extracted_path, info.filename)
                page_file = File(name=page_file_name, path=page_path, size=info.file_size, type=image_type.id)
                add_and_refresh(page_file)
                page = ComicPage(page_number=page_number, comic_id=comic.id, file_id=page_file.id)
                page_number += 1
                add_and_refresh(page)
        first_page = info_list[0].filename
        first_page_path = os.path.join(extracted_path, first_page)
        cover = self.make_cover_thumbnail(first_page, first_page_path, comic.name, image_type.id)
        comic.cover_id = cover.id

class CbzHandler(CbrCbzBaseHandler):
    def extract_file(self, comic, comic_file_path, extracted_path, image_type):
        with ZipFile(comic_file_path) as zip:
            self.extract_archve_info(zip, comic, extracted_path, image_type)

class CbrHandler(CbrCbzBaseHandler):
    def extract_file(self, comic, comic_file_path, extracted_path, image_type):
        with RarFile(comic_file_path) as rar:
            self.extract_archve_info(rar, comic, extracted_path, image_type)






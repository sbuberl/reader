from models import db
import os


def add_and_refresh(model_object):
    db.session.add(model_object)
    db.session.flush()
    db.session.refresh(model_object)


def path_leaf(path):
    head, tail = os.path.split(path)
    return tail or os.path.basename(head)

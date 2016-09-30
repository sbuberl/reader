from models import db
import os

def add_and_refresh(object):
    db.session.add(object)
    db.session.flush()
    db.session.refresh(object)


def path_leaf(path):
    head, tail = os.path.split(path)
    return tail or os.path.basename(head)

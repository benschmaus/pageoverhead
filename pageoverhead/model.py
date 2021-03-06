import string
import logging
from google.appengine.ext import db
from google.appengine.ext.db import polymodel
from pageoverhead import util

def get(filters, entity_class):
    query = entity_class.all()
    for filter_type, filter_value in filters.iteritems():
        query.filter(filter_type, filter_value)
    return query.get()

def fetch(filters, entity_class):
    query = entity_class.all()
    for filter_type, filter_value in filters.iteritems():
        query.filter(filter_type, filter_value)
    return query

class BaseEntity(db.Model):
    created = db.DateTimeProperty(auto_now_add=True)
    modified = db.DateTimeProperty(auto_now=True)
    user = db.UserProperty(auto_current_user_add=True)
    url = db.StringProperty()

    def local_modified(self):
        return self.modified.replace(tzinfo=util.UTC_tzinfo()).astimezone(util.Eastern_tzinfo())

class Bookmark(BaseEntity):
    access = db.StringProperty(choices=set(['private','public']))

class BookmarkNote(BaseEntity):
    owner = db.UserProperty()
    note = db.StringProperty(multiline=True)
    top = db.StringProperty()
    left = db.StringProperty()
    width = db.StringProperty()
    height = db.StringProperty()

    def note_as_one_line(self):
        return string.replace(self.note, '\n', '\\n')

class BookmarkTag(BaseEntity):
    tag = db.StringProperty()

class BookmarkCollaborator(BaseEntity):
    """ A collaborator can read and edit notes on an overhead """
    collaborator = db.UserProperty()

class BookmarkLink(BaseEntity):
    """Link someone elses public notes to one of your bookmarks"""
    pass



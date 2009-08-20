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
    author = db.UserProperty(auto_current_user_add=True)
    note = db.StringProperty(multiline=True)
    top = db.StringProperty()
    left = db.StringProperty()
    width = db.StringProperty()
    height = db.StringProperty()

class BookmarkTag(BaseEntity):
    tag = db.StringProperty()

class BookmarkCollaborator(BaseEntity):
    """Enable a boorkmark to be viewed by specific collaborators"""
    pass

class BookmarkLink(BaseEntity):
    """Link someone elses public notes to one of your bookmarks"""
    pass



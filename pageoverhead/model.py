import from google.appengine.ext import db

class BaseEntity(db.Model):
    created = db.DateTimeProperty(auto_now_add=True)
    modified = db.DateTimeProperty(auto_now=True)

class Bookmark(BaseEntity):
    user = db.UserProperty(auto_current_user_add=True)
    url = db.StringProperty()
    access = db.StringProperty(choices=set(['private','public']))

class BookmarkNote(BaseEntity):
    user = db.UserProperty(auto_current_user_add=True)
    url = db.StringProperty()
    author = db.UserProperty(auto_current_user=True)
    note = db.StringProperty(multiline=True)

class BookmarkTag(BaseEntity):
    user = db.UserProperty(auto_current_user_add=True)
    url = db.StringProperty()
    tag = db.StringProperty()

class BookmarkCollaborator(BaseEntity):
    """Enable a boorkmark to be viewed by specific collaborators"""
    pass

class BookmarkLink(BaseEntity):
    """Link someone elses public notes to one of your bookmarks"""
    pass


import from google.appengine.ext import db

class BaseEntity(polymodel.PolyModel):
    created = db.DateTimeProperty(auto_now_add=True)
    modified = db.DateTimeProperty(auto_now=True)
    user = db.UserProperty(auto_current_user_add=True)
    url = db.StringProperty()

class Bookmark(BaseEntity):
    access = db.StringProperty(choices=set(['private','public']))

class BookmarkNote(BaseEntity):
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


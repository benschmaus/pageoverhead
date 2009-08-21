import logging
import cgi
import os
import urllib
from google.appengine.ext import db
from google.appengine.api import users
from google.appengine.ext import webapp
from google.appengine.ext.webapp import template
from pageoverhead import auth
from pageoverhead import model

class NoteHandler(webapp.RequestHandler):
    """ Handles adding notes for a particular user's bookmark """

    # TODO ???Add param to decorator so we can check logged in user against user in request
    @auth.AuthenticationDecorator
    def get(self, user, page, note_id = None):
        current_user = users.get_current_user()
        user = urllib.unquote_plus(user)
        bookmark_notes = model.fetch({"owner =": users.User(user), "url =": page}, model.BookmarkNote)

        tmpl_vars = {
            "notes": bookmark_notes
        }
        self.response.headers['Content-Type'] = 'application/json'
        self.response.out.write(template.render('tmpl/notes_json.tmpl', tmpl_vars))

    # Note that if the user sends a POST but is logged out we need some workaround
    # to handle the POST after the user logs in.
    @auth.AuthenticationDecorator
    def post(self, user, page, note_id = None):
        """ Saves a new note, updates or deletes an existing one. """

        user = urllib.unquote_plus(user)
        current_user = users.get_current_user()
        logging.info('Request to modify note for user %s, page %s, note_id %s' % (user, page, note_id))

        bookmark_note = None
        if note_id:
            note_id = note_id.strip()
            bookmark_note = model.get({ "user =": current_user, "url =": page, "__key__ =": db.Key(note_id) }, model.BookmarkNote)
            logging.info('Updating existing bookmark note %s' % bookmark_note)

        if not bookmark_note:
            logging.info('Creating new bookmark note')
            bookmark_note = model.BookmarkNote()

        json = None
        if self.request.get('delete'):
            logging.debug('Deleting bookmark note')
            json = '{ "key": "%s" }' % bookmark_note.key()
            bookmark_note.delete()
        else:
            logging.debug('Saving bookmark note')
            bookmark_note.note = self.request.get('note_text')
            bookmark_note.url = page
            bookmark_note.owner = users.User(user)
            bookmark_note.top = self.request.get('note_top')
            bookmark_note.left = self.request.get('note_left')
            bookmark_note.width = self.request.get('note_width')
            bookmark_note.height = self.request.get('note_height')
            bookmark_note.put()
            json = '{ "key": "%s" }' % bookmark_note.key()

        self.response.headers['Content-Type'] = 'application/json'
        self.response.out.write(json)


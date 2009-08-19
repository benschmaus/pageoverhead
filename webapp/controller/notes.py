import cgi
import os
import urllib
from google.appengine.api import users
from google.appengine.ext import webapp
from google.appengine.ext.webapp.util import run_wsgi_app
from google.appengine.ext.webapp import template
from pageoverhead import auth
from pageoverhead import model

class NotesHandler(webapp.RequestHandler):
    """ Handles adding notes for a particular user's bookmark """

    # TODO ???Add param to decorator so we can check logged in user against user in request
    @auth.AuthenticationDecorator
    def get(self, user, page, note_id = None):
        current_user = users.get_current_user()
        self.response.headers['Content-Type'] = 'text/plain'
        self.response.out.write('GET "%s" "%s" "%s"' % (user, page, note_id))

    # Note that if the user sends a POST but is logged out we need some workaround
    # to handle the POST after the user logs in.
    @auth.AuthenticationDecorator
    def post(self, user, page, note_id = None):
        """ Saves a note. """
        self.response.headers['Content-Type'] = 'text/plain'
        self.response.out.write('POST %s' % self.request.uri)


application = webapp.WSGIApplication(
    [
        ('/([^/]+)/overheads/([^/]+)/notes/?([^/]+)?', NotesHandler)
    ],
    debug=True
)

def main():
    run_wsgi_app(application)

if __name__ == "__main__":
    main()


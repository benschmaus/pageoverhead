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

class CollaboratorHandler(webapp.RequestHandler):
    """ Handles adding collaborators to a particular user's bookmark """

    # TODO ???Add param to decorator so we can check logged in user against user in request
    @auth.AuthenticationDecorator
    def get(self, user, page):
        current_user = users.get_current_user()
        self.response.headers['Content-Type'] = 'text/plain'
        self.response.out.write('GET "%s" "%s" "%s"' % (user, page))

    # Note that if the user sends a POST but is logged out we need some workaround
    # to handle the POST after the user logs in.
    @auth.AuthenticationDecorator
    def post(self, user, page):
        """ Updates a bookmark's collaborators """
        current_user = users.get_current_user()
        logging.debug('Request to modify collaborators for user %s, page %s' % (user, page))

        collaborators_str = self.request.get('collaborators')
        collaborators = collaborators_str.split()

        # Go thru existing collaborators and remove any from the POST that
        # we already have, otherwise get rid of them.

        bookmark_collaborators = model.fetch({ "user =": current_user, "url =": page }, model.BookmarkCollaborator)

        for bookmark_collaborator in bookmark_collaborators:
            if bookmark_collaborator not in collaborators:
                bookmark_collaborator.delete()
            else:
                collaborators.remove(bookmark_collaborator)

        collaborator_keys = []
        # Go thru remaining collaborators and add them
        for collaborator in collaborators:
            bookmark_collaborator = model.BookmarkCollaborator()
            bookmark_collaborator.collaborator = users.User(collaborator)
            bookmark_collaborator.url = page
            bookmark_collaborator.put()
            collaborator_keys.append("'%s'" % str(bookmark_collaborator.key()))

        keys_str = ','.join(collaborator_keys)
        json = '{ "collaborators": [%s] }' % keys_str
        logging.info(json)
        self.response.headers['Content-Type'] = 'application/json'
        self.response.out.write(json)



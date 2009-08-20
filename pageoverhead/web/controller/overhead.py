import logging
import cgi
import os
import urllib
from google.appengine.api import users
from google.appengine.ext import webapp
from google.appengine.ext.webapp import template
from pageoverhead import auth
from pageoverhead import model

class OverheadHandler(webapp.RequestHandler):

    # TODO ???Add param to decorator so we can check logged in user against user in request
    @auth.AuthenticationDecorator
    def get(self, request_user, page):
        request_user = urllib.unquote_plus(request_user)
        page = urllib.unquote_plus(page)

        current_user = users.get_current_user()
        logging.debug('getting overhead user: %s, page: %s for %s' % (request_user, page, current_user))
        bookmark = model.get({"user =": users.User(request_user), "url =": page}, model.Bookmark)
        bookmark_tags = model.fetch({"user =": users.User(request_user), "url =": page}, model.BookmarkTag)
        # TODO Get notes for the user associated with the request and all other collaborators
        bookmark_notes = model.fetch({"user =": users.User(request_user), "url =": page}, model.BookmarkNote)
        logging.debug('fetched %d bookmark notes', bookmark_notes.count())

        access = ""
        tags_str = ""

        if bookmark:
            access = bookmark.access

        if bookmark_tags:
            def f(x): return x.tag
            bookmark_tags = map(f, bookmark_tags)
            tags_str = ' '.join(bookmark_tags)

        tmpl_vars = {
            "user": request_user,
            "page": page,
            "access": access,
            "tags": tags_str,
            "notes": bookmark_notes
        }

        self.response.headers['Content-Type'] = 'text/html'
        self.response.out.write(template.render('tmpl/overhead.tmpl', tmpl_vars))

    # Note that if the user sends a POST but is logged out we need some workaround
    # to handle the POST after the user logs in.
    @auth.AuthenticationDecorator
    def post(self, request_user, page):
        """ Saves a bookmark. """
        request_user = urllib.unquote_plus(request_user)
        page = urllib.unquote_plus(page)
        current_user = users.get_current_user()

        tags_str = self.request.get('tags')
        tags = tags_str.split()

        access = self.request.get('access')
        if access != 'public':
            access = 'private'

        self.update_bookmark(page, tags, access)

        bookmark_notes = model.fetch({"user =": current_user, "url =": page}, model.BookmarkNote)

        tmpl_vars = {
            "user": request_user,
            "page": page,
            "tags": tags_str,
            "access": access,
            "notes": ()
        }

        self.response.headers['Content-Type'] = 'text/html'
        self.response.out.write(template.render('tmpl/overhead.tmpl', tmpl_vars))

    def update_bookmark(self, page, tags, access):
        current_user = users.get_current_user()
        bookmark = model.get({ "user =": current_user, "url =": page }, model.Bookmark)

        if bookmark == None:
            bookmark = model.Bookmark()
            bookmark.url = page

        bookmark.access = access

        bookmark.put()

        # Now update tags
        bookmark_tags = model.fetch({ "user =": current_user, "url =": page }, model.BookmarkTag)

        for bookmark_tag in bookmark_tags:
            # if existing tag isn't in list of tags submitted by user remove it,
            # otherwise remove tag from list of user-submitted tags
            if bookmark_tag not in tags:
                bookmark_tag.delete()
            else:
                tags.remove(bookmark_tag)

        # Go thru remaining user-submitted tags and add them
        for tag in tags:
            bookmark_tag = model.BookmarkTag()
            bookmark_tag.url = page
            bookmark_tag.tag = tag
            bookmark_tag.put()



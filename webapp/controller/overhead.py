import cgi
import os
import urllib
from google.appengine.api import users
from google.appengine.ext import webapp
from google.appengine.ext.webapp.util import run_wsgi_app
from google.appengine.ext.webapp import template
from pageoverhead import auth

class OverheadPage(webapp.RequestHandler):

    # TODO ???Add param to decorator so we can check logged in user against user in request
    @auth.AuthenticationDecorator
    def get(self, user, page):

        tmpl_vars = {
            "user": urllib.unquote_plus(user),
            "page": page
        }

        path = os.path.join(os.path.dirname(__file__), '../tmpl/overhead.tmpl')

        self.response.headers['Content-Type'] = 'text/html'
        self.response.out.write(template.render(path, tmpl_vars))

    # Note that if the user sends a POST but is logged out we need some workaround
    # to handle the POST after the user logs in.
    @auth.AuthenticationDecorator
    def post(self, user, page):
        tags_str = self.request.get('tags')
        tags = tags_str.split()

        access = self.request.get('access')
        if access != 'public':
            access = 'private'

        tmpl_vars = {
            "user": urllib.unquote_plus(user),
            "page": page,
            "tags": tags_str,
            "access": access
        }

        path = os.path.join(os.path.dirname(__file__), '../tmpl/overhead.tmpl')

        self.response.headers['Content-Type'] = 'text/html'
        self.response.out.write(template.render(path, tmpl_vars))

application = webapp.WSGIApplication(
    [ ('/overheads/(.*)/(.*)', OverheadPage) ],
    debug=True
)

def main():
    run_wsgi_app(application)

if __name__ == "__main__":
    main()

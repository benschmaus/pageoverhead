import cgi
import os
from google.appengine.api import users
from google.appengine.ext import webapp
from google.appengine.ext.webapp.util import run_wsgi_app
from google.appengine.ext.webapp import template
from pageoverhead import auth

class OverheadPage(webapp.RequestHandler):

    @auth.AuthenticationDecorator
    def get(self, user, page):

        tmpl_vars = {"page": page}

        path = os.path.join(os.path.dirname(__file__), '../tmpl/overhead.tmpl')

        self.response.headers['Content-Type'] = 'text/html'
        self.response.out.write(template.render(path, tmpl_vars))

    # Note that if the user is logged out we need some workaround
    # to handle the POST after the user logs in.
    @auth.AuthenticationDecorator
    def post(self, user, url):
        self.response.headers['Content-Type'] = 'text/plain'
        self.response.out.write('POST');

application = webapp.WSGIApplication(
    [ ('/overhead', OverheadPage) ],
    debug=True
)

def main():
    run_wsgi_app(application)

if __name__ == "__main__":
    main()
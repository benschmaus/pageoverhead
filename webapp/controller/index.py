import cgi
import urllib
import os
from google.appengine.api import users
from google.appengine.ext import webapp
from google.appengine.ext.webapp.util import run_wsgi_app
from google.appengine.ext.webapp import template

class IndexPage(webapp.RequestHandler):
    """ Displays main app page with link to create an overhead for a new URL."""
    def get(self):

        user = users.get_current_user()
        email = ''
        nickname = ''
        if user:
            email = user.email()
            nickname = user.nickname()

        tmpl_vars = {
            "user_email" : email,
            "user_nickname" : urllib.quote_plus(nickname),
            "login_url" : users.create_login_url(self.request.uri),
            "logout_url" : users.create_logout_url(self.request.uri)
        }

        path = os.path.join(os.path.dirname(__file__), '../tmpl/index.tmpl')

        self.response.headers['Content-Type'] = 'text/html'
        self.response.out.write(template.render(path, tmpl_vars))

application = webapp.WSGIApplication(
    [ ('/', IndexPage) ],
    debug=True
)

def main():
    run_wsgi_app(application)

if __name__ == "__main__":
    main()

import os
from google.appengine.ext import webapp
from google.appengine.ext.webapp.util import run_wsgi_app
from google.appengine.ext.webapp import template

class MainPage(webapp.RequestHandler):
  def get(self):
    page = self.request.get('p')
    self.response.headers['Content-Type'] = 'text/html'
    tmpl_vars = {"page": page}
    path = os.path.join(os.path.dirname(__file__), 'tmpl/index.tmpl')
    self.response.out.write(template.render(path, tmpl_vars))

application = webapp.WSGIApplication(
    [('/', MainPage)],
    debug=True
)

def main():
  run_wsgi_app(application)

if __name__ == "__main__":
  main()
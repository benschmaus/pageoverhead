from google.appengine.ext import webapp
from google.appengine.ext.webapp.util import run_wsgi_app

from pageoverhead.web.controller import index
from pageoverhead.web.controller import overheads
from pageoverhead.web.controller import notes
from pageoverhead.web.controller import collaborators

application = webapp.WSGIApplication(
    [
        ('/', index.IndexHandler),
        ('/([^/]+)/overheads/([^/]+)/notes/?([^/]+)?/?', notes.NoteHandler),
        ('/([^/]+)/overheads/([^/]+)/collaborators/?', collaborators.CollaboratorHandler),
        ('/([^/]+)/overheads/([^/]*)/?', overheads.OverheadHandler)
    ],
    debug=True
)

def main():
    run_wsgi_app(application)

if __name__ == "__main__":
    main()


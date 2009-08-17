from google.appengine.api import users

class AuthenticationDecorator(object):
    """ Redirects current request to Google login page if no user is logged in."""

    def __init__(self, function_to_wrap):
        self.wrapped_function = function_to_wrap

    def __call__(self, *args):
        user = users.get_current_user()
        if user == None:
             self.wrapped_handler.redirect(users.create_login_url(self.wrapped_handler.request.uri))

        self.wrapped_function(self.wrapped_handler, *args)

    def __get__(self, handler_to_wrap, cls):
        self.wrapped_handler = handler_to_wrap
        return self

import logging

__author__ = 'dhensche'

import webapp2
import jinja2
import os
from hasher import Hash

template_dir = os.path.join(os.path.dirname(__file__), '../templates')
jinja_env = jinja2.Environment(loader=jinja2.FileSystemLoader(template_dir), autoescape=True)

class Handler(webapp2.RequestHandler):
    def write(self, *a, **kw):
        self.response.out.write(*a, **kw)

    def render_str(self, template, **params):
        t = jinja_env.get_template(template)
        return t.render(params)

    def render(self, template, **kw):
        self.write(self.render_str(template, **kw))

    def set_cookie(self, name, value, expires=None):
        if expires is None:
            self.response.headers.add_header('Set-Cookie', '%s=%s; Path=/' % (name, Hash.hash_cookie(str(value))))
        else:
            self.response.headers.add_header('Set-Cookie', '%s=%s; Path=/; Expires=%s' % (name, Hash.hash_cookie(str(value)), expires))

    def set_plaintext_cookie(self, name, value):
        self.response.headers.add_header('Set-Cookie', '%s=%s; Path=/' % (name, str(value)))

    def get_cookie(self, name):
        return Hash.dehash_cookie(self.request.cookies.get(name)) if self.request.cookies.get(name) else None

    def remove_cookies(self):
        for cookie in self.request.cookies:
            self.set_cookie(str(cookie), '', 'Thu, 01-Jan-1970 00:00:00 GMT')
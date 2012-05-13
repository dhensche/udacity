from google.appengine.ext import db

__author__ = 'dhensche'

from util.handler import Handler
import re
from util.hasher import Hash
from model.user import User
import logging

class SignUp(Handler):
    username, email, error, password, verify = '', '', {}, '', ''

    def render_form(self):
        self.render('signup/form.html', username=self.username, email=self.email, error=self.error)

    def get(self):
        self.render_form()

    def post(self):
        if not self.validate(self.request):
            self.render_form()
        else:
            user = User(name=self.username, password_hash=Hash.password(self.username, self.password), email=(self.email if self.email else None ))
            user.put()
            self.set_cookie('userid', user.key())
            self.redirect('/home')

    def validate(self, request):
        self.username, self.password = request.get('username'), request.get('password')
        self.verify, self.email = request.get('verify'), request.get('email')

        self.error['user'] = 'Invalid Username' if not re.search('^[a-zA-Z0-9_-]{3,20}$', self.username) else ''
        self.error['email'] = 'Invalid Email' if self.email and not re.search('^[\S]+@[\S]+\.[\S]+$', self.email) else ''
        self.error['password'] = 'Invalid Password' if not re.search('^.{3,20}$', self.password) else ''
        self.error['verify'] = 'First password does not match second' if self.password != self.verify else ''
        return len(''.join(self.error.values())) == 0

class Login(Handler):
    username, error = '', ''
    def render_form(self):
        self.render('login.html', username=self.username, error=self.error)

    def get(self):
        self.render_form()

    def post(self):
        self.username = self.request.get('username')
        user = User.find_by_username_and_password(self.username, self.request.get('password'))
        if user is not None:
            self.set_cookie('userid', user.key())
            self.redirect('/home')
        else:
            self.error = 'Invalid username or password'
            self.render_form()

class Logout(Handler):
    def get(self):
        self.set_plaintext_cookie('userid', '')
        self.redirect('/signup')

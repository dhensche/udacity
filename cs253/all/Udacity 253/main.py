#!/usr/bin/env python
#
# Copyright 2007 Google Inc.
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.
#
import webapp2
import logging
import string
import cgi
import re

form_hw2_p1="""
<form method="POST">
    <textarea name="text" rows="10" cols="75">%(value)s</textarea>
    <br/>
    <input type="submit">
</form>
"""
trans_table = string.maketrans('abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ',
                               'nopqrstuvwxyzabcdefghijklmNOPQRSTUVWXYZABCDEFGHIJKLM')

form_hw2_p2="""
<form method="post">
    <h2>Create a new user account</h2>
    <label>
        Username:
        <input type="text" name="username" value="%(username)s">
        <span style="color: red;">%(user_error)s</span>
    </label>
    <br/>
    <label>
        Password:
        <input type="password" name="password">
        <span style="color: red;">%(password_error)s</span>
    </label>
    <br/>
    <label>
        Password (verify):
        <input type="password" name="verify">
        <span style="color: red;">%(verify_error)s</span>
    </label>
    <br/>
    <label>
        Email (optional):
        <input type="email" name="email" value="%(email)s">
        <span style="color: red;">%(email_error)s</span>
    </label>
    <br/>
    <input type="submit" value="Create User">
</form>
"""

class MainHandler(webapp2.RequestHandler):
    def get(self):
        self.response.out.write('Hello Udacity!')

class HW2P1(webapp2.RequestHandler):
    def get(self):
        self.response.out.write(form_hw2_p1 % {'value' : ''})

    def post(self):
        self.response.out.write(form_hw2_p1 % {'value' : rot13(self.request.get('text'))})

def rot13(text):
    if text:
        text = string.translate(text.encode('ascii', 'ignore'), trans_table)

    return cgi.escape(text, True)

class HW2P2(webapp2.RequestHandler):
    hw2_p2_map = {'username': '', 'email' : '',
              'user_error': '', 'password_error': '',
              'verify_error': '', 'email_error': ''}
    
    def get(self):
        self.response.out.write(form_hw2_p2 % self.hw2_p2_map)

    def post(self):
        error = self.validate(self.request)
        if error:
            self.response.out.write(form_hw2_p2 % self.hw2_p2_map)
        else:
            self.redirect('/2/2-redirect?username=%s' % self.hw2_p2_map['username'])

    def validate(self, request):
        username, password = request.get('username'), request.get('password')
        verify, email = request.get('verify'), request.get('email')
        self.hw2_p2_map['username'] = username
        self.hw2_p2_map['email'] = email
        
        self.validate_user(username)
        self.validate_pass(password, verify)
        self.validate_email(email)
        

        return (len(self.hw2_p2_map['user_error']) + len(self.hw2_p2_map['password_error']) +
                len(self.hw2_p2_map['verify_error']) + len(self.hw2_p2_map['email_error'])) > 0

    def validate_user(self, username):
        self.hw2_p2_map['user_error'] = 'Invalid username' if not re.search('^[a-zA-Z0-9_-]{3,20}$', username) else ''

    def validate_pass(self, password, verify):
        self.hw2_p2_map['password_error'] = 'Invalid password' if not re.search('^.{3,20}$', password) else ''
        self.hw2_p2_map['verify_error'] = 'First password does not match second' if password != verify else ''

    def validate_email(self, email):
        self.hw2_p2_map['email_error'] = 'Invalid email' if email and not re.search('^[\S]+@[\S]+\.[\S]+$', email) else ''

class HW2P2Redirect(webapp2.RequestHandler):
    def get(self):
        self.response.out.write('<h1>User created: %s</h1>' % self.request.get('username'))

app = webapp2.WSGIApplication([('/', MainHandler),
                               ('/2/1', HW2P1),
                               ('/2/2', HW2P2),
                               ('/2/2-redirect', HW2P2Redirect)],
                              debug=True)

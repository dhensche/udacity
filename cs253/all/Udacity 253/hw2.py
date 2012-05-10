__author__ = 'dhensche'

import cgi
import re
import string
from util import Handler

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

class HW2P1(Handler):
    def get(self):
        self.write(form_hw2_p1 % {'value' : ''})

    def post(self):
        self.write(form_hw2_p1 % {'value' : rot13(self.request.get('text'))})

def rot13(text):
    if text:
        text = string.translate(text.encode('ascii', 'ignore'), trans_table)

    return cgi.escape(text, True)

class HW2P2(Handler):
    hw2_p2_map = {'username': '', 'email' : '',
                  'user_error': '', 'password_error': '',
                  'verify_error': '', 'email_error': ''}

    def get(self):
        self.write(form_hw2_p2 % self.hw2_p2_map)

    def post(self):
        error = self.validate(self.request)
        if error:
            self.write(form_hw2_p2 % self.hw2_p2_map)
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

class HW2P2Redirect(Handler):
    def get(self):
        self.write('<h1>User created: %s</h1>' % self.request.get('username'))

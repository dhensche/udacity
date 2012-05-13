__author__ = 'dhensche'

import random
import hashlib
import string

class Hash():
    @staticmethod
    def make_salt():
        return ''.join(random.choice(string.letters) for x in xrange(5))

    @staticmethod
    def password(name, password, salt=None):
        salt = Hash.make_salt() if salt is None else salt
        return '|'.join([hashlib.sha256(name + password + salt).hexdigest(), salt])

    @staticmethod
    def verify_password(name, password, hash):
        return hash == Hash.password(name, password, hash.split('|')[1])

    @staticmethod
    def hash_str(s):
        return hashlib.md5(s).hexdigest()

    @staticmethod
    def hash_cookie(value):
        return '|'.join([value, Hash.hash_str(value)])

    @staticmethod
    def dehash_cookie(hashed_value):
        return hashed_value.split('|')[0]
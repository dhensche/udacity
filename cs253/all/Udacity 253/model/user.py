__author__ = 'dhensche'

from google.appengine.ext import db
from util.hasher import Hash

class User(db.Model):
    name = db.StringProperty(required=True)
    password_hash = db.StringProperty(required=True)
    email = db.EmailProperty(required=False)

    @staticmethod
    def find_by_username_and_password(username, password):
        users = User.gql("where name = '%s'" % username)
        for user in users:
            if Hash.verify_password(user.name, password, user.password_hash):
                return user
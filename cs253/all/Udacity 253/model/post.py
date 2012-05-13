__author__ = 'dhensche'

from google.appengine.ext import db

class Post(db.Model):
    subject = db.StringProperty(required=True)
    content = db.TextProperty(required=True)
    created = db.DateTimeProperty(auto_now_add=True)

    @staticmethod
    def select_all():
        return db.GqlQuery('select * from Post order by created desc')
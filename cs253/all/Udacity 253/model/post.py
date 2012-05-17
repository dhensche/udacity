__author__ = 'dhensche'

from google.appengine.ext import db
from base_model import JsonModel

class Post(JsonModel):
    subject = db.StringProperty(required=True)
    content = db.TextProperty(required=True)
    created = db.DateTimeProperty(auto_now_add=True)

    @staticmethod
    def select_all():
        return db.GqlQuery('select * from Post order by created desc')

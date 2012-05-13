import logging
from model.user import User

__author__ = 'dhensche'

from util.handler import Handler

class Home(Handler):
    user = ''
    def render_index(self):
        self.render('index.html', user=self.user)
    def get(self):
        user_id = self.get_cookie('userid')
        logging.info(user_id)
        if user_id is not None:
            user = User.get(user_id)
            if user is not None:
                self.user=user.name

        self.render_index()
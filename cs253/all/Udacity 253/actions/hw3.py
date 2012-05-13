__author__ = 'dhensche'

from util.handler import Handler
from model.post import Post

class BlogHome(Handler):
    def get(self):
        self.render('blog/index.html', entries=Post.select_all())

class Blog(Handler):
    def render_form(self, content='', subject='', error=''):
        self.render('blog/form.html', content=content, subject=subject, error=error)

    def get(self, id):
        if id == 'newpost':
            self.render_form()
        elif str(id).isdigit():
            self.render('blog/post.html', post=Post.get_by_id([int(id)])[0])

    def post(self, id):
        subject = self.request.get('subject')
        content = self.request.get('content')

        if subject and content:
            post = Post(subject=subject, content=content)
            key = post.put()
            self.redirect('/blog/' + str(key.id()))
        else:
            self.render_form(content, subject, 'Both a subject and content must be present')
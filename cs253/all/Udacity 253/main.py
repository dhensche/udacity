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
from actions import hw2, hw3, hw4, home

from util.handler import Handler

class MainHandler(Handler):
    def get(self):
        self.write('Hello Udacity!')


app = webapp2.WSGIApplication([('/', MainHandler),
                               ('/2/1', hw2.HW2P1),
                               ('/2/2', hw2.HW2P2),
                               ('/2/2-redirect', hw2.HW2P2Redirect),
                               ('/blog', hw3.BlogHome),
                               ('/blog/(.*)', hw3.Blog),
                               ('/home', home.Home),
                               ('/login', hw4.Login),
                               ('/logout', hw4.Logout),
                               ('/signup', hw4.SignUp)],
                              debug=True)

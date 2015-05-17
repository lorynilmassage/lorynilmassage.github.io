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
import cgi
import datetime
import webapp2
import os

from google.appengine.ext import ndb
from google.appengine.api import users

import jinja2
import webapp2

JINJA_ENVIRONMENT = jinja2.Environment(
    loader=jinja2.FileSystemLoader(os.path.dirname(__file__)),
    extensions=['jinja2.ext.autoescape'],
    autoescape=True)

guestbook_key = ndb.Key('Guestbook', 'default_guestbook')

class Greeting(ndb.Model):
  author = ndb.UserProperty()
  content = ndb.TextProperty()
  date = ndb.DateTimeProperty(auto_now_add=True)


class MainPage(webapp2.RequestHandler):
  def get(self):
    template = JINJA_ENVIRONMENT.get_template('index.html')
    self.response.write(template.render({}))


class Guestbook(webapp2.RequestHandler):
  def post(self):
    greeting = Greeting(parent=guestbook_key)

    if users.get_current_user():
      greeting.author = users.get_current_user()

    greeting.content = self.request.get('content')
    greeting.put()
    self.redirect('/')


app = webapp2.WSGIApplication([
  ('/', MainPage),
  ('/sign', Guestbook)
], debug=True)

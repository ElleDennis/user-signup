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
import re
import cgi

page_header = """
<!DOCTYPE html>
<html>
<head>
    <title><h1>Signup<h1></title>
</head>
<body>
</body>
</html>
"""

form = """
<form method="post"><strong><h1>
    Signup
    </h1></strong>
    <br>
    <label>Username
        <input type="text" name="name" value="%(user_name)s">
    </label>
    <div style="color: red">%(errorName)s</div>
    <br>
    <label>Password
        <input type="password" name="password" value="">
    </label>
    <div style="color: red">%(errorPassword)s</div>
    <br>
    <label>Verify password
        <input type="password" name="passwordrepeat" value="">
    </label>
    <div style="color: red">%(errorPasswordrepeat)s</div>
    <br>
    <label>Email (option)
        <input type="text" name="email" value="%(user_email)s">
    </label>
        <div style="color: red">%(errorEmail)s</div>
    <br>
    <br>
    <input type="submit">
</form>
"""

USER_RE = re.compile(r"^[a-zA-Z0-9_-]{3,20}$")
def validFormatName(user_name):
    return user_name and USER_RE.match(user_name)

PASS_RE = re.compile(r"^.{3,20}$")
def validFormatPassword(user_password):
    return user_password and PASS_RE.match(user_password)

EMAIL_RE = re.compile(r'^[\S]+@[\S]+\.[\S]+$')
def validFormatEmail(user_email):
    return not user_email or EMAIL_RE.match(user_email)


class MainHandler(webapp2.RequestHandler):
    # creates form
    def write_form(self, errorName="", errorPassword="", errorPasswordrepeat="", errorEmail="", user_name="", user_email=""):
        self.response.write(form % {"errorName": errorName,
                                    "errorPassword": errorPassword,
                                    "errorPasswordrepeat": errorPasswordrepeat,
                                    "errorEmail": errorEmail,
                                    "user_name": cgi.escape(user_name),
                                    "user_email": cgi.escape(user_email)})

    def get(self):
        self.write_form()

    def post(self):

        user_name = self.request.get('name')
        user_password = self.request.get('password')
        user_passwordrepeat = self.request.get('passwordrepeat')
        user_email = self.request.get('email')

        has_error = False
        passing = {"user_name": user_name, "user_email": user_email}

        if not validFormatName(user_name):
            has_error = True
            passing["errorName"] = "Not a valid name."

        if not validFormatPassword(user_password):
            has_error = True
            passing["errorPassword"] = "Not a valid password."

        if user_password != user_passwordrepeat:
            has_error = True
            passing["errorPasswordrepeat"] = "These passwords don't match."

        if not validFormatEmail(user_email):
            has_error = True
            passing["errorEmail"] = "Not a valid email."

        if has_error:
            self.write_form(**passing)
        else:
            self.redirect('/welcome?username='+user_name)


class WelcomeHandler(webapp2.RequestHandler):
    def get(self):
        self.response.write("Welcome "+self.request.get("username") )

app = webapp2.WSGIApplication([
    ('/', MainHandler),
    ('/welcome', WelcomeHandler),
    ], debug=True)

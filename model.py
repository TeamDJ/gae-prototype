from google.appengine.ext import db

class Token(db.Model):
    token = db.StringProperty(multiline=True)
    date = db.DateTimeProperty(auto_now_add=True)
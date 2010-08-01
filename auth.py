from google.appengine.ext import webapp
from google.appengine.ext.webapp.util import run_wsgi_app
from google.appengine.api import users
import atom.url
import gdata.service
import gdata.alt.appengine
import settings
import urllib
from google.appengine.api import urlfetch
import cgi
from model import *

AUTH_SCOPE = 'http://maps.google.com/maps/feeds/'



class Fetcher(webapp.RequestHandler):

    def get(self):
        url = atom.url.parse_url(self.request.uri)
        
        if 'token' in url.params:
            token = url.params['token']
            result = urlfetch.fetch(url='https://www.google.com/accounts/AuthSubSessionToken',
                                                method=urlfetch.GET,
                                                headers={'Authorization':'AuthSub token=%s'%token}) 
            session_token = result.content.split('=')[1]
            self.response.out.write('token is  %s' % session_token)
            
            token = Token(key_name='thoughtsquare', token=session_token)
            token.put()
        
        else:
            next_url = atom.url.Url('http', settings.HOST_NAME, path='/auth2').to_string()
            authsub_url = "https://www.google.com/accounts/AuthSubRequest?next=%s&scope=%s&session=1&secure=0" % (next_url, AUTH_SCOPE)
            self.response.out.write('<a href=%s>click here</a>' % authsub_url)

def main():
    application = webapp.WSGIApplication([('/.*', Fetcher),], debug=True)
    run_wsgi_app(application)

if __name__ == '__main__':
    main()

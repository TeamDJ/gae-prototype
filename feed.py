from google.appengine.ext import webapp
from google.appengine.ext.webapp.util import run_wsgi_app
import settings
import urllib
from google.appengine.api import urlfetch
import cgi
from google.appengine.ext import db
from model import *
import xml.dom.minidom

FEED_URL = 'http://maps.google.com/maps/feeds/features/210912570095610105860/00048c2bba524da174c91/full'
ATOM_NS = 'http://www.w3.org/2005/Atom'
KML_NS = 'http://www.opengis.net/kml/2.2'

class Fetcher(webapp.RequestHandler):

    def get(self):
        token = Token.get_by_key_name('thoughtsquare')
        result = urlfetch.fetch(url=FEED_URL,
                                        method=urlfetch.GET,
                                        headers={'Authorization':'AuthSub token=%s'%token.token})
                
        dom = xml.dom.minidom.parseString(result.content)  
        
        entries = dom.getElementsByTagNameNS(ATOM_NS, 'entry')
        for entry in entries:
            self.response.out.write('title: ' + getText(entry, ATOM_NS, 'title') + '<br/>')
            self.response.out.write('updated: ' + getText(entry, ATOM_NS, 'updated') + '<br/>')
            self.response.out.write('coordinates: ' + getText(entry, KML_NS, 'coordinates') + '<br/><br/>')
            
              
        self.response.out.write("<pre>" + cgi.escape(dom.toprettyxml()) + "</pre>" )
        
    
def getText(parent, namespace, elementName):
    
    nodelist = parent.getElementsByTagNameNS(namespace,elementName)[0].childNodes
    
    rc = []
    for node in nodelist:
        if node.nodeType == node.TEXT_NODE:
            rc.append(node.data)
    return ''.join(rc)
def main():
    application = webapp.WSGIApplication([('/.*', Fetcher),], debug=True)
    run_wsgi_app(application)

if __name__ == '__main__':
    main()

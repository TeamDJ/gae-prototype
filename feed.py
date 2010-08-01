from google.appengine.ext import webapp
from google.appengine.ext.webapp.util import run_wsgi_app
import settings
import urllib
from google.appengine.api import urlfetch
import cgi
from google.appengine.ext import db
from model import *
import xml.dom.minidom
import json

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
        
        locations = []
        for entry in entries:
            locations.append(getLocationJSON(entry))
            
        self.response.out.write(json.dumps(locations))
 
def getLocationJSON(entry):
    obj = {}
    obj["title"] = getText(entry, ATOM_NS, 'title')
    obj["updated_at"] = getText(entry, ATOM_NS, 'updated') 
    obj["coordinates"] = getText(entry, KML_NS, 'coordinates').split(',')
    return obj
    
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

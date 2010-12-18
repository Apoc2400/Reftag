import re
from google.appengine.api import memcache
import urllib2
import sys
#import htmllib        # Deprecated since version 2.6: removed in Python 3.0.
from BeautifulSoup import BeautifulSoup, SoupStrainer # For processing HTML



def unescape(s):
    p = htmllib.HTMLParser(None)
    p.save_bgn()
    p.feed(s)
    return p.save_end()

def urlTitleFetch(url):
    key = 'urltitle/' + url
    data = memcache.get(key)
    if data is not None:
        #print >> sys.stderr, "Title from memcache: " + url
        return data
    else:
        #print >> sys.stderr, "Title from fetch: " + url
        htmldata = ''
        try:
            u = urllib2.urlopen(url)
            htmldata = u.read()
            u.close()
        except urllib2.URLError, e:
            #print >> sys.stderr, 'URLError'
            #raise
            return ''
        except:
            return ''
        
        if htmldata == '' or not re.search('<html', htmldata, re.I):
            #error('Bad html data')
            return ''
            
        #Strip everything from <body and on, we only need the head
        htmldata = re.split('(?i)<body', htmldata, maxsplit=1)[0]
        
        parseOnly = SoupStrainer('title')
        soup = BeautifulSoup(htmldata, parseOnlyThese=parseOnly, convertEntities=BeautifulSoup.HTML_ENTITIES)
        #print >> sys.stderr, soup
        if soup.title and soup.title.string:
            title = soup.title.string.extract()    # extract() makes it an ordinary string
        else:
            return ''
#        title = ''
#        m = re.search('<title>(.*?)<\/title>', htmldata, re.I | re.DOTALL)
#        if m:
#            title = m.group(1)
#            print >> sys.stderr, 'title:' + title
#            #title = re.sub('^[\s\n]+|[\s\n]+$', '', title)
#            title = title.strip()
#            title = unescape(title)
#            print >> sys.stderr, 'aftertitle:' + title
#        else:
#            print >> sys.stderr, 'none'
#            pass
        
        memcache.add(key, title, 3600)
        return title

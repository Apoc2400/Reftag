from google.appengine.api import memcache
from google.appengine.api.urlfetch import DownloadError 
import urllib2
#import os

#import sys

def cachedFetch(url, expiretime=3600, maxlength=100000):    # fetch url, with memcache
    # Enable this to effectively clear memcache on new version deployment
    #key = os.environ['CURRENT_VERSION_ID'] + '/' + url
    key = url
    data = memcache.get(key)
    if data is not None:
        #print >> sys.stderr, "From memcache: " + url 
        return data
    else:
        #print >> sys.stderr, "From fetch: " + url
        try:
            result = urllib2.urlopen(url)
            data = result.read(maxlength)
            result.close()
            memcache.add(key, data, expiretime)
            return data
        except urllib2.URLError, e:
            return ''
        except DownloadError:
            return ''

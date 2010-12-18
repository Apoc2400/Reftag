from cachedfetch import cachedFetch
from django.utils import simplejson as json
import urllib
import sys

def getRedirectTarget(title):
    querystring = urllib.urlencode({'action': 'query',
                                    'format': 'json',
                                    'redirects': '1',
                                    'titles':title})
    url = "http://en.wikipedia.org/w/api.php?" + querystring
    #url = "http://en.wikipedia.org/w/api.php?action=query&prop=info&titles=appspot.com&redirects&format=json"
    #print >> sys.stderr, "url: " + url 
    jsonstring = cachedFetch(url, 3600)
    #print >> sys.stderr, jsonstring
    apidata = json.loads(jsonstring)
    try:
        return apidata['query']['redirects'][0]['to']
    except KeyError, e:
        return ''

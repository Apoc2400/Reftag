from cachedfetch import cachedFetch
import urllib
from django.utils import simplejson as json
import re
import sys
from keys import nyt_apikey


def nytimesFetchInfo(url):
    #print >> sys.stderr, 'url: ' + url
    #http://api.nytimes.com/svc/search/v1/article?format=json&query=url%3Ahttp%3A%2F%2Fwww.nytimes.com%2F2009%2F03%2F26%2Fgarden%2F26slow.html&fields=title%2C+nytd_title%2C+date%2C+byline%2C+page_facet%2C+section_page_facet%2C+source_facet&api-key=#### 
    urlfixed = re.sub('\?.*$', '', url)
    #print >> sys.stderr, urlfixed
    querystring = urllib.urlencode({'format': 'json',
                                    'query': 'url:'+urlfixed,
                                    'fields': 'title, date, byline, page_facet, section_page_facet, source_facet, column_facet',
                                    'api-key': nyt_apikey})
    nyturl = "http://api.nytimes.com/svc/search/v1/article?" + querystring
    jsonstring = cachedFetch(nyturl, 3600)
    if jsonstring == '':
        error('Bad data from NYTimes')
    
    nytdata = json.loads(jsonstring)
    #print >> sys.stderr, nytdata
    if len(nytdata['results']) == 0:
        #error('No results')
        return {}
    
    result = nytdata['results'][0]
    citedata = {'work': 'The New York Times'}
    citedata['title'] = result['title']
    if result.has_key('page_facet'):
        citedata['page'] = result['page_facet']
    if result.has_key('date'):
        m = re.search('(\d\d\d\d)(\d\d)(\d\d)', result['date'])
        if m:
            citedata['date'] = m.group(1) + '-' + m.group(2) + '-' + m.group(3)
    if result.has_key('byline'):
        byline = result['byline']
        byline = re.sub('(?i)^By\s+', '', byline)
        byline = re.sub('(?i) And ', ', ', byline)
        byline = byline.title()
        authors = re.split('\s*,\s*', byline)
        citedata['authors'] = authors

    
    return citedata

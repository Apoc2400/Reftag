

from google.appengine.ext import webapp
from google.appengine.api import users

import gdata.service
import gdata.alt.appengine
import os
from google.appengine.api import memcache
from doifetch import doiFetchInfo
from urltitlefetch import urlTitleFetch
from nytimesfetch import nytimesFetchInfo

from cachedfetch import cachedFetch
from django.utils import simplejson as json
from RedirectTarget import getRedirectTarget
from DomainParser import domainFromURL



print 'Content-Type: text/html; charset=utf-8'
print ''
print """<!DOCTYPE html><html><head>
         <title>Wikipedia citation tool for Google Books</title>
     <body>testapa"""

print '<br>CURRENT_VERSION_ID: ', os.environ['CURRENT_VERSION_ID']

print '<br>memcache stats: ', memcache.get_stats()

url = "http://news.bbc.co.uk/2/hi/middle_east/8561998.stm"
domain = domainFromURL(url)
print '<br /> domain:'
print domain
print '<br /> Redir:'
print getRedirectTarget(domain)

print "</body></html>"



import cgi
import cgitb; cgitb.enable()
import urllib
#import urllib2        # Now called inside cachedFetch
from cachedfetch import cachedFetch
import re
from django.utils import simplejson as json

def error(message):
    print 'Content-Type: text/plain'
    print ''
    print message
    exit()

def main():
    form = cgi.FieldStorage()
    if (not form.has_key("isbn")):
      error('No isbn!')
    isbn = form["isbn"].value
    isbn = re.sub('[^0-9]', '', isbn)

    if (not form.has_key("callback")):
      error('No callback.')
    callback = form["callback"].value


    url = "http://diberri.dyndns.org/cgi-bin/templatefiller/index.cgi?type=isbn&vertical=1&dont_use_etal=1&format=xml&id=" + isbn

    xmldata = cachedFetch(url, 3600)
    if xmldata == '':
        error('Bad data from Diberri tool')

    #error(xmldata)
    bookdata = {}

    for line in xmldata.splitlines():
        m = re.search('^\|title=(.+)$', line, re.I)
        if m:
            bookdata['title'] = m.group(1)
        m = re.search('\|publisher=(.+)$', line, re.I)
        if m:
            bookdata['publisher'] = m.group(1)
        m = re.search('\|location=(.+)$', line, re.I)
        if m:
            bookdata['location'] = m.group(1)
        m = re.search('\|year=(.+)$', line, re.I)
        if m:
            bookdata['year'] = m.group(1)
        m = re.search('\|isbn=(.+)$', line, re.I)
        if m:
            bookdata['isbn'] = m.group(1)
        m = re.search('\|author=(.+)$', line, re.I)
        if m:
            bookdata['authors'] = m.group(1)

    
    jsonstr = json.dumps(bookdata, sort_keys=True, indent=4, ensure_ascii=False)
    jsonp = callback + '(' + jsonstr + ');'

    print 'Content-Type: text/javascript'
    print ''
    print jsonp
  

if __name__ == "__main__":
    main()
    

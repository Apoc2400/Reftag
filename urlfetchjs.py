from nytimesfetch import nytimesFetchInfo
import cgi
from django.utils import simplejson as json
import re
from urltitlefetch import urlTitleFetch
import sys
from RedirectTarget import getRedirectTarget
from DomainParser import domainFromURL

def error(message):
    print 'Content-Type: text/plain'
    print ''
    print 'Error: ', message

 
def main():
    form = cgi.FieldStorage()
    if (not form.has_key("url")):
        error('No URL.'); return
    url = form["url"].value

    if (not form.has_key("callback")):
        error('No callback.'); return
    callback = form["callback"].value
 
    if re.search('^http:\/\/[^\/]*nytimes\.com\/', url, re.I):
        citedata = nytimesFetchInfo(url)
    else:
        title = urlTitleFetch(url)
        citedata = {'title': title}
        try:
            #print >> sys.stderr, 'url:' + url
            domain = domainFromURL(url)
            #print >> sys.stderr, 'domain:' + domain
            workArticleTitle = getRedirectTarget(domain)
            if workArticleTitle:
                m = re.search('^(.+)\s*\(.*\)', workArticleTitle)
                if m:
                    work = '[[' + workArticleTitle + '|' + m.group(1).strip() + ']]'
                else:
                    work = '[[' + workArticleTitle + ']]'
                citedata['work'] = work
        except:
            pass
    
    jsonstr = json.dumps(citedata, sort_keys=True, indent=4, ensure_ascii=True)
    jsonp = callback + '(' + jsonstr + ');'
    
    print 'Content-Type: text/javascript'
    print ''
    print jsonp.encode('utf8')

 
 
if __name__ == "__main__":
    main()
    

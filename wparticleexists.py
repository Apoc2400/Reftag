import cgi
import cgitb; cgitb.enable()
import urllib
#import urllib2        # Now called inside cachedFetch
import re
from cachedfetch import cachedFetch

def main():
    form = cgi.FieldStorage()
    if (not form.has_key("title")):
      print 'Content-Type: text/plain'
      print ''
      print 'No title specified!'
      exit()

    title = form["title"].value

    querystring = urllib.urlencode([('titles', title)])
    url = "http://en.wikipedia.org/w/api.php?action=query&format=yaml&prop=info&" + querystring
    
    data = cachedFetch(url, 3600)
    if not data == '':
      if re.search('^\s*pageid: \d+', data, re.MULTILINE):
        print 'Content-Type: text/plain'
        print ''
        print '1'
      elif re.search('^\s*missing:', data, re.MULTILINE):
        print 'Content-Type: text/plain'
        print ''
        print '0'
      else:
        print 'Content-Type: text/plain'
        print ''
        print 'Data error!'
        exit()
    else:
      print 'Content-Type: text/html'
      print ''
      print 'Fail!'

if __name__ == "__main__":
    main()


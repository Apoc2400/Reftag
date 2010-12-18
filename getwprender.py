import cgi
import cgitb; cgitb.enable()
import urllib
#import urllib2        # Now called inside cachedFetch
from cachedfetch import cachedFetch

def main():
    form = cgi.FieldStorage()
    if (not form.has_key("wikitext")):
      print 'Content-Type: text/plain'
      print ''
      print 'No wikitext!'
      exit()

    wikitext = form["wikitext"].value

    querystring = urllib.urlencode([('text', wikitext)])
    url = "http://en.wikipedia.org/w/api.php?action=parse&format=xml&prop=text&" + querystring

    xmldata = cachedFetch(url, 3600)
    if not xmldata == '':
      #xmldata = re.sub('Chicagogsdgsdgsdgsfgsrg', 'ugg' , xmldata)
      print 'Content-Type: text/xml; charset=utf-8'
      print ''
      print xmldata
    else:
      print 'Content-Type: text/html'
      print ''
      print 'Fail!'
      

if __name__ == "__main__":
    main()
    

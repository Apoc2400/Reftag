from nytimesfetch import nytimesFetchInfo
import cgi
import re
import time
import sys


def printFooter():
    print """<hr>
    <small>Made by <a href="http://en.wikipedia.org/wiki/User:Apoc2400">Apoc2400</a>. Send feedback to apoc2400 (at) gmail.com or <a href="http://en.wikipedia.org/wiki/User_talk:Apoc2400">my talk page</a>.</small>
    """
    print "</body></html>"

def error(message):
    sys.stderr.write(message + "\n")
    print '<span id="citespan"><hr><font color="red">', cgi.escape(message, 1), "</font></span>"
    printFooter()

def main():
    print 'Content-Type: text/html; charset=utf-8'
    print ''
    print """<!DOCTYPE html><html><head>
             <title>New York Times Wikipedia reference generator</title>

        <link rel="shortcut icon" href="/favicon.ico" />

        </head><body style="font-family: sans-serif; font-size:0.79375em">
        <h1><a href="/nytweb.py" style="text-decoration: none; color: black">{<font color="red">T</font>} New York Times Wikipedia reference generator</a></h1>
        """


    form = cgi.FieldStorage()
    url = ''
    if form.has_key("url"):
        url = form["url"].value

    print """<hr><form action="" method="get">
        <label for="url">URL:</label>
        <input type="text" size="80" name="url" id="url" tabindex=1 value="%s">
        <input type="submit" value="Load" tabindex=1>
        </form>""" % (cgi.escape(url, 1))

    if not form.has_key("url"):
        print """<hr><font color="DarkOliveGreen">Example URL (copy and paste above):</font> http://www.nytimes.com/2007/12/25/world/africa/25kenya.html
        <p>Try also: <a href="/">Wikipedia citation tool for Google Books</a> or <a href="/doiweb.py">DOI</a></p>"""
        printFooter()
        return

    url = url.strip()    #Trim whitespace
    url = re.sub('\?.*$', '', url)    #Remove from the question mark
    if not re.search('^http:\/\/[^\/]*nytimes\.com\/', url, re.I):
        error('Not a New York Times URL.')
        return
    citedata = nytimesFetchInfo(url)
    if not citedata:
        sys.stderr.write("\ncitedata=" + repr(citedata) + "\n")
        error('No information returned by NYTimes API.')
        return
    
    cite = ''
    refname = ''
    
    if citedata.has_key('authors'):
        authori = 0
        for author in citedata['authors']:
            authori += 1
            if len(citedata['authors']) > 1:
                authoristr = str(authori)
            else:
                authoristr = ''
            match = re.search('(.+)\s+(.+)', author)
            if match:
                first = match.group(1)
                last = match.group(2)
                cite += '|last' + authoristr + '=' + last
                cite += '|first' + authoristr + '=' + first
                if authori <= 2:
                    refname += last
            else:
                cite += '|author' + authoristr + '=' + author
                if authori <= 2:
                    refname += last
                
    for field in ['title', 'work', 'page']:
        if citedata.has_key(field):
            cite += '|' + field + '=' + citedata[field]
    if refname and citedata.has_key('date'):
        d = time.strptime(citedata['date'],"%Y-%m-%d")
        datestr = time.strftime("%-d %B %Y",d)
        #match = re.search('(\d\d\d\d)-(\d\d)-(\d\d)', citedata['date'])
        #if match:
        #    year = int(match.group(1))
        #    month = int(match.group(2))
        #    day = int(match.group(3))    
        cite += '|date=' + datestr
    
    cite += '|url=' + url
    
    fullcite = "<ref"
    if refname:
        fullcite += ' name="' + refname + '"'
    fullcite += '>'
    fullcite += '{{cite news'
    fullcite += cite
    fullcite += '}}</ref>'
    
    fullcite_enc = cgi.escape(fullcite, 1).encode('utf-8')
    
    print """<hr><font color="DarkOliveGreen">Below is the complete reference tag. Copy and paste it into the Wikipedia article.</font><br />
    <textarea rows="5" cols="100" style="width: 99%" id="fullcite" tabindex=1>"""
    print fullcite_enc
    print '</textarea>'

    printFooter()



if __name__ == "__main__":
    main()

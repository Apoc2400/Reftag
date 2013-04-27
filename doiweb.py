from doifetch import doiFetchInfo
import cgi


def printFooter():
    print """<hr>
    <small>Made by <a href="http://en.wikipedia.org/wiki/User:Apoc2400">Apoc2400</a>. Send feedback to apoc2400 (at) gmail.com or <a href="http://en.wikipedia.org/wiki/User_talk:Apoc2400">my talk page</a>.</small>
    """
    print "</body></html>"

def error(message):
    print '<span id="citespan"><hr><font color="red">', cgi.escape(message, 1), "</font></span>"
    printFooter()
    exit()

def main():
    print 'Content-Type: text/html; charset=utf-8'
    print ''
    print """<!DOCTYPE html><html><head>
             <title>DOI Wikipedia reference generator</title>

        <link rel="shortcut icon" href="/favicon.ico" />

        </head><body style="font-family: sans-serif; font-size:0.79375em">
        <h1><a href="/doiweb.py" style="text-decoration: none; color: black">{<font color="red">T</font>} DOI Wikipedia reference generator</a></h1>
        """


    form = cgi.FieldStorage()
    doi = ''
    if form.has_key("doi"):
        doi = form["doi"].value

    print """<hr><form action="" method="get">
        <label for="doi">DOI:</label>
        <input type="text" size="80" name="doi" id="doi" tabindex=1 value="%s">
        <input type="submit" value="Load" tabindex=1>
        </form>""" % (cgi.escape(doi, 1))

    if not form.has_key("doi"):
        print """<hr><font color="DarkOliveGreen">Example DOI (copy and paste above):</font> 10.1111/j.1600-0404.1986.tb04634.x
        <p>Try also: <a href="/">Wikipedia citation tool for Google Books</a> or <a href="/nytweb.py">The New York Times</a></p>"""
        printFooter()
        return

    doi = doi.strip()    #Trim whitespace
    citedata = doiFetchInfo(doi)
    cite = ''
    refname = ''
    
    if citedata.has_key('authors'):
        authori = 0
        for author in citedata['authors']:
            authori += 1
            if author.has_key('last'):
                cite += '|last' + str(authori) + '=' + author['last']
                if authori <= 2:
                    refname += author['last']
            if author.has_key('first'):
                cite += '|first' + str(authori) + '=' + author['first']
    for field in ['title', 'journal', 'volume', 'issue', 'year', 'pages', 'issn', 'doi']:
        if citedata.has_key(field):
            cite += '|' + field + '=' + citedata[field]
    if refname and citedata.has_key('year'):
        refname += citedata['year']
    
    fullcite = "<ref"
    if refname:
        fullcite += ' name="' + refname + '"'
    fullcite += '>'
    fullcite += '{{cite journal'
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

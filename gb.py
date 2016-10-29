#
#
#

#__author__ = 'Apoc2400'

import wsgiref.handlers
from google.appengine.api import users
import atom.url
import gdata.service
import gdata.alt.appengine
import gdata.books
import gdata.books.service
from isbn_hyphenate.isbn_hyphenate import try_hyphenate, IsbnError

import cgi
import cgitb; cgitb.enable()
import re
import urllib
import sys
import worldcat_api


def printFooter():
    print """<hr>
    <small>Made by <a href="http://en.wikipedia.org/wiki/User:Apoc2400">Apoc2400</a>. Send feedback to apoc2400 (at) gmail.com or <a href="http://en.wikipedia.org/wiki/User_talk:Apoc2400">my talk page</a>. Using some html and js from <a href="http://en.wikipedia.org/wiki/User:Mr.Z-man/refToolbar">refToolbar</a> by Mr.Z-man. <a href="http://www.marklets.com/Bookmarklets/RefTag.aspx">Bookmarklet</a> for direct access from Google Books. <a href="https://github.com/Apoc2400/Reftag">Source code</a> in Python.</small>
    """
    print "</body></html>"

def error(message):
    print '<span id="citespan"><hr><font color="red"> Error:', cgi.escape(message, 1), "</font></span>"
    printFooter()


def getBookData(urlOrNum):
    if urlOrNum.isdigit():
        oclc = urlOrNum
        thisdict = worldcat_api.get_by_oclc(oclc)
        if thisdict is None:
            error('The OCLC number entered was not found.')
        return thisdict


    book_url = urlOrNum
    #print "url:", book_url, "<br />"
    if not re.search('books.google.', book_url, re.I) and not re.search('\?id=', book_url, re.I):
        error('Not a Google Books URL.')
        return
    urlsep = re.search('\?([^#]*)', book_url)
    if not urlsep:
        error('Bad URL.')
        return

    book_url_qs = urlsep.group(1)
    #print "url_qs:", book_url_qs, "<br />"

    book_url_qs_fields = cgi.parse_qs(book_url_qs)
    #print "book_url_qs_fields:", book_url_qs_fields, "<br />"

    if "id" not in book_url_qs_fields:
        error('Bad URL. It has to be for a specific book, not a search result page')
        return
    book_id = book_url_qs_fields["id"][0]
    #print "book_id:", book_id, "<br />"
    page = ''
    page_string = ''
    if 'pg' in book_url_qs_fields:
        page_string = book_url_qs_fields['pg'][0]
        match = re.search('\D*(\d+)', page_string)
        if match:
            page = match.group(1) + u"\u2013".encode("utf-8")


    new_url = 'https://books.google.com/books?id=' + urllib.quote_plus(book_id)
    if page_string:
        new_url += '&pg=' + urllib.quote_plus(page_string)

    client = gdata.books.service.BookService()
    gdata.alt.appengine.run_on_appengine(client)


    try:
        thisbook = client.get_by_google_id(book_id)    # '8cp-Z_G42g4C'
        thisdict = thisbook.to_dict()
        thisdict['page'] = page
        thisdict['new_url'] = new_url
        return thisdict
    except Exception, err:
        print >> sys.stderr, 'ERROR: %s\n' % str(err)
        error('No information available for this URL.')
        return

def main():
    print 'Content-Type: text/html; charset=utf-8'
    print ''
    print """<!DOCTYPE html><html><head>
             <title>Wikipedia citation tool for Google Books</title>
         <script src="static/gb.js" type="text/javascript"></script>

        <link rel="stylesheet" href="http://en.wikipedia.org/w/index.php?title=MediaWiki:Common.css&amp;usemsgcache=yes&amp;ctype=text%2Fcss&amp;smaxage=2678400&amp;action=raw&amp;maxage=2678400" type="text/css" media="all" />
        <link rel="stylesheet" href="http://en.wikipedia.org/w/index.php?title=MediaWiki:Print.css&amp;usemsgcache=yes&amp;ctype=text%2Fcss&amp;smaxage=2678400&amp;action=raw&amp;maxage=2678400" type="text/css" media="print" />
        <link rel="stylesheet" href="http://en.wikipedia.org/w/index.php?title=MediaWiki:Handheld.css&amp;usemsgcache=yes&amp;ctype=text%2Fcss&amp;smaxage=2678400&amp;action=raw&amp;maxage=2678400" type="text/css" media="handheld" />
        <link rel="stylesheet" href="http://en.wikipedia.org/w/index.php?title=MediaWiki:Monobook.css&amp;usemsgcache=yes&amp;ctype=text%2Fcss&amp;smaxage=2678400&amp;action=raw&amp;maxage=2678400" type="text/css" media="all" />
        <link rel="stylesheet" href="http://en.wikipedia.org/w/index.php?title=-&amp;action=raw&amp;maxage=2678400&amp;smaxage=0&amp;ts=20100117020437&amp;gen=css" type="text/css" media="all" />

        <link rel="stylesheet" href="http://bits.wikimedia.org/skins-1.5/common/shared.css?257z2" type="text/css" media="screen" />
        <link rel="stylesheet" href="http://bits.wikimedia.org/skins-1.5/common/commonPrint.css?257z2" type="text/css" media="print" />

        <!--<link rel="stylesheet" href="http://bits.wikimedia.org/skins-1.5/monobook/main.css?257z2" type="text/css" media="screen" />-->
        <link rel="shortcut icon" href="/favicon.ico" />

             </head><body onload="loadRun();" style="font-family: sans-serif; font-size:0.79375em">"""


    book_url = ''
    form = cgi.FieldStorage()
    if "book_url" in form:
        book_url = form["book_url"].value


    print  """<h1><a href="/" style="text-decoration: none; color: black">{<font color="red">T</font>} Wikipedia citation tool for Google Books</a></h1>
              <font color="DarkOliveGreen">1: Find a book you want to cite on <a href="http://books.google.com/" target="_blank">Google Books</a>. 
          Copy the URL of the book from the address bar, and paste it below. Then press "Load". <a href="http://books.google.com/books?id=aqmAc2fFsAUC&pg=PA90" target="_blank">Example book</a>.</font>
          <form action="" method="get">
              <label id="book_url_label" for="book_url">Google Books URL:</label>
              <input type="text" size="80" name="book_url" id="book_url" tabindex=1 
                  value="%s"></input>
              <input type="submit" value="Load" tabindex=1></input> &nbsp; &nbsp; <input type="button" tabindex=1 value="Clear" onClick="formClear();"> <!--Hej du!-->
              </form>""" % (cgi.escape(book_url, 1))

    if "book_url" not in form:
        print """<hr><font color="DarkOliveGreen">Example book (copy and paste above):</font> http://books.google.com/books?id=aqmAc2fFsAUC&pg=PA90
            <p>Try also: <a href="doiweb.py">Wikipedia citation tool for DOI</a> or <a href="/nytweb.py">The New York Times</a>.<br />
            Also available from a user script: <a href="http://en.wikipedia.org/wiki/Wikipedia:RefToolbarPlus">refToolPlus</a>.</p>"""
        printFooter()
        return

    thisdict = getBookData(book_url)
    if thisdict is None:
        return
    #sys.stderr.write('thisdict = ' + repr(thisdict) + '\n')
    page = thisdict.get('page', '')
    new_url = thisdict.get('new_url', '')
        
    #thisdict = {'embeddability': 'embeddable', 'info': 'http://books.google.com/books?id=9PE2T2a5fDYC&ie=ISO-8859-1&source=gbs_gdata', 'description': 'Ramon Sarr\xc3\xb3 explores an iconoclastic religious movement initiated by a Muslim preacher during the French colonial period. Employing an ethnographic approach that respects the testimony of those who suffered violence as opposed to those who wanted to "get rid of custom," this work discusses the extent to which iconoclasm produces a rupture of religious knowledge and identity and analyzes its relevance in the making of modern nations and citizens. The Politics of Religious Change on the Upper Guinea Coastexamines the historical complexity of the interface between Islam, traditional religions, and Christianity in West Africa, and how this interface connects to dramatic political change. The book unveils a rare history and brokers a dialogue between a long tradition of anthropology and contemporary anthropological debates. A wide range of readers, particularly those with an interest in the anthropology of religion, iconoclasm, the history and anthropology of West Africa, or the politics of heritage, will gravitate toward this work.', 'format': 'book', 'publishers': ['Edinburgh University Press'], 'identifiers': [('google_id', '9PE2T2a5fDYC'), ('ISBN', '0748635157'), ('ISBN', '9780748635153')], 'thumbnail': 'http://bks9.books.google.com/books?id=9PE2T2a5fDYC&printsec=frontcover&img=1&zoom=5&edge=curl&sig=ACfU3U0LyllDnVUHiadMIrdIuvVAiURtuQ&source=gbs_gdata', 'subjects': ['Iconoclasm', 'Guinea', 'Iconoclasm/ Guinea', 'Religion and politics', 'History / Europe / General', 'Social Science / Human Geography', 'Social Science / Ethnic Studies / General', 'Social Science / Customs & Traditions', 'Religion / Ethnic & Tribal', 'Religion / General', 'History / Africa / General', 'Religion / Comparative Religion', 'History / General', 'History / Africa / General', 'Religion / Ethnic & Tribal', 'Religion / Islam / General', 'Religion / Religion, Politics & State', 'Social Science / Human Geography', 'Social Science / Islamic Studies', 'Travel / Africa / General'], 'authors': ['Ramon Sarr\xc3\xb3', 'John Smith', 'Jane Smith', 'Olaus Petrus', 'Mick Paff'], 'date': '2009-05-03', 'title': 'The Politics of Religious Change on the Upper Guinea Coast: Iconoclasm Done and Undone', 'viewability': 'view_partial', 'annotation': 'http://www.google.com/books/feeds/users/me/volumes'}

    #print 'Got dict: ' + str(thisdict)+  '<br />'

    #print thisdict['title'], "<br />"
    title = thisdict.get('title', '')
    date = thisdict.get('date', '')
    publisher = ', '.join(thisdict.get('publishers', []))
    authors = thisdict.get('authors', '')

    isbn = ''
    issn = ''
    iccn = ''
    oclc = ''
    other_id_list = []
    otherfields = []
    if 'identifiers' in thisdict:
        unique_identifiers = dict(thisdict['identifiers'])
        for idpair in unique_identifiers.iteritems():
            if idpair[0].lower() == 'google_id':
                pass
            elif idpair[0].lower() == 'isbn':
                if len(idpair[1]) >= len(isbn): isbn = idpair[1]    # Only keep the longest ISBN
            elif idpair[0].lower() == 'issn':
                issn = idpair[1]
                other_id_list.append('{{ISSN|' + issn + '}}')
            elif idpair[0].lower() == 'lccn':
                lccn = idpair[1]
                other_id_list.append('{{LCCN|' + lccn + '}}')
            elif idpair[0].lower() == 'oclc':
                oclc = idpair[1]
                otherfields.append('oclc=' + oclc)
            elif idpair[0].lower() == 'doi':
                otherfields.append('doi=' + idpair[1])
            else:
                other_id_list.append(idpair[0] + ':' + idpair[1])

    if isbn:
        try:
            isbn = try_hyphenate(isbn)
        except IsbnError:
            pass    #Keep the currect value of isbn

    other_id = ', '.join(other_id_list)
    if len(other_id):
        otherfields.append('id=' + other_id)

    #width 1040
    print """<span id="citespan"><hr>
    <!--<fieldset><legend>Cite book source</legend>-->
    <font color="DarkOliveGreen">2: The fields below have been filled in automatically. Correct any mistakes and add the information you have. All fields are optional, but "Page number(s)" is very useful.</font>
    <table cellspacing="5">

    <tr><td><label for="title">Title: </label></td>
    <td colspan=7><input type="text" tabindex=1 style="width:100%%" id="title" value="%s"></td></tr>
    """% (cgi.escape(title, 1))


    for i in range(1, 3+1):
        this_author = authors[i-1] if len(authors)>=i else ''
        this_author_escaped = cgi.escape(this_author, 1)
        print """
        <tr><td width="70"><label for="author%i">Author%s: </label></td>
        <td width="150"><input type="text" tabindex=1 style="width:100%%" id="author%i" value="%s">
        <input type="hidden" id="authorOrig%i" value="%s"></td>
        <td width="70"><label for="last%i">&nbsp;<a href="javascript:splitName(%i);" tabindex=1>or</a>&nbsp;last&nbsp;name: </label></td>
        <td width="150"><input type="text" tabindex=1 style="width:100%%" id="last%i"></td>
        <td width="70"><label for="first%i">,&nbsp;first&nbsp;name: </label></td>
        <td width="150"><input type="text" tabindex=1 style="width:100%%" id="first%i"></td>
        <td width="70"><label for="authorlink%i">&nbsp;Authorlink: </label></td>
        <td width="150"><input type="text" tabindex=1 style="width:70%%" id="authorlink%i">
        <a id="authorLinkAnchor%i"><img id="authorLinkButton%i" src="static/progress.gif" border="0" style="visibility: hidden" /></a>
        <a href="http://en.wikipedia.org/wiki/%s" target="_blank"><img id="authorTryLink%i" src="static/external.png" border="0" style="visibility: hidden" /></a>
        </td></tr>
        """ % (i , '' if i==1 else ' '+`i` , i, this_author_escaped, i, this_author_escaped, i, i, i, i, i, i, i, i, i, this_author_escaped, i)

    coauthors = ', '.join(authors[3:])


    #    <tr><td width="120"><label for="last">&nbsp;Last name: </label></td>
    #    <td width="400" colspan=3><input type="text" tabindex=1 style="width:100%%" id="last" value="%s"></td>
    #    <td width="120"><label for="first">&nbsp;First name: </label></td>
    #    <td width="400" colspan=3><input type="text" tabindex=1 style="width:100%%" id="first"></td></tr>
    print """
    <tr><td><label for="coauthors">Coauthors: </label></td>
    <td colspan=3><input type="text" tabindex=1 style="width:100%%" id="coauthors" value="%s"></td>
    <td><label for="editor">&nbsp;Editor: </label></td>
    <td><input type="text" tabindex=1 style="width:100%%" id="editor"></td>
    <td><label for="others">&nbsp;Others: </label></td>
    <td><input type="text" tabindex=1 style="width:100%%" id="others"></td></tr>

    <tr><td><label for="publisher">Publisher: </label></td>
    <td colspan=3><input type="text" tabindex=1 style="width:100%%" id="publisher" value="%s"></td>
    <td><label for="location">&nbsp;Location: </label></td>
    <td colspan=3><input type="text" tabindex=1 style="width:100%%" id="location"></td></tr>

    <tr><td><label for="date">Publication&nbsp;date or&nbsp;year: </label></td>
    <td colspan=3><input type="text" tabindex=1 style="width:140px" id="date" value="%s"> format: 
    <input id="dmy" name="dateformat" value="dmy" type="radio" checked="1" tabindex=1 onclick="reformatDates()"><label for="dmy">dmy</label>
    <input id="mdy" name="dateformat" value="mdy" type="radio" tabindex=1 onclick="reformatDates()"><label for="mdy">md, y</label>
    <input id="ymd" name="dateformat" value="ymd" type="radio" tabindex=1 onclick="reformatDates()"><label for="ymd">y-m-d</label>
    </td>
    <td><label for="edition">&nbsp;Edition: </label></td>
    <td colspan=3><input type="text" tabindex=1 style="width:100%%" id="edition"></td></tr>

    <tr><td><label for="series">Series: </label></td>
    <td colspan=3><input type="text" tabindex=1 style="width:100%%" id="series"></td>
    <td><label for="volume">&nbsp;Volume: </label></td>
    <td colspan=3><input type="text" tabindex=1 style="width:100%%" id="volume"></td></tr>

    <tr><td><label for="pages">Page number(s):</label></td>
    <td colspan=3><input type="text" tabindex=1 style="width:100%%; background-color: #FFFF99" id="pages" name="pages" value="%s" onFocus="this.style.backgroundColor='';"></td>
    <td><label for="chapter">&nbsp;Chapter: </label></td>
    <td colspan=3><input type="text" tabindex=1 style="width:100%%" id="chapter"></td></tr>

    <tr><td><label for="isbn">ISBN: </label></td>
    <td colspan=3><input type="text" tabindex=1 style="width:100%%" id="isbn" value="%s"></td>
    <td><label for="language">&nbsp;Language: </label></td>
    <td colspan=3><input type="text" tabindex=1 style="width:100%%" id="language"></td></tr>

    <!--    <td><label for="oclc">&nbsp;OCLC: </label></td>
    <td colspan=3><input type="text" tabindex=1 style="width:100%%" id="oclc"></td></tr>
    -->

    <tr><td><label for="url">URL: </label></td>
    <td colspan=3><input type="text" tabindex=1 style="width:100%%" id="url" value="%s"></td>
    <td><label for="accessdate">&nbsp;Access&nbsp;date:</label></td>
    <td colspan=3><input type="text" tabindex=1 style="width:50%%" id="accessdate"><input type="button" tabindex=1 value="<Today" onClick="setAccessDateToday()"></td></tr>

    <tr><td><label for="otherfields">Other&nbsp;fields:</label></td>
    <td colspan=3><input type="text" tabindex=1 style="width:100%%" name="otherfields" id="otherfields" value="%s"></td>
    <td><label for="refname">&nbsp;Ref&nbsp;name: </label></td>
    <td colspan=3><input type="text" tabindex=1 style="width:100%%" id="refname"><!--<input type="button" tabindex=1 value="<Make" onClick="makeRefname()">--></td>
    </tr>
    </table>
    <input type="button" tabindex=1 value="Make citation" onClick="makeCiteBook()">
    <input type="radio" tabindex=1 name="template" id="cite_book" value="cite_book" checked="1" onClick="makeCiteBook()"><label for="cite_book">{{cite book}}</label> <sup><a href="http://en.wikipedia.org/wiki/Template:Cite_book" target="_blank">[doc]</a></sup>
    <input type="radio" tabindex=1 name="template" id="citation" value="citation" onClick="makeCiteBook()"><label for="citation">{{citation}}</label> <sup><a href="http://en.wikipedia.org/wiki/Template:Citation" target="_blank">[doc]</a></sup>
    <input type="radio" tabindex=1 name="template" id="plain" value="plain" onClick="makeCiteBook()"><label for="plain">plain wikicode</label>
    <input type="checkbox" tabindex=1 name="verbose" id="verbose" value="verbose" onClick="makeCiteBook()"><label for="verbose">Vertical form</label>
    <input type="checkbox" tabindex=1 name="extraparams" id="extraparams" value="extraparams" onClick="makeCiteBook()"><label for="extraparams">Extra parameters</label>
    <input type="checkbox" tabindex=1 name="harv" id="harv" value="harv" onClick="makeCiteBook()"><label for="harv">ref=harv</label>
    <hr>""" % (cgi.escape(coauthors, 1), cgi.escape(publisher, 1), cgi.escape(date, 1), cgi.escape(page, 1), cgi.escape(isbn, 1), cgi.escape(new_url, 1), cgi.escape('|'.join(otherfields), 1))

    print """<font color="DarkOliveGreen">3: Below is the complete reference tag. Copy and paste it into the Wikipedia article. Press "Make citation" above to regenerate if you have changed anything above.</font><br />
    <textarea rows="5" cols="100" style="width: 99%" id="fullcite" tabindex=1></textarea>"""

    print """<br /><input type="button" value="Make preview" tabindex=1 onClick="makePreview()">
    <img id="progress" src="static/progress.gif" style="visibility: hidden" /><span id="clipboardspan"></span><br />
    <fieldset><legend>Preview</legend><span id="previewSpan"></span></fieldset>
    <br /><br /></span>"""

    printFooter()


if __name__ == "__main__":
    main()

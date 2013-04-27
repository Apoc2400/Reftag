#
#
#

#__author__ = 'Apoc2400'

import wsgiref.handlers
from google.appengine.ext import webapp
from google.appengine.api import users
import atom.url
import gdata.service
import gdata.alt.appengine
import gdata.books
import gdata.books.service
from google.appengine.api import memcache
import sys
import os

import cgi
import cgitb; cgitb.enable()
import re
import urllib
from django.utils import simplejson as json

#import wsgiref.handlers
#from google.appengine.api import users
#from google.appengine.ext import webapp
#from google.appengine.ext import db
#from google.appengine.api import urlfetch
#import urllib # Used to unescape URL parameters.
#import gdata.service
#import gdata.alt.appengine
#import gdata.auth
#import atom
#import atom.http_interface
#import atom.token_store
#import atom.url
#import settings


def error(message):
    print 'Content-Type: text/plain'
    print ''
    print 'Error: ', message


def main():

    book_url = ''
    form = cgi.FieldStorage()
    if (not form.has_key("book_url")):
        error('No URL.')
        return
    book_url = form["book_url"].value

    if (not form.has_key("callback")):
        error('No callback.')
        return
    callback = form["callback"].value

    memcache_key = '5:' + os.environ['CURRENT_VERSION_ID'] + '/' + callback + ':' + book_url
    memcache_jsonp = memcache.get(memcache_key)
    if memcache_jsonp is not None:
        #print >> sys.stderr, "From memcache: " + memcache_key 
        print 'Content-Type: text/javascript'
        print ''
        print memcache_jsonp
        return
    else:
        #print >> sys.stderr, "From fetch: " + memcache_key
        pass

    dateformat = ''
    if (form.has_key("dateformat")):
        dateformat = form["dateformat"].value

    checked_dmy = ''
    checked_mdy = ''
    checked_ymd = ''
    if dateformat == 'dmy':
        checked_dmy = ' checked="1"'
    elif dateformat == 'mdy':
        checked_mdy = ' checked="1"'
    elif dateformat == 'ymd':
        checked_ymd = ' checked="1"'
    else:
        checked_dmy = ' checked="1"'
        dateformat = 'dmy'


    if not re.search('books.google.', book_url, re.I) and not re.search('\?id=', book_url, re.I):
        error('Not a Google Books URL.')
        return
    urlsep = re.search('\?([^#]*)', book_url)
    if not urlsep:
        error('Bad URL.')
        return

    book_url_qs = urlsep.group(1)
    book_url_qs_fields = cgi.parse_qs(book_url_qs)

    if not book_url_qs_fields.has_key("id"):
        error('Bad URL. It has to be for a specific book, not a search result page')
        return
    book_id = book_url_qs_fields["id"][0]
    page = ''
    page_string = ''
    if book_url_qs_fields.has_key('pg'):
        page_string = book_url_qs_fields['pg'][0]
        match = re.search('\D*(\d+)', page_string)
        if match:
            page = match.group(1) + u"\u2013".encode("utf-8")
    
    
    new_url = 'http://books.google.com/books?id=' + urllib.quote_plus(book_id)
    if page_string:
        new_url += '&pg=' + urllib.quote_plus(page_string)

    client = gdata.books.service.BookService()
    gdata.alt.appengine.run_on_appengine(client)

    thisbook = client.get_by_google_id(book_id)    # '8cp-Z_G42g4C'
    thisdict = thisbook.to_dict()
    #thisdict = {'embeddability': 'embeddable', 'info': 'http://books.google.com/books?id=9PE2T2a5fDYC&ie=ISO-8859-1&source=gbs_gdata', 'description': 'Ramon Sarr\xc3\xb3 explores an iconoclastic religious movement initiated by a Muslim preacher during the French colonial period. Employing an ethnographic approach that respects the testimony of those who suffered violence as opposed to those who wanted to "get rid of custom," this work discusses the extent to which iconoclasm produces a rupture of religious knowledge and identity and analyzes its relevance in the making of modern nations and citizens. The Politics of Religious Change on the Upper Guinea Coastexamines the historical complexity of the interface between Islam, traditional religions, and Christianity in West Africa, and how this interface connects to dramatic political change. The book unveils a rare history and brokers a dialogue between a long tradition of anthropology and contemporary anthropological debates. A wide range of readers, particularly those with an interest in the anthropology of religion, iconoclasm, the history and anthropology of West Africa, or the politics of heritage, will gravitate toward this work.', 'format': 'book', 'publishers': ['Edinburgh University Press'], 'identifiers': [('google_id', '9PE2T2a5fDYC'), ('ISBN', '0748635157'), ('ISBN', '9780748635153')], 'thumbnail': 'http://bks9.books.google.com/books?id=9PE2T2a5fDYC&printsec=frontcover&img=1&zoom=5&edge=curl&sig=ACfU3U0LyllDnVUHiadMIrdIuvVAiURtuQ&source=gbs_gdata', 'subjects': ['Iconoclasm', 'Guinea', 'Iconoclasm/ Guinea', 'Religion and politics', 'History / Europe / General', 'Social Science / Human Geography', 'Social Science / Ethnic Studies / General', 'Social Science / Customs & Traditions', 'Religion / Ethnic & Tribal', 'Religion / General', 'History / Africa / General', 'Religion / Comparative Religion', 'History / General', 'History / Africa / General', 'Religion / Ethnic & Tribal', 'Religion / Islam / General', 'Religion / Religion, Politics & State', 'Social Science / Human Geography', 'Social Science / Islamic Studies', 'Travel / Africa / General'], 'authors': ['Ramon Sarr\xc3\xb3', 'John Smith', 'Jane Smith', 'Olaus Petrus', 'Mick Paff'], 'date': '2009-05-03', 'title': 'The Politics of Religious Change on the Upper Guinea Coast: Iconoclasm Done and Undone', 'viewability': 'view_partial', 'annotation': 'http://www.google.com/books/feeds/users/me/volumes'}

    #print 'Got dict: ' + str(thisdict)+  '<br />'

    #print thisdict['title'], "<br />"
    title = thisdict['title'] if thisdict.has_key('title') else ''
    date = thisdict['date'] if thisdict.has_key('date') else ''
    publisher = (', '.join(thisdict['publishers'])) if thisdict.has_key('publishers') else ''
    authors = thisdict['authors'] if thisdict.has_key('authors') else ''

    coauthors = ', '.join(authors[3:])

    isbn = ''
    issn = ''
    iccn = ''
    oclc = ''
    other_id_list = []
    otherfields = []
    if thisdict.has_key('identifiers'):
        for idpair in thisdict['identifiers']:
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


    other_id = ', '.join(other_id_list)
    if len(other_id):
        otherfields.append('id=' + other_id)

    bookdata = {'title': title, 
            'isbn': isbn,
            'publisher': publisher,
            'pages': page,
            'url': new_url,
            'authors': authors,
            'date': date}
    jsonstr = json.dumps(bookdata, sort_keys=True, indent=4, ensure_ascii=False)
    jsonp = callback + '(' + jsonstr + ');'
    
    print 'Content-Type: text/javascript'
    print ''
    print jsonp

    memcache.add(memcache_key, jsonp, 3600)


if __name__ == "__main__":
    main()

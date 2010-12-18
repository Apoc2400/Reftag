from cachedfetch import cachedFetch
import urllib
import xml.dom.minidom
from keys import crossref_id

def getText(startnode):
    rc = ""
    for node in startnode.childNodes:
        if node.nodeType == node.TEXT_NODE:
            rc = rc + node.data
    return rc


def doiFetchInfo(doi):

    querystring = urllib.urlencode([('id', 'doi:'+doi)])
    url = "http://www.crossref.org/openurl/?pid=" + crossref_id + "&noredirect=true&" + querystring
    xmldata = cachedFetch(url, 3600)
    if xmldata == '':
        error('Bad data from CrossRef')
    
    xmldoc = xml.dom.minidom.parseString(xmldata)
    citedata = {}
    
    simplefields = {'doi': 'doi',
    'issn': 'issn',
    'journal': 'journal_title',
    'volume': 'volume',
    'issue': 'issue',
    'year': 'year',
    'title': 'article_title',
    'isbn': 'isbn',
    }
    
    for key, cr_tagname in simplefields.iteritems():
        cr_node = xmldoc.getElementsByTagName(cr_tagname)
        if cr_node:
            citedata[key] = getText(cr_node[0])

    cr_contributors = xmldoc.getElementsByTagName('contributor')
    authors = [];
    for cr_contributor in cr_contributors:
        author = {}
        cr_givenname = cr_contributor.getElementsByTagName('given_name')
        if cr_givenname:
            author['first'] = getText(cr_givenname[0])
        cr_surname = cr_contributor.getElementsByTagName('surname')
        if cr_surname:
            author['last'] = getText(cr_surname[0])
        if author['first'].isupper() and author['last'].isupper():
            author['first'] = author['first'].title()
            author['last'] = author['last'].title()
        authors.append(author)
    if authors:
        citedata['authors'] = authors;
    
    cr_first_page = xmldoc.getElementsByTagName('first_page')
    cr_last_page = xmldoc.getElementsByTagName('last_page')
    if cr_first_page:
        citedata['pages'] = getText(cr_first_page[0])
    if cr_last_page:
        citedata['pages'] += u"\u2013" + getText(cr_last_page[0])
        

    return citedata

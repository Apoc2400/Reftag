from doifetch import doiFetchInfo
import cgi
from django.utils import simplejson as json
 
def error(message):
    print 'Content-Type: text/plain'
    print ''
    print 'Error: ', message
    exit()

 
def main():
    doi = '';
    form = cgi.FieldStorage()
    if (not form.has_key("doi")):
        error('No DOI.')
    doi = form["doi"].value

    if (not form.has_key("callback")):
        error('No callback.')
    callback = form["callback"].value
 
    citedata = doiFetchInfo(doi)
 
    jsonstr = json.dumps(citedata, sort_keys=True, indent=4, ensure_ascii=False)
    jsonp = callback + '(' + jsonstr + ');'
    
    print 'Content-Type: text/javascript'
    print ''
    print jsonp.encode('utf8')

 
 
if __name__ == "__main__":
    main()
    

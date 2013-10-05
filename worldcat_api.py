from worldcat.request.xid import xOCLCNUMRequest, xISBNRequest

def get_by_oclc(oclc):

    o = xOCLCNUMRequest(rec_num=oclc, method='getMetadata').get_response().data

    for i in o['list']:
        #print i
        for isbn in i['isbn']:
            #print isbn
            return get_by_isbn(isbn)

def get_by_isbn(isbn):
    output = {}
    o = xISBNRequest(rec_num=isbn, method='getMetadata').get_response().data
    for i in o['list']:
        #print i
        if 'title' in i:
            output['title'] = i['title']

    return output


if __name__ == "__main__":
    print get_by_oclc(550538756)
    

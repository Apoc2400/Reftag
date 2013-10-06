from worldcat.request.xid import xOCLCNUMRequest, xISBNRequest

def get_by_oclc(oclc):
    o = xOCLCNUMRequest(rec_num=oclc, method='getMetadata').get_response().data

    for i in o['list']:
        #print i
        for isbn in i['isbn']:
            #print isbn
            output = get_by_isbn(isbn)
            # First the known oclc, in case it is not returned from WorldCat
            output['identifiers'].add(('oclc', str(oclc)))
            return output

def get_by_isbn(isbn):
    o = xISBNRequest(rec_num=isbn, method='getMetadata').get_response().data
    
    assert len(o['list']) == 1
    data_dict = o['list'][0]
    print data_dict

    output = {}

    fields = ['title', 'author']
    for field in fields:
        if field in data_dict:
            output[field] = data_dict[field]
            
    if 'year' in data_dict:
        output['date'] = data_dict['year']
            
    if 'publisher' in data_dict:
        output['publishers'] = [data_dict['publisher']]
            
    identifiers = set()
    # First add the known isbn
    identifiers.add(('isbn', str(isbn)))
    if 'isbn' in data_dict:
        for otherisbn in data_dict['isbn']:
            identifiers.add(('isbn', otherisbn))
    if 'oclcnum' in data_dict:
        for otheroclc in data_dict['oclcnum']:
            identifiers.add(('oclc', otheroclc))
    output['identifiers'] = identifiers

    return output


if __name__ == "__main__":
    print get_by_oclc(550538756)
    #print get_by_oclc(222891799)
    
    

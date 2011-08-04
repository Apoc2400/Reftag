import re
import isbn_lengthmaps

class IsbnError(Exception): pass

# ISBN is malformed, such as too short, too long or contains invalid characters
class IsbnMalformedError(IsbnError): pass

# Unable to hyphenate is ISBN. Either it does not exist, or 
# the ranges information used by this library is out of date
class IsbnUnableToHyphenateError(IsbnError): pass

 
def hyphenate(input):
    """Add hyphens to an International Standard Book Number (ISBN)
    
    >>> hyphenate('1843560283')
    '1-84356-028-3'
    
    10 or 13 digit ISBN are hyphenated. Hyphens and whitespace in the input
    is stipped. 
    
    This function uses a database of ISBN ranges, so might not work for
    ISBNs in recently allocated ranges.
    """

    without_hyphens = re.sub('[\s-]', '', input)
    
    if re.match('[^0-9X]', without_hyphens):
        raise IsbnMalformedError, "Must only contain digits and/or and X"
    
    with_hyphens = ''
    
    GS1_prefix = None
    if len(without_hyphens) == 13:
        GS1_prefix = without_hyphens[:3]
        with_hyphens = GS1_prefix + '-'
        without_hyphens = without_hyphens[3:]
    elif len(without_hyphens) == 10:
        GS1_prefix = '978'
    else:
        raise IsbnMalformedError, "Length must be 10 or 13"
    
    first7 = int(without_hyphens[:7])
    groupPrefixLength = None
    if not isbn_lengthmaps.groups_length.has_key(GS1_prefix):
        raise IsbnUnableToHyphenateError, "GS1 prefix %s not recognized" % GS1_prefix
    for curRange in isbn_lengthmaps.groups_length[GS1_prefix]:
        if curRange['min'] <= first7 <= curRange['max']:
            groupPrefixLength = curRange['length']
            break
    
    if groupPrefixLength is None:
        raise IsbnUnableToHyphenateError, "Not in any recognized group range"
    elif groupPrefixLength == 0:
        raise IsbnUnableToHyphenateError, "Group range is unused"
    
    groupPrefix = without_hyphens[:groupPrefixLength]
    without_hyphens = without_hyphens[groupPrefixLength:]
    with_hyphens += groupPrefix + '-'
    
    first7 = int(without_hyphens[:7].ljust(7, '0'))
    publisherLength = None
    GS1_and_group = GS1_prefix + '-' + groupPrefix
    if not isbn_lengthmaps.publisher_length.has_key(GS1_and_group):
        raise IsbnUnableToHyphenateError, "Prefix %s not recognized" % GS1_and_group
    for curRange in isbn_lengthmaps.publisher_length[GS1_and_group]:
        if curRange['min'] <= first7 <= curRange['max']:
            publisherLength = curRange['length']
            break

    if publisherLength is None:
        raise IsbnUnableToHyphenateError, "Not in any recognized publisher range"
    elif publisherLength == 0:
        raise IsbnUnableToHyphenateError, "Publisher range is unused"
    
    publisher = without_hyphens[:publisherLength]
    without_hyphens = without_hyphens[publisherLength:]
    with_hyphens += publisher + '-'
    
    bookId = without_hyphens[:-1]
    checkDigit = without_hyphens[-1:]
    with_hyphens += bookId + '-' + checkDigit
    
    return with_hyphens
    

def try_hyphenate(input):
    try:
        return hyphenate(input)
    except IsbnUnableToHyphenateError:
        return input
        

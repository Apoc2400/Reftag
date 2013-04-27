from __future__ import absolute_import, print_function, unicode_literals
import re
import sys
from . import isbn_lengthmaps

class IsbnError(Exception): 
    """Base class for exceptions thrown by hyphenate and try_hyphenate."""
    pass


class IsbnMalformedError(IsbnError): 
    """ISBN is malformed, such as too short, too long or 
    contains invalid characters"""
    pass

class IsbnUnableToHyphenateError(IsbnError):
    """Unable to hyphenate is ISBN. Either it does not exist, or
    the ranges information used by this library is out of date"""
    pass


def hyphenate(input_data):
    """Add hyphens to an International Standard Book Number (ISBN)
    
    >>> hyphenate('1843560283')
    '1-84356-028-3'
    
    10 or 13 digit ISBN are hyphenated. Hyphens and whitespace in the input
    is stipped.
    
    This function uses a database of ISBN ranges, so might not work for
    ISBNs in recently allocated ranges.
    
    Compatible with both Python 2 and 3.
    """

    # Convert input to Unicode (only needed in Python 2)
    return_ascii = False
    if sys.version_info < (3, 0, 0):
        if isinstance(input_data, str):
            input_data = unicode(input_data)
            return_ascii = True

    without_hyphens = re.sub('[\s-]', '', input_data)
    
    # Must be digits, maybe an X at the end
    if not re.match('^[0-9]+X?$', without_hyphens):
        raise IsbnMalformedError("Must only contain digits and/or and X")

    with_hyphens = ''
    
    GS1_prefix = None
    if len(without_hyphens) == 13:
        GS1_prefix = without_hyphens[:3]
        with_hyphens = GS1_prefix + '-'
        without_hyphens = without_hyphens[3:]
    elif len(without_hyphens) == 10:
        GS1_prefix = '978'
    else:
        raise IsbnMalformedError("Length must be 10 or 13")
    
    first7 = int(without_hyphens[:7])
    group_prefix_length = None
    if GS1_prefix not in isbn_lengthmaps.groups_length:
        raise IsbnUnableToHyphenateError("GS1 prefix %s not recognized" % 
            GS1_prefix)
    for cur_range in isbn_lengthmaps.groups_length[GS1_prefix]:
        if cur_range['min'] <= first7 <= cur_range['max']:
            group_prefix_length = cur_range['length']
            break
    
    if group_prefix_length is None:
        raise IsbnUnableToHyphenateError("Not in any recognized group range")
    elif group_prefix_length == 0:
        raise IsbnUnableToHyphenateError("Group range is unused")
    
    group_prefix = without_hyphens[:group_prefix_length]
    without_hyphens = without_hyphens[group_prefix_length:]
    with_hyphens += group_prefix + '-'
    
    first7 = int(without_hyphens[:7].ljust(7, '0'))
    publisher_length = None
    GS1_and_group = GS1_prefix + '-' + group_prefix
    if GS1_and_group not in isbn_lengthmaps.publisher_length:
        raise IsbnUnableToHyphenateError("Prefix %s not recognized" % 
            GS1_and_group)
    for cur_range in isbn_lengthmaps.publisher_length[GS1_and_group]:
        if cur_range['min'] <= first7 <= cur_range['max']:
            publisher_length = cur_range['length']
            break

    if publisher_length is None:
        raise IsbnUnableToHyphenateError(
            "Not in any recognized publisher range")
    elif publisher_length == 0:
        raise IsbnUnableToHyphenateError("Publisher range is unused")
    
    publisher = without_hyphens[:publisher_length]
    without_hyphens = without_hyphens[publisher_length:]
    with_hyphens += publisher + '-'
    
    book_id = without_hyphens[:-1]
    check_digit = without_hyphens[-1:]
    with_hyphens += book_id + '-' + check_digit

    # If this is Python 2, and the input was a non-Unicode string, 
    # then return an ascii string
    if return_ascii:
        with_hyphens = with_hyphens.encode("ascii")
    
    return with_hyphens
    

def try_hyphenate(isbn):
    """Attempts to add hyphens to an International Standard Book Number (ISBN).
    If not possible, return the input string. Can still throw
    IsbnMalformedError for malformed input.
    This is a wrapper for hyphenate."""
    try:
        return hyphenate(isbn)
    except IsbnUnableToHyphenateError:
        return isbn
        

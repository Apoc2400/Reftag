isbn_hyphenate is a Python library to add hyphens in the right place to an ISBN (International Standard Book Number). Example:
>>> isbn_hyphenate.hyphenate("9781590593561")
'978-1-59059-356-1'

Most libraries for handling ISBNs can not do hyphenation because it requires using a list of prefixes, available from the International ISBN Agency.

isbn_hyphenate can handle both 10 and 13 digit ISBNs, and will keep the number of digits. 
If the ISBN is malformed (wrong length or invalid characters) an IsbnMalformedError exception is raised. 
If the correct hyphen positions cannot be determined, an IsbnUnableToHyphenateError exception is raised. 
This can mean that the input ISBN is wrong, or it is in a range that is not yet in the known list.

To update the prefix list:
1) Download a new RangeMessage.xml file from ttp://www.isbn-international.org/agency?rmxml=1
2) Convert it to Python format: ./isbn_xml2py.py > isbn_lengthmaps.py

These alternative Python libraries can also hyphenate:
* python-stdnum http://pypi.python.org/pypi/python-stdnum
* isbnid http://code.google.com/p/isbnid/

# By Markus on stackoverflow.com
# http://stackoverflow.com/questions/1066933/python-extract-domain-name-from-url
# Modified by Apoc2400
#
# The file effective_tld_names.dat is downloaded from
# http://mxr.mozilla.org/mozilla/source/netwerk/dns/src/effective_tld_names.dat?raw=1
# See http://publicsuffix.org/

from __future__ import with_statement
from urlparse import urlparse

# load tlds, ignore comments and empty lines:
with open("effective_tld_names.dat") as tldFile:
    tlds = [line.strip() for line in tldFile if line[0] not in "/\n"]

def getDomain(url, tlds):
    urlElements = urlparse(url)[1].split('.')
    # urlElements = ["abcde","co","uk"]

    for i in range(-len(urlElements),0):
        lastIElements = urlElements[i:]
        #    i=-3: ["abcde","co","uk"]
        #    i=-2: ["co","uk"]
        #    i=-1: ["uk"] etc

        candidate = ".".join(lastIElements) # abcde.co.uk, co.uk, uk
        wildcardCandidate = ".".join(["*"]+lastIElements[1:]) # *.co.uk, *.uk, *
        exceptionCandidate = "!"+candidate

        # match tlds: 
        if (exceptionCandidate in tlds):
            return ".".join(urlElements[i:]) 
        if (candidate in tlds or wildcardCandidate in tlds):
            return ".".join(urlElements[i-1:])
            # returns "abcde.co.uk"

    raise ValueError("Domain not in global list of TLDs")

def domainFromURL(url):
    return getDomain(url,tlds)

#print getDomain("http://abcde.co.uk",tlds)

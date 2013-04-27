#!/usr/bin/env python

from __future__ import absolute_import, print_function, unicode_literals
import xml.dom.minidom
import sys

def get_text(startnode):
    text = ""
    for node in startnode.childNodes:
        if node.nodeType == node.TEXT_NODE:
            text = text + node.data
    return text

def parse_prefix_length_map(dom):
    prefix = get_text(dom.getElementsByTagName("Prefix")[0])
    length_map = []
    for rule in dom.getElementsByTagName("Rules")[0].getElementsByTagName("Rule"):
        rule_range = get_text(rule.getElementsByTagName("Range")[0])
        length = get_text(rule.getElementsByTagName("Length")[0])
        (range_min, range_max) = rule_range.strip().split('-')
        range_to_length = { 'min'    : int(range_min),
                            'max'    : int(range_max),
                            'length' : int(length)
                            }
        length_map.append(range_to_length)
    return (prefix, length_map)

if len(sys.argv) != 2:
    print("Usage:\n./isbn_xml2py.py RangeMessage.xml > isbn_lengthmaps.py", file=sys.stderr)
    sys.exit(2)

def main():
    xmlfile = sys.argv[1]
    dom = xml.dom.minidom.parse(xmlfile)

    ISBN_range_message = dom.getElementsByTagName("ISBNRangeMessage")[0]

    groups_length = {}
    for ean in ISBN_range_message.getElementsByTagName("EAN.UCCPrefixes")[0].getElementsByTagName("EAN.UCC"):
        (prefix, length_map) = parse_prefix_length_map(ean)
        groups_length[prefix] = length_map

    publisher_length = {}
    for group in ISBN_range_message.getElementsByTagName("RegistrationGroups")[0].getElementsByTagName("Group"):
        (prefix, length_map) = parse_prefix_length_map(group)
        publisher_length[prefix] = length_map

    message_serial = get_text(ISBN_range_message.getElementsByTagName("MessageSerialNumber")[0])
    message_date = get_text(ISBN_range_message.getElementsByTagName("MessageDate")[0])

    print('# Generated from RangeMessage.xml with isbn_xml2py.py')
    print('# Available from http://www.isbn-international.org/agency?rmxml=1')
    print('# MessageDate: ' + message_date)
    print('# MessageSerialNumber: ' + message_serial)
    print('groups_length = ' + repr(groups_length).replace("u'", "'"))
    print('publisher_length = ' + repr(publisher_length).replace("u'", "'"))

main()

#!/usr/bin/env python
"""Unit tests for isbn_hyphenate.py"""

from __future__ import absolute_import, print_function, unicode_literals
import isbn_hyphenate
import unittest
import sys

class KnownValues(unittest.TestCase):
    knownValues = ( "99921-58-10-7",
                    "9971-5-0210-0",
                    "960-425-059-0",
                    "80-902734-1-6",
                    "85-359-0277-5",
                    "1-84356-028-3",
                    "0-684-84328-5",
                    "0-8044-2957-X",
                    "0-85131-041-9",
                    "0-943396-04-2",
                    "0-9752298-0-X",
                    "978-0-321-53496-5",
                    "978-3-16-148410-0",
                    "1-4028-9462-7",
                    "978-1-4028-9462-6",
                    "978-99953-838-2-4",
                    "978-99930-75-89-9",
                    "978-1-59059-356-1",
                  )

    def test_hyphenating_known_values(self):
        for with_hyphens in self.knownValues:
            without_hyphens = with_hyphens.replace('-', '')
            self.assertEqual(isbn_hyphenate.hyphenate(without_hyphens), with_hyphens)
            
    def test_try_hyphenating_known_values(self):
        for with_hyphens in self.knownValues:
            without_hyphens = with_hyphens.replace('-', '')
            self.assertEqual(isbn_hyphenate.try_hyphenate(without_hyphens), with_hyphens)

    # Only test non-unicode if Python2
    if sys.version_info < (3,0,0):
        def test_hyphenating_known_values_not_unicode(self):
            for with_hyphens in self.knownValues:
                without_hyphens = with_hyphens.replace('-', '')
                without_hyphens_ascii = without_hyphens.encode("ascii")
                self.assertEqual(isbn_hyphenate.hyphenate(without_hyphens_ascii), with_hyphens.encode("ascii"))


class BadInput(unittest.TestCase):
    def test_bad_characters(self):
        self.assertRaises(isbn_hyphenate.IsbnMalformedError, isbn_hyphenate.hyphenate, "fghdf hdfjhfgj")
    def test_bad_characters2(self):
        self.assertRaises(isbn_hyphenate.IsbnMalformedError, isbn_hyphenate.hyphenate, "085131ffff")
    def test_bad_charactersX(self):
        self.assertRaises(isbn_hyphenate.IsbnMalformedError, isbn_hyphenate.hyphenate, "X604250590")
        self.assertRaises(isbn_hyphenate.IsbnMalformedError, isbn_hyphenate.hyphenate, "960X250590")
        self.assertRaises(isbn_hyphenate.IsbnMalformedError, isbn_hyphenate.hyphenate, "96042X0590")
    def test_try_bad_characters(self):
        self.assertRaises(isbn_hyphenate.IsbnMalformedError, isbn_hyphenate.try_hyphenate, "fghdf hdfjhfgj")

    def test_try_bad_non_ascii_character(self):
        self.assertRaises(isbn_hyphenate.IsbnMalformedError, isbn_hyphenate.try_hyphenate, "9971\u260302100")

    def test_too_short(self):
        self.assertRaises(isbn_hyphenate.IsbnMalformedError, isbn_hyphenate.hyphenate, "12345")

    def test_unknown_prefix(self):
        self.assertRaises(isbn_hyphenate.IsbnUnableToHyphenateError, isbn_hyphenate.hyphenate, "9751402894626")

    def test_unused_prefix(self):
        self.assertRaises(isbn_hyphenate.IsbnUnableToHyphenateError, isbn_hyphenate.hyphenate, "9786500042626")

    def test_unknown_prefix2(self):
        self.assertRaises(isbn_hyphenate.IsbnUnableToHyphenateError, isbn_hyphenate.hyphenate, "9789999999626")

    def test_unused_prefix2(self):
        self.assertRaises(isbn_hyphenate.IsbnUnableToHyphenateError, isbn_hyphenate.hyphenate, "9789927512300")

    def test_try_unknown_prefix(self):
        isbn_unknown = "9751402894626"
        self.assertEqual(isbn_hyphenate.try_hyphenate(isbn_unknown), isbn_unknown)

    def test_empty_input(self):
        self.assertRaises(isbn_hyphenate.IsbnMalformedError, isbn_hyphenate.hyphenate, "")


unittest.main()

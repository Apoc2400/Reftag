"""Unit test for isbn_hyphenate.py"""

import isbn_hyphenate
import unittest

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
                  )

    def testHyphenatingKnownValues(self):
        for with_hyphens in self.knownValues:
            without_hyphens = with_hyphens.replace('-', '')
            self.assertEqual(isbn_hyphenate.hyphenate(without_hyphens), with_hyphens)
            
    def testTryHyphenatingKnownValues(self):
        for with_hyphens in self.knownValues:
            without_hyphens = with_hyphens.replace('-', '')
            self.assertEqual(isbn_hyphenate.try_hyphenate(without_hyphens), with_hyphens)


class BadInput(unittest.TestCase):                            
    def testBadCharacters(self):                                          
        self.assertRaises(isbn_hyphenate.IsbnMalformedError, isbn_hyphenate.hyphenate, "fghdf hdfjhfgj")
    def testTryBadCharacters(self):                                          
        self.assertRaises(isbn_hyphenate.IsbnMalformedError, isbn_hyphenate.try_hyphenate, "fghdf hdfjhfgj")

    def testTooShort(self):                                          
        self.assertRaises(isbn_hyphenate.IsbnMalformedError, isbn_hyphenate.hyphenate, "12345")


    def testUnknownPrefix(self):                                          
        self.assertRaises(isbn_hyphenate.IsbnDoesNotExistError, isbn_hyphenate.hyphenate, "9751402894626")

    def testUnusedPrefix(self):                                          
        self.assertRaises(isbn_hyphenate.IsbnDoesNotExistError, isbn_hyphenate.hyphenate, "9786500042626")

    def testUnknownPrefix2(self):                                          
        self.assertRaises(isbn_hyphenate.IsbnDoesNotExistError, isbn_hyphenate.hyphenate, "9789999999626")

    def testUnusedPrefix2(self):                                          
        self.assertRaises(isbn_hyphenate.IsbnDoesNotExistError, isbn_hyphenate.hyphenate, "9789927512300")

    def testTryUnknownPrefix(self):                                          
        isbnUnknown = "9751402894626"
        self.assertEqual(isbn_hyphenate.try_hyphenate(isbnUnknown), isbnUnknown)

    def testEmptyInput(self):                                          
        self.assertRaises(isbn_hyphenate.IsbnMalformedError, isbn_hyphenate.hyphenate, "")


if __name__ == '__main__':
    unittest.main()

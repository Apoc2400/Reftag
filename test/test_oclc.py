import unittest
from worldcat_api import get_by_oclc, get_by_isbn

class TestOclc(unittest.TestCase):
    def test_oclc(self):
        oclc = '550538756'
        info = get_by_oclc(oclc)
        self.assertEquals(info['title'], "On hobos and homelessness")
        self.assertIn('Nels Anderson', info['authors'][0])
        self.assertIn('1998', info['date'])
        self.assertIn('Chicago Press', info['publishers'][0])

        identifiers = info['identifiers']
        self.assertIn(('oclc', oclc), identifiers)
        self.assertIn(('isbn', '9780226019666'), identifiers)

    def test_igma(self):
        oclc = '608542024'
        info = get_by_oclc(oclc)
        self.assertEquals(info['title'], "It probably won't kill you ... : twisted humor for your kitchen")
        self.assertEquals('Iyan Igma', info['authors'][0])
        self.assertIn('2009', info['date'])
        self.assertIn('CreateSpace', info['publishers'][0])

        identifiers = info['identifiers']
        self.assertIn(('oclc', oclc), identifiers)
        self.assertIn(('isbn', '9781441476562'), identifiers)

    def test_isbn(self):
        isbn = '1858286999'
        info = get_by_isbn(isbn)
        self.assertIn('Japan', info['title'])
        self.assertIn('Jan Dodd', info['authors'][0])
        self.assertIn('Simon Richmond', info['authors'][0])
        self.assertIn('2001', info['date'])
        self.assertIn('Rough Guides', info['publishers'][0])

        identifiers = info['identifiers']
        self.assertIn(('oclc', '222891799'), identifiers)
        self.assertIn(('isbn', isbn), identifiers)

    def test_bad_oclc(self):
        #Bad OCLC (actual an ISBN)
        oclc = '1441476563'
        info = get_by_oclc(oclc)
        self.assertIsNone(info)

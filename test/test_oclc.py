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
        
    def test_oclc_41271560(self):
        #'author': u'[Michael Wielsch, Jens Prahm] ; [trad. Liger Fran\xe7ois, Wolf Pierre M., Springinsfeld Serge].'
        info = get_by_oclc(41271560)
        self.assertEquals(info['authors'], ['Michael Wielsch', 'Jens Prahm'])

    def test_oclc_35883297(self):
        #'author': 'ed. by Kenneth T. MacKay'
        info = get_by_oclc(35883297)
        self.assertEquals(info['authors'], ['Kenneth T. MacKay'])

    def test_oclc_22239204(self):
        # Book found, but no data
        oclc = 22239204
        info = get_by_oclc(oclc)
        self.assertIn(('oclc', str(oclc)), info['identifiers'])
        self.assertNotIn('authors', info)
        self.assertNotIn('title', info)
        
    def test_oclc_2340417(self):
        # Returns an HTTP error
        oclc = 2340417
        info = get_by_oclc(oclc)
        self.assertIsNone(info)

    def test_bad_oclc(self):
        #Bad OCLC (actual an ISBN)
        oclc = '1441476563'
        info = get_by_oclc(oclc)
        self.assertIsNone(info)

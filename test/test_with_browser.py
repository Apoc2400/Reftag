import unittest
from splinter import Browser
import time


site = "http://localhost:8080/"
#site = "http://reftag.appspot.com/"

browser = Browser()
def tearDownModule():
    browser.quit()
    
def wait_until_filled(box):
    for i in range(10):
        content = box['value'] or box.text
        if content != '' and content != 'Updating...':
            return content
        time.sleep(1)
    assert 0
    return None
    

class TestArticleExists(unittest.TestCase):
    subsite = site + "wparticleexists.py"
    def test_exists(self):
        url = self.subsite + "?title=Africa"
        browser.visit(url) 
        self.assertTrue(browser.is_text_present('1'))
        self.assertFalse(browser.is_text_present('0'))

    def test_no_exists(self):
        url = self.subsite + "?title=UyUgyuygsdfuyggyu34t6js"
        browser.visit(url) 
        self.assertTrue(browser.is_text_present('0'))
        self.assertFalse(browser.is_text_present('1'))

    def test_no_title(self):
        url = self.subsite
        browser.visit(url) 
        self.assertFalse(browser.is_text_present('0'))
        self.assertFalse(browser.is_text_present('1'))
        self.assertTrue(browser.is_text_present('No title specified'))

class TestNytWeb(unittest.TestCase):
    subsite = site + "nytweb.py"
    def test_start(self):
        browser.visit(self.subsite)
        self.assertTrue(browser.is_text_present('New York Times Wikipedia reference generator'))
    
    def test_example(self):
        browser.visit(self.subsite + "?url=http%3A%2F%2Fwww.nytimes.com%2F2007%2F12%2F25%2Fworld%2Fafrica%2F25kenya.html") 
        self.assertTrue(browser.is_text_present('cite news|last=Gettleman'))

    def test_flow(self):
        browser.visit(self.subsite)
        browser.fill('url', 'http://www.nytimes.com/2007/12/25/world/africa/25kenya.html')
        browser.find_by_value('Load').click()
        self.assertTrue(browser.is_text_present('cite news|last=Gettleman'))

class TestDoiWeb(unittest.TestCase):
    subsite = site + "doiweb.py"
    def test_start(self):
        browser.visit(self.subsite)
        self.assertTrue(browser.is_text_present('DOI Wikipedia reference generator'))
    
    def test_example(self):
        browser.visit(self.subsite + "?doi=10.1111%2Fj.1600-0404.1986.tb04634.x")
        self.assertTrue(browser.is_text_present('title=Survival and cause'))

    def test_flow(self):
        browser.visit(self.subsite)
        browser.fill('doi', '10.1111/j.1600-0404.1986.tb04634.x')
        browser.find_by_value('Load').click()
        self.assertTrue(browser.is_text_present('title=Survival and cause'))
                
class TestGoogleBooks(unittest.TestCase):

    def setUp(self):
        browser.cookies.delete()
        browser.visit(site)
        browser.fill('book_url', 'http://books.google.com/books?id=aqmAc2fFsAUC&pg=PA90')
        browser.find_by_value('Load').click()

    def test_start(self):
        browser.visit(site)
        self.assertTrue(browser.is_text_present('Wikipedia citation tool for Google Books'))
    
    def test_flow(self):
        authorbox = browser.find_by_id('author1').first
        self.assertEquals(authorbox['value'], 'Nels Anderson')
        
        isbn = browser.find_by_id('isbn').first['value']
        self.assertEquals(isbn, '978-0-226-01966-6')
        
        citebox = browser.find_by_id('fullcite').first
        self.assertIn('|title=On Hobos', citebox['value'])
        
        preview = wait_until_filled(browser.find_by_id('previewSpan').first)
        self.assertIn('Nels Anderson (', preview)

        browser.find_by_id('edition').first.fill('Foo')
        browser.find_by_value('Make citation').first.click()
        self.assertIn('|edition=Foo|', citebox['value'])
        
        browser.find_by_id('authorLinkAnchor1').first.click()
        filled_in = browser.find_by_id('authorlink1').first['value']
        self.assertEquals(filled_in, 'Nels Anderson')
        
    def test_plain_wikicode(self):
        browser.find_by_id('plain').first.click()
        cite = wait_until_filled(browser.find_by_id('fullcite').first)
        self.assertIn('University of Chicago Press;', cite)
        
    def test_harv(self):
        browser.check('harv')
        cite = wait_until_filled(browser.find_by_id('fullcite').first)
        self.assertIn('|ref=harv', cite)
        
    def test_cookies(self):
        browser.choose('dateformat', 'ymd')
        browser.check('harv')
        
        browser.find_by_value('Load').click()
        
        self.assertTrue(browser.find_by_id('ymd').first.checked)
        self.assertTrue(browser.find_by_id('harv').first.checked)

if __name__ == '__main__':
    unittest.main()

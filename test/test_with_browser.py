import unittest
from splinter import Browser
import time
from siteurl import site

browser = Browser()
def tearDownModule():
    browser.quit()
    
def wait_until_filled(box):
    for i in range(10):
        content = box.value or box.text
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
        self.assertEqual(authorbox.value, 'Nels Anderson')
        
        isbn = browser.find_by_id('isbn').first.value
        self.assertEqual(isbn, '978-0-226-01966-6')
        
        citebox = browser.find_by_id('fullcite').first
        self.assertIn('|title=On Hobos', citebox.value)
        
        preview = wait_until_filled(browser.find_by_id('previewSpan').first)
        self.assertIn('Nels Anderson (', preview)

        browser.find_by_id('edition').first.fill('Foo')
        browser.find_by_value('Make citation').first.click()
        self.assertIn('|edition=Foo|', citebox.value)
        
        browser.find_by_id('authorLinkAnchor1').first.click()
        filled_in = browser.find_by_id('authorlink1').first.value
        self.assertEqual(filled_in, 'Nels Anderson')
        
    def test_plain_wikicode(self):
        browser.find_by_id('plain').first.click()
        cite = wait_until_filled(browser.find_by_id('fullcite').first)
        self.assertIn('University of Chicago Press;', cite)
        
    def test_harv(self):
        #pagebox = browser.find_by_id('pages').first
        #self.assertFalse(pagebox['disabled']);
        #self.assertIn('background-color: rgb(255, 255, 153);', pagebox['style']);
        
        browser.check('harv')
        cite = wait_until_filled(browser.find_by_id('fullcite').first)
        self.assertIn('|ref=harv', cite)
        self.assertNotIn('|page', cite)
        #self.assertTrue(pagebox['disabled']);
        #self.assertEqual(pagebox.value, '');
        #self.assertNotIn('background-color', pagebox['style']);
        
        browser.choose('template', 'citation')
        cite = wait_until_filled(browser.find_by_id('fullcite').first)
        self.assertNotIn('|ref=harv', cite)

        browser.choose('template', 'plain')
        cite = wait_until_filled(browser.find_by_id('fullcite').first)
        self.assertNotIn('|ref=harv', cite)

    def test_name_orbutton(self):
        authorbox = browser.find_by_id('author1').first
        lastbox = browser.find_by_id('last1').first
        firstbox = browser.find_by_id('first1').first
        
        self.assertEqual(authorbox.value, 'Nels Anderson')
        self.assertEqual(lastbox.value, '')
        self.assertEqual(firstbox.value, '')

        browser.click_link_by_text('or')
        
        self.assertEqual(authorbox.value, '')
        self.assertEqual(lastbox.value, 'Anderson')
        self.assertEqual(firstbox.value, 'Nels')

        browser.click_link_by_text('or')

        self.assertEqual(authorbox.value, 'Nels Anderson')
        self.assertEqual(lastbox.value, '')
        self.assertEqual(firstbox.value, '')
        
    def test_cookies(self):
        browser.choose('dateformat', 'ymd')
        browser.check('harv')
        
        browser.find_by_value('Load').click()
        
        self.assertTrue(browser.find_by_id('ymd').first.checked)
        self.assertTrue(browser.find_by_id('harv').first.checked)
        
    def test_authorformat_cookie(self):
        browser.click_link_by_text('or')
        
        otherbook = 'http://books.google.se/books?id=EzI8AAAAMAAJ&printsec=frontcover&dq=japan&hl=en&sa=X&ei=ZnFMUvO7IOWi4gSFwIGQBg&redir_esc=y#v=onepage&q=japan&f=false'
        browser.fill('book_url', otherbook)
        browser.find_by_value('Load').click()
        
        self.assertEqual(read_textbox('author1'), '')
        self.assertEqual(read_textbox('last1'), 'Nitta')
        self.assertEqual(read_textbox('first1'), 'Hideharu')

        self.assertEqual(read_textbox('author2'), '')
        self.assertEqual(read_textbox('last2'), 'Kanai')
        self.assertEqual(read_textbox('first2'), 'Madoka')

        self.assertEqual(read_textbox('author3'), '')
        self.assertEqual(read_textbox('last3'), 'Yamagiwa')
        self.assertEqual(read_textbox('first3'), 'Joseph Koshimi')
        
        browser.click_link_by_text('or')
        browser.find_by_value('Load').click()
        
        self.assertEqual(read_textbox('author1'), 'Hideharu Nitta')
        self.assertEqual(read_textbox('last1'), '')
        self.assertEqual(read_textbox('first1'), '')

        self.assertEqual(read_textbox('author2'), 'Madoka Kanai')
        self.assertEqual(read_textbox('last2'), '')
        self.assertEqual(read_textbox('first2'), '')

        self.assertEqual(read_textbox('author3'), 'Joseph Koshimi Yamagiwa')
        self.assertEqual(read_textbox('last3'), '')
        self.assertEqual(read_textbox('first3'), '')
        
        browser.click_link_by_text('or')
        self.assertEqual(read_textbox('author1'), '')
        
        browser.cookies.delete()
        browser.find_by_value('Load').click()
        self.assertEqual(read_textbox('author1'), 'Hideharu Nitta')
        
    def test_accessdate(self):
        self.assertEqual(read_textbox('accessdate'), '')
        browser.find_by_value('<Today').click()
        self.assertNotEqual(read_textbox('accessdate'), '')
        
    def test_errormessage(self):
        browser.fill('book_url', 'foo')
        browser.find_by_value('Load').click()
        self.assertTrue(browser.is_text_present('Error: Not a Google Books URL.'))
        
        browser.fill('book_url', 'books.google.se/books?foo')
        browser.find_by_value('Load').click()
        self.assertTrue(browser.is_text_present('Error: Bad URL. It has to be for a specific book, not a search result page'))

        browser.fill('book_url', 'books.google.se')
        browser.find_by_value('Load').click()
        self.assertTrue(browser.is_text_present('Error: Bad URL.'))

    def test_brackets(self):
        book_with_brackets = 'http://books.google.com/books?id=XvENAAAAQAAJ'
        # Title: Matthews's new Bristol directory [afterw.] Mathews's annual directory for the city and county of Bristol [afterw.] Mathews' Bristol directory
        # The brackets [] have caused problems before. They are not 
        # allowed in the templates and must be escaped.
        
        browser.fill('book_url', book_with_brackets)
        browser.find_by_value('Load').click()
        
        citebox = browser.find_by_id('fullcite').first
        self.assertIn('&#91;afterw.&#93; Mathews', citebox.value)
        self.assertNotIn('[', citebox.value)
        self.assertNotIn(']', citebox.value)
        
        browser.find_by_id('citation').first.click()
        self.assertIn('&#91;afterw.&#93; Mathews', citebox.value)
        self.assertNotIn('[', citebox.value)
        self.assertNotIn(']', citebox.value)
        
        browser.find_by_id('plain').first.click()
        wait_until_filled(citebox)
        self.assertIn('&#91;afterw.&#93; Mathews', citebox.value)

    def test_manual_oclc(self):
        citebox = browser.find_by_id('fullcite').first
        browser.fill('otherfields', 'oclc=1234567')
        browser.find_by_value('Make citation').first.click()
        self.assertIn('|oclc=1234567', citebox.value)
        
        browser.find_by_id('citation').first.click()
        self.assertIn('|oclc=1234567', citebox.value)
        
        browser.find_by_id('plain').first.click()
        wait_until_filled(citebox)
        self.assertIn('OCLC 1234567', citebox.value)
        
        browser.find_by_id('cite_book').first.click()
        browser.check('verbose')
        browser.check('extraparams')
        browser.check('harv')
        self.assertIn('|oclc=1234567', citebox.value)
        preview = wait_until_filled(browser.find_by_id('previewSpan').first)
        self.assertIn('OCLC', preview)
        
        
class TestOclcWeb(unittest.TestCase):
    def setUp(self):
        browser.cookies.delete()
        browser.visit(site)

    def test_oclc_input(self):
        oclc = '608542024'
        browser.fill('book_url', oclc)
        browser.find_by_value('Load').click()
        
        authorbox = browser.find_by_id('author1').first
        self.assertEqual(authorbox.value, 'Iyan Igma')

        self.assertEqual(browser.find_by_id('publisher').first.value, 'CreateSpace')
        
        isbn = browser.find_by_id('isbn').first.value
        self.assertEqual(isbn, '978-1-4414-7656-2')
        
        citebox = browser.find_by_id('fullcite').first
        self.assertIn('|title=It probably', citebox.value)
        self.assertIn('|oclc=' + oclc, citebox.value)
        
        preview = wait_until_filled(browser.find_by_id('previewSpan').first)
        self.assertIn('Iyan Igma (', preview)
        self.assertIn('OCLC', preview)
        self.assertIn('ISBN', preview)
        
    def test_bad_oclc(self):
        #Bad OCLC (actual an ISBN)
        oclc = '1441476563'
        browser.fill('book_url', oclc)
        browser.find_by_value('Load').click()
        self.assertTrue(browser.is_text_present('Error: The OCLC number entered was not found.'))


def read_textbox(id):
    return browser.find_by_id(id).first.value


if __name__ == '__main__':
    unittest.main()

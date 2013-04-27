import unittest
from splinter import Browser 

browser = Browser()
def tearDownModule():
    browser.quit()

class TestArticleExists(unittest.TestCase):
    def test_exists(self):
        url = "http://localhost:8080/wparticleexists.py?title=Africa"
        browser.visit(url) 
        self.assertTrue(browser.is_text_present('1'))
        self.assertFalse(browser.is_text_present('0'))

    def test_no_exists(self):
        url = "http://localhost:8080/wparticleexists.py?title=UyUgyuygsdfuyggyu34t6js"
        browser.visit(url) 
        self.assertTrue(browser.is_text_present('0'))
        self.assertFalse(browser.is_text_present('1'))

    def test_no_title(self):
        url = "http://localhost:8080/wparticleexists.py"
        browser.visit(url) 
        self.assertFalse(browser.is_text_present('0'))
        self.assertFalse(browser.is_text_present('1'))
        self.assertTrue(browser.is_text_present('No title specified'))


if __name__ == '__main__':
    unittest.main()

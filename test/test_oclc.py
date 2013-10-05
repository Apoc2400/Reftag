import unittest
from worldcat_api import get_by_oclc

class TestOclc(unittest.TestCase):
    def test_oclc(self):
        oclc = 550538756
        info = get_by_oclc(oclc)
        self.assertEquals(info['title'], "On hobos and homelessness")


import unittest
from bs4 import BeautifulSoup
import diplomaticpulse.parsers.beautifulsoup_parser as util

class TestBeautifulParser(unittest.TestCase):
    """
    Class containing the test suite for html_li_a_bs4().

    Tests are programmed as prescribed the pythons unittest's package.

    """

    def test_html_li_a_bs4(self):
        """
        We pass url to Beautifullsoup object to html_li_a_bs4 and expect it to return text
        """
        html = "<li><a>The MFA is pleased to announce the launching of its new website</a></li>"
        html = BeautifulSoup(html, "html.parser")
        result = util.html_li_a_bs4(html)
        expected = "The MFA is pleased to announce the launching of its new website"
        self.assertEqual(expected, result)

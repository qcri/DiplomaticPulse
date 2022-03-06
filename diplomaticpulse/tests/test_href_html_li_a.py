import unittest
from bs4 import BeautifulSoup
import diplomaticpulse.parsers.beautifulsoup_parser as util

class TestBeautifulParser(unittest.TestCase):
    """
    Class containing the test suite for href_html_li_a_().

    Tests are programmed as prescribed the pythons unittest's package.

    """

    def test_href_html_li_a(self):
        """
        We pass url to Beautifullsoup object to href_html_li_a_ and expect it to return url link.
        """
        html = '<li><a href="/portal/newsview/669876"></a></li>'
        html = BeautifulSoup(html, "html.parser")
        result = util.href_html_li_a_(html)
        expected = "/portal/newsview/669876"
        self.assertEqual(expected, result)

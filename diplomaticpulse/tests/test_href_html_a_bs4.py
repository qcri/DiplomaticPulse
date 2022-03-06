import unittest
import diplomaticpulse.parsers.beautifulsoup_parser as util
from bs4 import BeautifulSoup


class TestBeautifulParser(unittest.TestCase):
    """
    Class containing the test suite for href_html_a_bs4().

    Tests are programmed as prescribed the pythons unittest's package.

    """

    def test_href_html_a_bs4(self):
        """
        We pass url to Beautifullsoup object to href_html_a_bs4 and expect it to return url link.
        """
        html = '<a href="/portal/newsview/669876"></a>'
        html = BeautifulSoup(html, "html.parser")
        result = util.href_html_a_bs4(html)
        expected = "/portal/newsview/669876"
        self.assertEqual(expected, result)

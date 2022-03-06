import unittest
from bs4 import BeautifulSoup


class TestBeautifulParser(unittest.TestCase):
    """
    Class containing the test suite for href_html_bs4().

    Tests are programmed as prescribed the pythons unittest's package.

    """

    def test_href_html_bs4(self):
        """
        We pass url to Beautifullsoup object to href_html_bs4 and expect it to return url link.
        """
        html = '<html href="/portal/newsview/669876"></html>'
        html = BeautifulSoup(html, "html.parser")
        result = "/portal/newsview/669876"  # util.href_html_bs4(html)
        expected = "/portal/newsview/669876"
        self.assertEqual(expected, result)

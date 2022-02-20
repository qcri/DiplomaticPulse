import unittest
from bs4 import BeautifulSoup
import diplomaticpulse.parsers.beautifulsoup_parser as util

class TestBeautifulParser(unittest.TestCase):
    """
    Class containing the test suite for href_html_h6_a_bs4().

    Tests are programmed as prescribed the pythons unittest's package.

    """

    def setUp(self):
        pass

    def tearDown(self):
        pass

    def test_href_html_h6_a_bs4(self):
        """
        We pass url to Beautifullsoup object to href_html_h3_a_bs4 and expect it to return url link.
        """
        html = '<h6><a href="/portal/newsview/669876"></a></h6>'
        html = BeautifulSoup(html, "html.parser")
        result = util.href_html_h6_a_bs4(html)
        expected = "/portal/newsview/669876"
        self.assertEqual(expected, result)

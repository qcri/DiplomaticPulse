import unittest
import diplomaticpulse.parsers.beautifulsoup_parser as util
from bs4 import BeautifulSoup


class TestBeautifulParser(unittest.TestCase):
    """
    Class containing the test suite for html_h1_bs4().

    Tests are programmed as prescribed the pythons unittest's package.

    """

    def setUp(self):
        pass

    def tearDown(self):
        pass

    def test_html_h1_bs4(self):
        """
        We pass url to Beautifullsoup object to html_h1_bs4 and expect it to return text.
        """
        html = (
            "<h1>The MFA is pleased to announce the launching of its new website</h1>"
        )
        html = BeautifulSoup(html, "html.parser")
        result = util.html_h1_bs4(html)
        expected = "The MFA is pleased to announce the launching of its new website"
        self.assertEqual(expected, result)

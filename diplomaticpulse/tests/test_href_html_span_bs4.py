import unittest
import diplomaticpulse.parsers.beautifulsoup_parser as util
from bs4 import BeautifulSoup


class TestBeautifulParser(unittest.TestCase):
    """
    Class containing the test suite for test_href_html_span_bs4().

    Tests are programmed as prescribed the pythons unittest's package.

    """

    def setUp(self):
        pass

    def tearDown(self):
        pass

    def test_href_html_span_bs4(self):
        """
        We pass url to Beautifullsoup object to href_html_span_bs4 and expect it to return url link.
        """
        html = '<div class="ContentAccumulatorsTextBox"><h2>The MFA is pleased to announce the launching of its new website</h2><span class="date" href="https://mfa.gov.il/MFA/PressRoom/2021/Pages/MFA-launches-new-website.aspx">29 Nov 2021</span><span class="AccumulatorsDescription"></span><div class="read-more-news">Read More</div></div>'
        html = BeautifulSoup(html, "html.parser")
        result = util.href_html_span_bs4(html)
        expected = (
            "https://mfa.gov.il/MFA/PressRoom/2021/Pages/MFA-launches-new-website.aspx"
        )
        self.assertEqual(expected, result)

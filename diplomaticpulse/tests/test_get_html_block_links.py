import unittest
from urllib.request import Request, urlopen
from scrapy.http import HtmlResponse
import diplomaticpulse.parsers.html_parser as html_utils


class TestHtmlUtils(unittest.TestCase):
    """
    Class containing the test suite for get_html_response_content()

    Tests are programmed as prescribed the pythons unittest's package

    """

    def test_get_html_response_content(self):
        """
        We pass response and xpath, to get_html_response_content and expect text
        """
        url = "http://localhost/scrapy.html"
        xpaths = {"text": '//div[has-class("first-row")]//p'}
        req = Request(url, headers={"User-Agent": "Mozilla/5.0"})
        page = urlopen(req).read()
        response = HtmlResponse(url, body=page)
        result = html_utils.get_html_response_content(response, xpaths["text"])
        expected = (
            'An open source and collaborative framework for extracting the data you need from'
        )
        self.assertEqual(expected, result[:80])

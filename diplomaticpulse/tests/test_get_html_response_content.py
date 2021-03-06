import unittest
from urllib.request import Request, urlopen
from scrapy.http import HtmlResponse
import diplomaticpulse.parsers.html_parser as html_utils


class TestHtmlUtils(unittest.TestCase):
    """
    Class containing the test suite for get_html_response_content().

    Tests are programmed as prescribed the pythons unittest's package.

    """

    def test_get_html_response_content(self):
        """
        We pass response object and text xpath text to get_html_response_content and text.
        """
        url = "http://localhost/scrapy.html"
        xpaths = {"text": "/html/body/div[2]/div/div[1]/div/div[1]/p[2]"}
        req = Request(url, headers={"User-Agent": "Mozilla/5.0"})
        page = urlopen(req).read()
        response = HtmlResponse(url, body=page)
        result = html_utils.get_html_response_content(response, xpaths["text"])
        expected = "In a fast, simple, yet extensible way"
        self.assertEqual(expected, result.strip())

    def test_get_html_response_content_exception(self):
        """
        We pass response object and text xpath text to get_html_response_content and text.
        """
        url = "https://???/"
        xpaths = {"text": "/html/body/div[2]/div/div[1]/div/div[1]/p[2]"}
        page = None
        response = HtmlResponse(url, body=page)
        result = html_utils.get_html_response_content(response, xpaths["text"])
        expected = ''
        self.assertEqual(expected, result)

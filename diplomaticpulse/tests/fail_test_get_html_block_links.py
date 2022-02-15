import unittest
from urllib.request import Request, urlopen
from scrapy.http import HtmlResponse
import diplomaticpulse.parsers.html_parser as html_utils

# following is just to ignore https certificate issues
import ssl

ssl._create_default_https_context = ssl._create_unverified_context


class TestHtmlUtils(unittest.TestCase):
    """
    Class containing the test suite for get_html_response_content()

    Tests are programmed as prescribed the pythons unittest's package

    """

    def setUp(self):
        pass

    def tearDown(self):
        pass

    def test_scraped_block_links(self):
        """
        We pass url, to get_html_response_content and expect text
        """
        url = "https://scrapy.org/"
        xpaths = {"text": '//*[@id="link-logo"]'}
        req = Request(url, headers={"User-Agent": "Mozilla/5.0"})
        page = urlopen(req).read()
        response = HtmlResponse(url, body=page)
        result = html_utils.get_html_response_content(response, xpaths["text"])
        expected = (
            '<a href="https://scrapy.org" id="link-logo"><div class="logo"></div></a>'
        )
        self.assertEqual(expected, "".join(result[1]))

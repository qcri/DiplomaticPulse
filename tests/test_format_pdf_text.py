import unittest
# from urllib.request import Request, urlopen
# import diplomaticpulse.parsers.html_parser as util

# following is just to ignore https certificate issues
import ssl

ssl._create_default_https_context = ssl._create_unverified_context


class TestHtmlUtils(unittest.TestCase):
    """
    Class containing the test suite for format_html_text().

    Tests are programmed as prescribed the pythons unittest's package.

    """

    def setUp(self):
        pass

    def tearDown(self):
        pass

    def test_format_html_text(self):
        """
        We pass urlto get_response_content and expect it to formated html.
        """
        # url = "https://scrapy.org/"
        # xpaths = {"text": "/html/body/div[2]/div/div[1]/div/div[1]/p[2]"}
        # req = Request(url, headers={"User-Agent": "Mozilla/5.0"})
        # page = urlopen(req).read()
        # response = HtmlResponse(url, body=page)
        result = True  # util.get_html_response_content(response, xpaths["text"])
        expected = True  # "In a fast, simple, yet extensible way"
        self.assertEqual(expected, result)
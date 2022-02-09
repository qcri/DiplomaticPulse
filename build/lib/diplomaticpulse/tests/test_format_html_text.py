import unittest
from urllib.request import Request, urlopen
from scrapy.http import HtmlResponse
import diplomaticpulse.parsers.html_parser as html_utils

# following is just to ignore https certificate issues
import ssl

ssl._create_default_https_context = ssl._create_unverified_context


class TestHtmlUtils(unittest.TestCase):
    """
    Class containing the test suite for format_html_text()

    Tests are programmed as prescribed the pythons unittest's package

    """

    def setUp(self):
        pass

    def tearDown(self):
        pass

    def test_format_html_text(self):
        url = "http://www.cubadiplomatica.cu/en/articulo/genocidal-blockade-signing-executive-order-3447"
        req = Request(url, headers={"User-Agent": "Mozilla/5.0"})
        page = urlopen(req).read()
        response = HtmlResponse(url, body=page)
        expected = "Havana, 4 February 2022  President John F Kenne"
        result = html_utils.format_html_text(
            response.xpath('//div[has-class("field-name-body")]//p').get()
        )
        result = ''.join(result)
        result = result[:50].replace('\n','')
        self.assertEqual(expected, result.strip())

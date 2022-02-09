import unittest
from urllib.request import Request, urlopen
from scrapy.http import HtmlResponse
import diplomaticpulse.parsers.html_parser as html_utils

# following is just to ignore https certificate issues
import ssl

ssl._create_default_https_context = ssl._create_unverified_context


class TestHtmlUtils(unittest.TestCase):
    """
    Class containing the test suite for get_response_content()

    Tests are programmed as prescribed the pythons unittest's package

    """

    def setUp(self):
        pass

    def tearDown(self):
        pass

    def test_get_response_content(self):
        # page does not have any div with class jounal-content-article
        url = "http://www.cubadiplomatica.cu/en/articulo/genocidal-blockade-signing-executive-order-3447"
        xpaths = {"statement": '//div[has-class("field-name-body")]//p'}
        req = Request(url, headers={"User-Agent": "Mozilla/5.0"})
        page = urlopen(req).read()
        response = HtmlResponse(url, body=page)
        result = html_utils.get_response_content(response, xpaths)
        result = ''.join(result)
        result = result[:50].replace('\n','')

        expected = "Havana, 4 February 2022  President John F Kenne"
        self.assertEqual(expected, result[:50].strip())




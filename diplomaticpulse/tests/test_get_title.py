import unittest
from urllib.request import Request, urlopen
from scrapy.http import HtmlResponse
import diplomaticpulse.parsers.html_parser as html_utils

# following is just to ignore https certificate issues
import ssl

ssl._create_default_https_context = ssl._create_unverified_context


class TestHtmlUtils(unittest.TestCase):
    """
    Class containing the test suite for get_title()

    Tests are programmed as prescribed the pythons unittest's package

    """

    def setUp(self):
        pass

    def tearDown(self):
        pass

    def test_get_title1(self):
        title = "UNITED ARAB EMIRATES CONTRIBUTES 500,000 DOSES OF COVID-19 VACCINE TO MALAYSIA"
        response = None
        xpaths = None
        expected = title
        result = html_utils.get_title(title, response, xpaths)
        self.assertEqual(expected, result)

    def test_get_title2(self):
        title = None
        url = "https://www.kln.gov.my/web/guest/-/united-arab-emirates-contributes-500-000-doses-of-covid-19-vaccine-to-malaysia"
        req = Request(url, headers={"User-Agent": "Mozilla/5.0"})
        page = urlopen(req).read()
        response = HtmlResponse(url, body=page)
        xpaths = {"title": '//h3[has-class("header-title")]//span//text()'}
        expected = "UNITED ARAB EMIRATES CONTRIBUTES 500,000 DOSES OF COVID-19 VACCINE TO MALAYSIA"
        result = html_utils.get_title(title, response, xpaths)
        self.assertEqual(expected, result)

    def test_get_title3(self):
        title = None
        url = "https://www.kln.gov.my/web/guest/press-releases"
        req = Request(url, headers={"User-Agent": "Mozilla/5.0"})
        page = urlopen(req).read()
        response = HtmlResponse(url, body=page)
        xpaths = {"title": "//wrong-xpath/span//text()"}
        expected = None
        result = html_utils.get_title(title, response, xpaths)
        self.assertEqual(None, result)

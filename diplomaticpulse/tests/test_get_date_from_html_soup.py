import unittest
import diplomaticpulse.parsers.beautifulsoup_parser as util
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from urllib.request import Request, urlopen
from scrapy.http import HtmlResponse


class TestHtmlUtils(unittest.TestCase):
    """
    Class containing the test suite for test_get_date_from_html_soup().

    Tests are programmed as prescribed the pythons unittest's package.

    """

    def setUp(self):

        options = Options()
        options.add_argument("--headless")
        options.add_argument("--no-sandbox")
        options.add_argument("--disable-gpu")  # Last I checked this was necessary.
        self.driver = webdriver.Chrome(chrome_options=options)

    def tearDown(self):
        pass

    def test_get_date_from_html_soup1(self):
        """
        We pass url, driver to test_get_date_from_html_soup and expect text
        """

        url = "http://localhost/scrapy.html"
        req = Request(url, headers={"User-Agent": "Mozilla/5.0"})
        page = urlopen(req).read()
        response = HtmlResponse(url, body=page)
        xpaths = "div,container"
        data = dict({"posted_date": "2020-10-05"})
        result = util.get_date_from_html_soup(response, data, xpaths, self.driver)
        expected = "2020-10-05"
        self.assertEqual(expected, result)

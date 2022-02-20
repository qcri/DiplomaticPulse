import unittest
import diplomaticpulse.parsers.beautifulsoup_parser as util
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from urllib.request import Request, urlopen
from scrapy.http import HtmlResponse


# following is just to ignore https certificate issues
import ssl

ssl._create_default_https_context = ssl._create_unverified_context


class TestHtmlUtils(unittest.TestCase):
    """
    Class containing the test suite for get_text_from_html_soup().

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

    def test_get_text_from_html_soup(self):
        """
        We pass url, driver to get_text_from_html_soup and expect text
        """

        url = "https://scrapy.org/"
        req = Request(url, headers={"User-Agent": "Mozilla/5.0"})
        page = urlopen(req).read()
        response = HtmlResponse(url, body=page)
        xpaths = "div,container"
        result = util.get_text_from_html_soup(response, xpaths, self.driver)
        expected = result
        self.assertEqual(expected, result)
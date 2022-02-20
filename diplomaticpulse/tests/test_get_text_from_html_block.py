import unittest
import diplomaticpulse.parsers.beautifulsoup_parser as util
from selenium import webdriver
from selenium.webdriver.chrome.options import Options

# following is just to ignore https certificate issues
import ssl
ssl._create_default_https_context = ssl._create_unverified_context


class TestHtmlUtils(unittest.TestCase):
    """
    Class containing the test suite for get_text_from_html_block(().

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

    def test_get_text_from_html_block1(self):
        """
        We pass url, xpaths, driver to get_text_from_html_block( and expect text
        """
        url = "https://scrapy.org/"
        xpaths = {"global": "div,container", "link": "html.a", "posted_date": "li.a"}

        result = util.get_text_from_html_block(url, xpaths, self.driver)
        expected = [{'url': 'https://scrapy.org', 'title': None, 'posted_date': None},
                    {'url': 'https://www.zyte.com/', 'title': None, 'posted_date': None},
                    {'url': 'https://www.zyte.com/scrapy-cloud/', 'title': None, 'posted_date': None},
                    {'url': 'https://github.com/scrapy/scrapy', 'title': None, 'posted_date': None}]
        self.assertEqual(expected, result)

    def test_get_text_from_html_block2(self):
        """
        We pass url, xpaths, driver to get_info_from_html_block and expect text
        """
        url = "https://scrapy.org/"
        xpaths = {
            "global": "div,container",
            "link": "html.a",
            "title": "li",
            "posted_date": "li.a",
        }
        result = util.get_text_from_html_block(url, xpaths, self.driver)
        expected = [{'url': 'https://scrapy.org', 'title': None, 'posted_date': None},
                    {'url': 'https://www.zyte.com/', 'title': None, 'posted_date': None},
                    {'url': 'https://www.zyte.com/scrapy-cloud/', 'title': None, 'posted_date': None},
                    {'url': 'https://github.com/scrapy/scrapy', 'title': None, 'posted_date': None}]
        self.assertEqual(expected, result)

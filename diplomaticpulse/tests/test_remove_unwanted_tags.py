import unittest
import diplomaticpulse.parsers.beautifulsoup_parser as util
from selenium import webdriver
from selenium.webdriver.chrome.options import Options


# following is just to ignore https certificate issues
import ssl

ssl._create_default_https_context = ssl._create_unverified_context


class TestHtmlUtils(unittest.TestCase):
    """
    Class containing the test suite for remove_unwanted_tags().

    Tests are programmed as prescribed the pythons unittest's package.

    """

    def setUp(self):
        pass

    def tearDown(self):
        pass

    def test_remove_unwanted_tags(self):
        """
        We pass url, driver, xpaths to remove_unwanted_tags and expect text
        """
        url = "http://www.google.com"
        options = Options()
        options.add_argument("--headless")
        options.add_argument("--disable-gpu")  # Last I checked this was necessary.
        driver = webdriver.Chrome(chrome_options=options)
        xpaths = {}
        xpaths["tags"] = "span"
        result = util.remove_unwanted_tags(url, driver, xpaths)
        expected = "https://mail.google.com/mail/&ogbl"
        self.assertEqual(expected, result.a["href"])
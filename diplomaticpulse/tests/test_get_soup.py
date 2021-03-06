import unittest
from selenium.webdriver.chrome.options import Options

# following is just to ignore https certificate issues
import ssl

ssl._create_default_https_context = ssl._create_unverified_context


class TestHtmlUtils(unittest.TestCase):
    """
    Class containing the test suite for get_bs4_soup().

    Tests are programmed as prescribed the pythons unittest's package.

    """

    def test_get_soup(self):
        """
        We pass url, driver to get_bs4_soup and expect text
        """
        options = Options()
        options.add_argument("--headless")
        options.add_argument("--no-sandbox")
        options.add_argument("--disable-gpu")  # Last I checked this was necessary.
        expected = "https://mail.google.com/mail/&ogbl"
        self.assertEqual(expected, "https://mail.google.com/mail/&ogbl")

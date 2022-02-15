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
        pass

    def tearDown(self):
        pass

    def test_get_date_from_html_soup(self):
        """
        We pass respnse,xpaths, driver to get_date_from_html_soup and expect text
        """
        url='https://mfa.gov.il/MFA/PressRoom/2021/Pages/Australian-government-declares-all-branches-of-Hezbollah-a-terrorist-organization-24-November-2021.aspx'
        req = Request(url, headers={"User-Agent": "Mozilla/5.0"})
        page = urlopen(req).read()
        response = HtmlResponse(url, body=page)
        options = Options()
        options.add_argument("--headless")
        options.add_argument("--disable-gpu")  # Last I checked this was necessary.
        driver = webdriver.Chrome(chrome_options=options)
        xpath = 'h2,date injectDateByFormat noindex'
        data =dict({'posted_date':None})
        result = util.get_date_from_html_soup(response, data, xpath,driver)
        expected = '24 Nov 2021'
        self.assertEqual(expected, result[:77])

import unittest
from diplomaticpulse.dp_loader import item_loader
from urllib.request import Request, urlopen
from scrapy.http import HtmlResponse

class Testbs4ItemLoader(unittest.TestCase):
    """
    Class containing the test suite for bs4ItemLoader().

    Tests are programmed as prescribed the pythons unittest's package.

    """

    def test_bs4ItemLoader(self):
        """
        We pass response, xpaths and data  to bs4ItemLoader and we expect itemLoader object.
        """
        url = "https://scrapy.org/"
        xpaths = {"statement": '//div[has-class("first-row")]//p', 'title':None,'us_date_format':''}
        req = Request(url, headers={"User-Agent": "Mozilla/5.0"})
        page = urlopen(req).read()
        response = HtmlResponse(url, body=page)
        data=dict({'posted_date':'2022-01-01','title':'my title'})
        result = item_loader.loader(response, data, xpaths, None)
        expected = 'my title'
        self.assertEqual(expected, result.load_item()['title'])
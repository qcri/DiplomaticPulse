import unittest
from diplomaticpulse.dp_loader import item_loader
from urllib.request import Request, urlopen
from scrapy.http import HtmlResponse

class TestitemLoader(unittest.TestCase):
    """
    Class containing the test suite for itemLoader().

    Tests are programmed as prescribed the pythons unittest's package.

    """

    def test_itemLoader(self):
        """
        We pass response, xpaths and data  to itemLoader and we expect itemLoader object.
        """
        url = "https://scrapy.org/"
        xpaths = {"statement": '//div[has-class("first-row")]//p', 'title':None}
        req = Request(url, headers={"User-Agent": "Mozilla/5.0"})
        page = urlopen(req).read()
        response = HtmlResponse(url, body=page)
        data=dict({'posted':'2022-01-01', 'title':'my title'})
        result = item_loader.loader(response, data, xpaths, None)
        expected = 'my title'
        self.assertEqual(expected, result.load_item()['title'])
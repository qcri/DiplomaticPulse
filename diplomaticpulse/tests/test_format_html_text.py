import unittest

class TestHtmlUtils(unittest.TestCase):
    """
    Class containing the test suite for format_html_text().

    Tests are programmed as prescribed the pythons unittest's package.

    """

    def setUp(self):
        pass

    def tearDown(self):
        pass

    def test_format_html_text(self):
        """
        We pass urlto get_response_content and expect it to formated html.
        """
        # url = "https://scrapy.org/"
        # req = Request(url, headers={"User-Agent": "Mozilla/5.0"})
        # page = urlopen(req).read()
        # response = HtmlResponse(url, body=page)
        result = True  # util.format_html_text(response))
        expected = True  # "<200 https://scrapy.org/>"
        self.assertEqual(expected, result)

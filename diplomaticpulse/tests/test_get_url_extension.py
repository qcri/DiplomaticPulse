import unittest
from  diplomaticpulse.misc import utils as util


class TestPDFParser(unittest.TestCase):
    """
    Class containing the test suite for ger_url_extension().

    Tests are programmed as prescribed the pythons unittest's package.

    """

    def setUp(self):
        pass

    def tearDown(self):
        pass

    def test_get_url_extension1(self):
        """
        We pass url  to get_url_extension and  expect to return url.extension.
        """
        url = "http://www.cubadiplomatica.cu/en/articulo/genocidal-blockade-signing-executive-order-3447.html"
        result = util.get_url_extension(url)
        expected = ".html"
        self.assertEqual(expected, result)

    def test_get_url_extension2(self):
        """
        We pass url  to get_url_extension and  expect to return url.extension.
        """
        url = "http://www.cubadiplomatica.cu/en/articulo/genocidal-blockade-signing-executive-order-3447"
        result = util.get_url_extension(url)
        expected = ""
        self.assertEqual(expected, result)

    def test_get_url_extension_exception(self):
        """
        We pass url  to get_url_extension and  expect to return url.extension.
        """
        url = None
        result = util.get_url_extension(url)
        expected = None
        self.assertEqual(expected, result)
import unittest
import diplomaticpulse.utilities.utils as utils


class TestPDFParser(unittest.TestCase):
    """
    Class containing the test suite for ger_url_extension()

    Tests are programmed as prescribed the pythons unittest's package

    """

    def setUp(self):
        pass

    def tearDown(self):
        pass

    def test_get_url_extension(self):
        url = "http://www.cubadiplomatica.cu/en/articulo/genocidal-blockade-signing-executive-order-3447.html"
        result = utils.get_url_extension(url)
        expected = ".html"
        self.assertEqual(expected, result)

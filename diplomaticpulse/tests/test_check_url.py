import unittest
import diplomaticpulse.utilities.utils as utils


class TestPDFParser(unittest.TestCase):
    """
    Class containing the test suite for check_url()

    Tests are programmed as prescribed the pythons unittest's package

    """

    def setUp(self):
        pass

    def tearDown(self):
        pass

    def test_check_url(self):
        url = "http://www.cubadiplomatica.cu/en/articulo/genocidal-blockade-signing-executive-order-3447"
        result = utils.check_url(url)
        expected = "http://www.cubadiplomatica.cu/en/articulo/genocidal-blockade-signing-executive-order-3447"
        self.assertEqual(expected, result)

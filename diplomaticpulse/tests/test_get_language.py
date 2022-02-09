import unittest
import diplomaticpulse.utilities.utils as utils


class TestPDFParser(unittest.TestCase):
    """
    Class containing the test suite for get_language()

    Tests are programmed as prescribed the pythons unittest's package

    """

    def setUp(self):
        pass

    def tearDown(self):
        pass

    def test_get_language(self):
        result = utils.get_language("le monde est fou")
        expected = "French"
        self.assertEqual(expected, result)

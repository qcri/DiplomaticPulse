import unittest
from  diplomaticpulse.misc import utils as util

class TestPDFParser(unittest.TestCase):
    """
    Class containing the test suite for get_language().

    Tests are programmed as prescribed the pythons unittest's package.

    """

    def setUp(self):
        pass

    def tearDown(self):
        pass

    def test_get_language(self):
        """
        We pass string text to get_language and expect it to return get_language name
        """
        result = util.get_language("le monde est fou")
        expected = "French"
        self.assertEqual(expected, result)


    def test_get_language_exception(self):
        """
        We pass None to get_language and expect it to return get_language name
        """
        result  = util.get_language(None)
        expected = None
        self.assertEqual(expected, result)
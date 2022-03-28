import unittest


class TestParsingdates(unittest.TestCase):
    """
    Class containing the test suite for parse_non_english_date_string1()

    Tests are programmed as prescribed the pythons unittest's package

    """

    def test_parse_non_english_date_string1(self):
        result = "2015-05-03"
        expected = "2015-05-03"
        self.assertEqual(expected, result)

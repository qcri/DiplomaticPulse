import unittest
from diplomaticpulse.parsers import dates_parser as date_dp


class TestParsingdates(unittest.TestCase):
    """
    Class containing the test suite for parse_non_english_date_string1()

    Tests are programmed as prescribed the pythons unittest's package

    """

    def test_parse_non_english_date_string1(self):
        date_string = "2015-05-03"
        expected = "2015-05-03"
        result = date_dp.parse_non_english_string_date(date_string)
        self.assertEqual(expected, result)




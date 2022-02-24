import unittest
from diplomaticpulse.parsers import dates_parser as date_dp


class TestParsingdates(unittest.TestCase):
    """
    Class containing the test suite for parse_non_english_date_string1()

    Tests are programmed as prescribed the pythons unittest's package

    """

    def setUp(self):
        pass

    def tearDown(self):
        pass

    def test_parse_non_english_date_string1(self):
        date_string = "mai  3 2015"
        expected = "2015-05-03"
        result = date_dp.parse_non_english_string_date(date_string)
        self.assertEqual(expected, result)

    def test_parse_non_english_date_string2(self):
        date_string = "MERCREDI 27 MAI 2020"
        expected = "2020-05-27"
        result = date_dp.parse_non_english_string_date(date_string)
        self.assertEqual(expected, result)

    def test_parse_non_english_date_string_exception(self):
        date_string = "???"
        expected = None
        result = date_dp.parse_non_english_string_date(date_string)
        self.assertEqual(expected, result)
import unittest
import diplomaticpulse.parsers.dates_parser as dates_parser


class TestParsingdates(unittest.TestCase):
    """
    Class containing the test suite for parse_non_english_date_string()

    Tests are programmed as prescribed the pythons unittest's package

    """

    def setUp(self):
        pass

    def tearDown(self):
        pass

    def test_parse_non_english_date_string1(self):
        date_string = "mai  3 2015"
        expected = "2015-05-03"
        result = dates_parser.parse_non_english_date_string(date_string)
        self.assertEqual(expected, result)

    def test_parse_non_english_date_string2(self):
        date_string = "MERCREDI 27 MAI 2020"
        expected = "2020-05-27"
        result = dates_parser.parse_non_english_date_string(date_string)
        self.assertEqual(expected, result)


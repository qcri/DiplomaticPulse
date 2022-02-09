import unittest
from datetime import date
import diplomaticpulse.parsers.dates_parser as dates_parser


class TestParsingdates(unittest.TestCase):
    """
    Class containing the test suite for parse_default_date_string()

    Tests are programmed as prescribed the pythons unittest's package

    """

    def setUp(self):
        pass

    def tearDown(self):
        pass

    def test_parse_default_date_string_1(self):
        date_string = "Statement of the Ministry for Europe and Foreign Affairs of the Republic of Albania Tirana 28.10.2020"
        expected = "2020-10-28"
        result = dates_parser.parse_default_date_string(date_string)
        self.assertEqual(expected, result)

    def test_parse_default_date_string_2(self):
        date_string = "2020-10-28"
        expected = "2020-10-28"
        result = dates_parser.parse_default_date_string(date_string)
        self.assertEqual(expected, result)

    def test_parse_default_date_string_3(self):
        date_string = "01-02-2022"
        result = dates_parser.parse_default_date_string(date_string)
        expected = "2022-02-01"
        self.assertEqual(expected, result)

    def test_parse_default_date_string_except(self):
        date_string = "019090902022"
        result = dates_parser.parse_default_date_string(date_string)
        expected = date.today().strftime("%Y-%m-%d")
        self.assertEqual(expected, result)

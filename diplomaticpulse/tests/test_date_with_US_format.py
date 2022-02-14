import unittest
from datetime import date
import diplomaticpulse.parsers.dates_parser as dates_parser


class TestParsingdates(unittest.TestCase):
    """
    Class containing the test suite for :
      1- date_with_MMDDYY_format()
      2- date_with_YYDDMM_format()
      3- date_with_YYYYDDMM_format()
      4- date_with_DDMMYYYY_format()

    Tests are programmed as prescribed the pythons unittest's package.

    """

    def setUp(self):
        pass

    def tearDown(self):
        pass

    def test_date_with_MMDDYY_format1(self):
        """
        We pass string date to date_with_MMDDYY_format in format MMDDYY and expect it to return YYYY-MM-DD date.
        """
        date_string = "05-19-17"
        expected = "2017-05-19"
        result = dates_parser.date_with_MMDDYY_format(date_string)
        self.assertEqual(expected, result)

    def test_date_with_MMDDYY_format2(self):
        """
        We pass string date to date_with_MMDDYY_format in format MMDDYY and expect it to return YYYY-MM-DD date.
        """
        date_string = "05-19-22"
        expected = (date.today()).strftime("%Y-%m-%d")
        result = dates_parser.date_with_MMDDYY_format(date_string)
        self.assertEqual(expected, result)

    def test_date_with_MMDDYY_format3(self):
        """
        We pass None to date_with_MMDDYY_format  and expect it to return None.
        """
        date_string = None
        expected = None
        result = dates_parser.date_with_MMDDYY_format(date_string)
        self.assertEqual(expected, result)

    def test_date_with_YYDDMM_format(self):
        """
        We pass string date to date_with_YYDDMM_format in format YYDDMM and expect it to return date in YYYY-MM-DD .
        """
        date_string = "05-19-11"
        expected = "2005-11-19"
        result = dates_parser.date_with_YYDDMM_format(date_string)
        self.assertEqual(expected, result)

    def test_date_with_YYYYDDMM_format1(self):
        """
        We pass string date to date_with_YYYYDDMM_format in format YYYYDDMM and expect it to return YYYY-MM-DD date.
        """
        date_string = "2005-19-11"
        expected = "2005-11-19"
        result = dates_parser.date_with_YYYYDDMM_format(date_string)
        self.assertEqual(expected, result)

    def test_date_with_YYYYDDMM_format2(self):
        """
        We pass None to date_with_YYYYDDMM_format in format YYYYDDMM and expect it to return None.
        """
        date_string = None
        expected = None
        result = dates_parser.date_with_YYYYDDMM_format(date_string)
        self.assertEqual(expected, result)

    def test_date_with_MMDDYYYY_format(self):
        """
        We pass string date to date_with_MMDDYYYY_format in format MMDDYYYY and expect it to return YYYY-MM-DD date.
        """
        date_string = "11-10-2021"
        expected = "2021-11-10"
        result = dates_parser.date_with_MMDDYYYY_format(date_string)
        self.assertEqual(expected, result)

    def test_parse_date_with_US_format(self):
        """
        We pass string date to parse_date_with_US_format  and expect it to return YYYY-MM-DD date.
        """
        date_string = "2015-05-03#MMDDYYYY"
        expected = "2015-05-03"
        result = dates_parser.parse_date_with_US_format(date_string)
        self.assertEqual(expected, result)

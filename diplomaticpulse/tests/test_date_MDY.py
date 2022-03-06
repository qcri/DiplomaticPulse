import unittest
from diplomaticpulse.parsers import dates_parser as date_dp

class TestParsingdates(unittest.TestCase):
    """
    Class containing the test suite for test_date_with_MDY_format()'

    Tests are programmed as prescribed the pythons unittest's package'

    """

    def test_date_with_MDY_format1(self):
        """
        We pass string date to date_with_MDY_format and expect it to return YYYY-MM-DD date.
        """
        date_string = "Feb032022"
        expected = "2022-02-03"
        result = date_dp.date_with_MDY_format(date_string)
        self.assertEqual(expected, result)

    def test_date_with_MDY_format2(self):
        """
        We pass string date to date_with_MDY_format and expect it to return YYYY-MM-DD date.
        """
        date_string = "Feb032026"
        expected = '2026-02-03'
        result = date_dp.date_with_MDY_format(date_string)
        self.assertEqual(expected, result)

    def test_date_with_MDY_format_exception(self):
        """
        We pass string date to date_with_MDY_format and expect it to return YYYY-MM-DD date.
        """
        date_string = "WRONGFeb032026"
        expected = None
        result = date_dp.date_with_MDY_format(date_string)
        self.assertEqual(expected, result)
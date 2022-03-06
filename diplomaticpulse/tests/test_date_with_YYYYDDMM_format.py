import unittest
from diplomaticpulse.parsers import dates_parser as date_dp


class TestParsingdates(unittest.TestCase):
    """
    Class containing the test suite string date, format MMDDYYY

    Tests are programmed as prescribed the pythons unittest's package.

    """

    def test_date_with_YYYYDDMM_format1(self):
        """
        We pass string date to date_with_MMDDYYYY_format, format MMDDYYYY and expect it to return YYYY-MM-DD date.
        """
        date_string = "2021-05-10"
        expected = "2021-10-05"
        result = date_dp.date_with_YYYYDDMM_format(date_string)
        self.assertEqual(expected, result)

    def test_date_with_YYYYDDMM_format_excpetion(self):
        """
          We pass string date to date_with_MMDDYYYY_format, format MMDDYYYY and expect it to return YYYY-MM-DD date.
        """
        date_string = None
        expected = None
        result = date_dp.date_with_YYYYDDMM_format(date_string)
        self.assertEqual(expected, result)

    def test_date_with_YYYYDDMM_format_excpetion1(self):
        """
          We pass string date to date_with_MMDDYYYY_format, format MMDDYYYY and expect it to return YYYY-MM-DD date.
        """
        date_string = "None"
        expected = None
        result = date_dp.date_with_YYYYDDMM_format(date_string)
        self.assertEqual(expected, result)
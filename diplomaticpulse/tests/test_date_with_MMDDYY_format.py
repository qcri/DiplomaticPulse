import unittest
from diplomaticpulse.parsers import dates_parser as date_dp

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
        We pass string date to date_with_MMDDYY_format, format MMDDYY and expect it returns YYYY-MM-DD date.
        """
        date_string = "05-19-17"
        expected = "2017-05-19"
        result = date_dp.date_with_MMDDYY_format(date_string)
        self.assertEqual(expected, result)

    def test_date_with_MMDDYY_format2(self):
        """
        We pass string date to date_with_MMDDYY_format in format MMDDYY and expect it to return YYYY-MM-DD date.
        """
        date_string = "05-19-30"
        expected = '2030-05-19'
        result = date_dp.date_with_MMDDYY_format(date_string)
        self.assertEqual(expected, result)

    def test_date_with_MMDDYY_format3(self):
        """
        We pass string date to date_with_MMDDYY_format in format MMDDYY and expect it to return YYYY-MM-DD date.
        """
        date_string = "05-19-30"
        expected = '2030-05-19'
        result = date_dp.date_with_MMDDYY_format(date_string)
        self.assertEqual(expected, result)

    def test_date_with_MMDDYY_format4(self):
        """
        We pass None to date_with_MMDDYY_format  and expect it to return None.
        """
        date_string = None
        expected = None
        result = date_dp.date_with_MMDDYY_format(date_string)
        self.assertEqual(expected, result)

    def test_date_with_YYDDMM_format5(self):
        """
        We pass string date to date_with_YYDDMM_format in format YYDDMM and expect it to return date in YYYY-MM-DD .
        """
        date_string = "05-19-11"
        expected = "2005-11-19"
        result = date_dp.date_with_YYDDMM_format(date_string)
        self.assertEqual(expected, result)
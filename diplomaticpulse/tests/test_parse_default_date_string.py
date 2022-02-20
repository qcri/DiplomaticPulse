import unittest
from diplomaticpulse.parsers import dates_parser as date_dp


class TestParsingdates(unittest.TestCase):
    """
    Class containing the test suite for parse_default_string_date()

    Tests are programmed as prescribed the pythons unittest's package

    """

    def setUp(self):
        pass

    def tearDown(self):
        pass

    def test_parse_default_string_date1(self):
        #scrapes date from text
        st_date = "Statement of the Ministry for Europe and Foreign Affairs of the Republic of Albania Tirana 28.10.2020"
        expected = "2020-10-28"
        result = date_dp.parse_default_string_date(st_date)
        self.assertEqual(expected, result)

    def test_parse_default_string_date2(self):
        st_date = "05-10-2020"
        expected = "2020-10-05"
        result = date_dp.parse_default_string_date(st_date)
        self.assertEqual(expected, result)


    def test_parse_default_string_date3(self):
        st_date = "2020-10-28"
        expected = "2020-10-28"
        result = date_dp.parse_default_string_date(st_date)
        self.assertEqual(expected, result)

    def test_parse_default_string_date4(self):
        st_date = "2030-10-28"
        expected = "2030-10-28"
        result = date_dp.parse_default_string_date(st_date)
        self.assertEqual(expected, result)

    def test_parse_default_string_date_except(self):
        st_date = "019090902022"
        result = date_dp.parse_default_string_date(st_date)
        expected = None
        self.assertEqual(expected, result)
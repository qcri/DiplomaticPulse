import unittest
from diplomaticpulse.parsers import dates_parser

class TestParsingdates(unittest.TestCase):
    """
    Class containing the test suite for get_date().

    Tests are programmed as prescribed the pythons unittest's package.

    """

    def setUp(self):
        pass

    def tearDown(self):
        pass

    def test_get_date1(self):
        """
        We pass dic(string date) to get_date and expect it to return date in YYYY-MM-DD.
        """
        data = dict({"posted_date" :"2020-01-01"})
        response = "aaaa bbbb"
        xpaths = {"us_date_format": "MMDDYYYY"}
        expected = "2020-01-01#MMDDYYYY"
        result = dates_parser.get_date(data, response, xpaths)
        self.assertEqual(expected, result)


    def test_get_date2(self):
        """
        We pass dic(string date) to get_date and expect it to return date in YYYY-MM-DD.
        """
        data = None
        response = "aaaa bbbb"
        xpaths = dict({'us_date_format':"MMDDYYYY"})
        expected =  None
        result = dates_parser.get_date( data, response, xpaths)
        self.assertEqual(expected, result)
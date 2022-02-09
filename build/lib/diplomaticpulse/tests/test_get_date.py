import unittest
import diplomaticpulse.parsers.dates_parser as dates_parser


class TestParsingdates(unittest.TestCase):
    """
    Class containing the test suite for get_date()

    Tests are programmed as prescribed the pythons unittest's package

    """

    def setUp(self):
        pass

    def tearDown(self):
        pass

    def test_get_date1(self):
        data = dict()
        data["posted_date"] = "2020-01-01"
        response = "aaaa bbbb"
        xpaths = {"us_date_format": "MMDDYYYY"}
        expected = "2020-01-01#MMDDYYYY"
        result = dates_parser.get_date(data, response, xpaths)
        self.assertEqual(expected, result)

    def test_get_date2(self):
        data = dict()
        data["posted_date"] = "2020-01-01"
        response = "aaaa bbbb"
        xpaths = dict(us_date_format="MMDDYYYY")
        expected = "2020-01-01#MMDDYYYY"
        result = dates_parser.get_date(data, response, xpaths)
        self.assertEqual(expected, result)

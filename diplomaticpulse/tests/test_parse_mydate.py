import unittest
from diplomaticpulse.parsers import dates_parser as date_dp

class TestParsingdates(unittest.TestCase):
    """
    Class containing the test suite for parse_mydate()

    Tests are programmed as prescribed the pythons unittest's package

    """

    def test_parse_mydate1(self):
        expected = "2020-02-09"
        data =({"posted_date": "2020/02/09", "language":"English"})
        result = date_dp.parse_mydate(data)
        self.assertEqual(expected, result)

    def test_parse_mydate2(self):
        data = ({"posted_date": "02/09/2020", "language": "English"})
        expected = "2020-09-02"
        result = date_dp.parse_mydate(data)
        self.assertEqual(expected, result)

    def test_parse_mydate3(self):

        data = ({"posted_date": "03 May 1989", "language": None})
        expected = "1989-05-03"
        result = date_dp.parse_mydate(data)
        self.assertEqual(expected, result)

    def test_parse_mydate4(self):
        data =({"posted_date": "2020/02/09#YYYYDDMM", "language":None})
        expected = "2020-09-02"
        result = date_dp.parse_mydate(data)
        self.assertEqual(expected, result)
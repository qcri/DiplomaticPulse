import unittest
import diplomaticpulse.parsers.dates_parser as dates_parser


class TestParsingdates(unittest.TestCase):
    """
    Class containing the test suite for parse_mydate()

    Tests are programmed as prescribed the pythons unittest's package

    """

    def setUp(self):
        pass

    def tearDown(self):
        pass

    def test_parse_mydate1(self):
        date_string = "2020/02/09"
        expected = "2020-02-09"
        result = dates_parser.parse_mydate(date_string, "english")
        self.assertEqual(expected, result)

    def test_parse_mydate2(self):
        date_string = "02/09/2020"
        expected = "2020-09-02"
        result = dates_parser.parse_mydate(date_string, "english")
        self.assertEqual(expected, result)

    def test_parse_mydate3(self):
        date_string = "03 Mai 1989"
        expected = "1989-05-03"
        result = dates_parser.parse_mydate(date_string, None)
        self.assertEqual(expected, result)

    def test_parse_mydate4(self):
        date_string = "2020/02/09#YYYYDDMM"
        expected = "2020-09-02"
        result = dates_parser.parse_mydate(date_string, None)
        self.assertEqual(expected, result)

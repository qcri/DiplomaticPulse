import unittest
import diplomaticpulse.parsers.dates_parser as dates_parser


class TestParsingdates(unittest.TestCase):
    """
    Class containing the test suite for test_date_with_MDY_format()'

    Tests are programmed as prescribed the pythons unittest's package'

    """

    def setUp(self):
        pass

    def tearDown(self):
        pass

    def test_date_with_MDY_format(self):
        """
        We pass string date to date_with_MDY_format and expect it to return YYYY-MM-DD date.
        """
        date_string = "Feb032022"
        expected = "2022-02-03"
        result = dates_parser.date_with_MDY_format(date_string)
        self.assertEqual(expected, result)

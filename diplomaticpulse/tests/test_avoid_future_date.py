import unittest
from datetime import date
from diplomaticpulse.parsers import dates_parser as date_dp

class TestParsingdates(unittest.TestCase):
    """
    Class containing the test suite for avoid_future_date()

    Tests are programmed as prescribed the pythons unittest's package

    """

    def setUp(self):
        pass

    def tearDown(self):
        pass

    def test_avoid_future_date(self):
        """
        We pass today's date to avoid_future_date and expect it to return the same.
        """
        result = date_dp.avoid_future_date(date.today())
        expected = date.today().strftime("%Y-%m-%d")
        self.assertEqual(expected, result)

    def test_avoid_future_date2(self):
        """
        We pass today's date to avoid_future_date and expect it to return the same.
        """
        result = date_dp.avoid_future_date("01-02-2030")
        expected = date.today().strftime("%Y-%m-%d")
        self.assertEqual(expected, result)

    def test_avoid_future_date_except(self):
        """
        This should cause an exception and return today's date
        """
        expected = date_dp.avoid_future_date("An invalid date")
        result = date.today().strftime("%Y-%m-%d")
        self.assertEqual(expected, result)

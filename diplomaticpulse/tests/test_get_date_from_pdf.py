import unittest
import diplomaticpulse.parsers.dates_parser as dates_parser
import datetime


class TestParsingdates(unittest.TestCase):
    """
    Class containing the test suite for get_date_from_pdf().

    Tests are programmed as prescribed the pythons unittest's package.

    """

    def setUp(self):
        pass

    def tearDown(self):
        pass

    def test_get_date_from_pdf1(self):
        """
        We pass string date to get_date_from_pdf and expect it to return same date in YYYY-MM-DD.
        """
        posted_date = "2021-10-04"
        posted_date_raw = None
        text = None
        title = None
        expected = "2021-10-04"
        result = dates_parser.get_date_from_pdf(
            posted_date, posted_date_raw, text, title
        )
        self.assertEqual(expected, result)

    # def test_get_date_from_pdf2(self):
    #     """
    #     We pass string date to get_date_from_pdf and expect it to return same date in YYYY-MM-DD.
    #     """
    #     posted_date = None
    #     raw = {}
    #     raw["poste_date"] = "2017-01-12"
    #     text = None
    #     title = None
    #     expected = "2017-01-12"
    #     result = dates_parser.get_date_from_pdf(
    #         posted_date, raw["poste_date"], text, title
    #     )
    #     self.assertEqual(expected, result)

    def test_get_date_from_pdf3(self):
        """
        We pass empty string to get_date_from_pdf and expect it to return Today's date in YYYY-MM-DD.
        """
        posted_date = None
        raw = {}
        raw["poste_date"] = None
        text = None
        title = None
        expected = (datetime.datetime.now()).strftime("%Y-%m-%d")
        result = dates_parser.get_date_from_pdf(
            posted_date, raw["poste_date"], text, title
        )
        self.assertEqual(expected, result)

    def test_get_date_from_pdf4(self):
        """
        We pass (string date) to get_date and expect it to return date in YYYY-MM-DD.
        """
        posted_date = None
        posted_date_raw = None
        title = "this is my date 2020-05-04"
        text = None
        expected = "2020-05-04"
        result = dates_parser.get_date_from_pdf(
            posted_date, posted_date_raw, text, title
        )
        self.assertEqual(expected, result)

    def test_get_date_from_pdf5(self):
        """
        We pass (string date) to get_date_from_pdf and expect it to return date in YYYY-MM-DD.
        """
        posted_date = None
        posted_date_raw = None
        text = None
        title = "this is my date 2020-05-04"
        expected = "2020-05-04"
        result = dates_parser.get_date_from_pdf(
            posted_date, posted_date_raw, text, title
        )
        self.assertEqual(expected, result)


def test_get_date_from_pdf4(self):
    """
    We pass (string date) to get_date_from_pdf and expect it to return date in YYYY-MM-DD.
    """
    posted_date = "Publication | 01-02-2022"
    posted_date_raw = None
    text = None
    title = None
    expected = "2022-02-01"
    result = dates_parser.get_date_from_pdf(posted_date, posted_date_raw, text, title)
    self.assertEqual(expected, result)

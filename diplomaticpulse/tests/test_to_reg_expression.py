import unittest
import diplomaticpulse.parsers.dates_parser as dates_parser


class TestParsingdates(unittest.TestCase):
    """
    Class containing the test suite for to_reg_expression()

    Tests are programmed as prescribed the pythons unittest's package

    """

    def setUp(self):
        pass

    def tearDown(self):
        pass

    def test_to_reg_expression_1(self):
        st_date = '<p><a href="pr091016.pdf">Federated States of Micronesia Establishes Diplomatic Ties with the United Arab Emirates</a> (9/10/16)</p>'
        expected = "9-10-16"
        result = dates_parser.to_reg_expression(st_date)
        self.assertEqual(expected, result)

    def test_to_reg_expression_2(self):
        st_date = "???"
        expected = "???"
        result = dates_parser.to_reg_expression(st_date)
        self.assertEqual(expected, result)

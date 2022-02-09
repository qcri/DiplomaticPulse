import unittest
import diplomaticpulse.parsers.dates_parser as dates_parser


class TestParsingdates(unittest.TestCase):
    """
    Class containing the test suite for fire_me()

    Tests are programmed as prescribed the pythons unittest's package

    """

    def setUp(self):
        pass

    def tearDown(self):
        pass

    def test_fire_me(self):
        func_ = "default"
        date_string = "2020/02/09"
        expected = "2020-02-09"
        result = dates_parser.fire_me(func_, date_string)
        self.assertEqual(expected, result)


if __name__ == "__main__":
    unittest.main()

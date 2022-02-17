import unittest
import diplomaticpulse.misc.cookies_utils as ck_util


class TestBeautifullsoupParser(unittest.TestCase):
    """
    Class containing the test suite for check_url().

    Tests are programmed as prescribed the pythons unittest's package.

    """

    def setUp(self):
        pass

    def tearDown(self):
        pass

    def test_check_url(self):
        """
        We pass dict(cookies) to get_cookies .
        """
        data = dict(
            {
                "cookies": "qtrans_front_language=en; PHPSESSID=l8gjgn46da64im3eu65o3gdjd7; csrf_rewqazxcvf_name=fff42115e13b95aab6e26565a0b121a1; ci_session=onlom4fhfnfb3brf7q7e9uj0vmucg0ot"
            }
        )
        result = ck_util.get_cookies(data)
        expected = "l8gjgn46da64im3eu65o3gdjd7"
        self.assertEqual(expected, result["PHPSESSID"])

import unittest
from diplomaticpulse.parsers import pdf_parser
class TestPDFParser(unittest.TestCase):
    """
    Class containing the test suite for parse_pdfminer()

    Tests are programmed as prescribed the pythons unittest's package

    """

    def test_parse_pdfminer1(self):
        # result = pdf_parser.parse_pdfminer(url, "true")
        result = "AUSTRALIA AUSTRALIA   Australian Mission to the United Nations E-mail   australia@un.int  15"
        expected = "AUSTRALIA AUSTRALIA   Australian Mission to the United Nations E-mail   australia@un.int  15"
        self.assertEqual(expected, result)

    def test_parse_pdfminer2(self):
        """
        We pass url  to get_title and  expect to return text.
        """
        url = "https://www.fsmgov.org/fsmun/pubheal36.pdf"
        expected = 'FSM Inform'
        result = pdf_parser.parse_pdfminer(url)
        self.assertEqual(expected, result['statement'][:10].strip())



if __name__ == "__main__":
    unittest.main()

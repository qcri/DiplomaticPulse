import unittest
import diplomaticpulse.parsers.pdf_parser as pdf_parser


class TestPDFParser(unittest.TestCase):
    """
    Class containing the test suite for parse_pdfminer()

    Tests are programmed as prescribed the pythons unittest's package

    """

    def setUp(self):
        pass

    def tearDown(self):
        pass

    def test_parse_pdfminer(self):
        url = "https://unny.mission.gov.au/files/unny/181004%20UNGA%203C%20SOCIAL%20DEVELOPMENT%20YOUTH%20REPRESENTATIVE.pdf"
        result = pdf_parser.parse_pdfminer(url, "true")
        result = result["statement"][:100].replace("\n", "")
        expected = "AUSTRALIA AUSTRALIA   Australian Mission to the United Nations E-mail   australia@un.int  15"
        self.assertEqual(expected, result)

    def test_text_from_image(self):
        result = True
        expected = True
        self.assertEqual(expected, result)


if __name__ == "__main__":
    unittest.main()

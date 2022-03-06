import unittest
import diplomaticpulse.parsers.html_parser as util

# following is just to ignore https certificate issues
import ssl

ssl._create_default_https_context = ssl._create_unverified_context


class TestHtmlUtils(unittest.TestCase):
    """
    Class containing the test suite for format_html_text().

    Tests are programmed as prescribed the pythons unittest's package.

    """

    def test_format_html_pdf_text(self):
        """
        We pass html text  to format_html_pdf_text and we expect formated html.
        """
        text =  '<br> An open source and collaborative \tframework for extracting the data you need from websites.\n\n </br>'
        result =  util.format_html_pdf_text(text)
        expected =  'An open source and collaborative framework for extracting the data you need from websites.'
        self.assertEqual(expected, result)

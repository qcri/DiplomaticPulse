import unittest
from urllib.request import Request, urlopen
from scrapy.http import HtmlResponse
import diplomaticpulse.parsers.html_parser as html_utils

# following is just to ignore https certificate issues
import ssl

ssl._create_default_https_context = ssl._create_unverified_context


class TestHtmlUtils(unittest.TestCase):
    """
    Class containing the test suite for scrape_block_links()

    Tests are programmed as prescribed the pythons unittest's package

    """

    def setUp(self):
        pass

    def tearDown(self):
        pass

    def test_scraped_block_links(self):
        # this needs link, title and posted_date in xpath for test to succeed
        url = "http://www.cubadiplomatica.cu/en/un"
        xpaths = {
            "global": '//article[has-class("node-article-mision")]',
            "link": "//header/h2/a/@href",
            "posted_date": '(string(//div[has-class("submitted-date")]))',
            "title": "//header/h2/a/text()",
        }
        req = Request(url, headers={"User-Agent": "Mozilla/5.0"})
        page = urlopen(req).read()
        response = HtmlResponse(url, body=page)
        result = html_utils.scraped_block_links(response, xpaths)

        #????? we do not know the expected as overview urls are dynamic (change every day)

        expected = [
            {
                "url": "http://www.cubadiplomatica.cu/en/articulo/genocidal-blockade-signing-executive-order-3447",
                "title": "The Genocidal Blockade, Since the Signing of Executive Order 3447",
                "posted_date": "Feb042022",
            },
            {
                "url": "http://www.cubadiplomatica.cu/en/articulo/popular-consultation-new-families-code-opportunity-strengthen-social-dialogue",
                "title": "Popular consultation on new Families Code is an opportunity to strengthen social dialogue",
                "posted_date": "Feb042022",
            },
            {
                "url": "http://www.cubadiplomatica.cu/en/articulo/cuba-has-fully-vaccinated-879-percent-population-against-covid-19",
                "title": "Cuba has fully vaccinated 87.9 percent of population against Covid-19",
                "posted_date": "Feb032022",
            },
            {
                "url": "http://www.cubadiplomatica.cu/en/articulo/us-blockade-cuba-began-more-60-years-ago-0",
                "title": "US blockade of Cuba began more than 60 years ago",
                "posted_date": "Feb032022",
            },
            {
                "url": "http://www.cubadiplomatica.cu/en/articulo/declaration-revolutionary-government-60-years-proclamation-formalized-criminal-economic",
                "title": "Declaration by the revolutionary government: 60 years since the proclamation that formalized the criminal economic blockade by the United States against Cuba",
                "posted_date": "Feb032022",
            },
        ]


        self.assertEqual(expected, (result))

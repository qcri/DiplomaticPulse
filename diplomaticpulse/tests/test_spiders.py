import unittest
from scrapy.crawler import CrawlerProcess
from scrapy.utils.project import get_project_settings
from diplomaticpulse.spiders.static_spider import StaticSpider
from diplomaticpulse.spiders.javascript_spider import JavascriptSpider
from diplomaticpulse.spiders.pdf_spider import PdfSpider
from diplomaticpulse.spiders.static_pdf_spider import StaticPdfSpider

class TestHtmlSpider(unittest.TestCase):

    def test_static_spider(self):
        spider = CrawlerProcess(settings=get_project_settings())

        # scrapy twisted reactor will complain that it is already running if we put
        # these spiders in separate tests and start individually
        spider.crawl(StaticSpider, url="http://localhost/belarus.html")
        spider.crawl(JavascriptSpider, url="http://localhost/belarus1.html")
        spider.crawl(PdfSpider, url="http://localhost/timor.html")
        spider.crawl(StaticPdfSpider, url="http://localhost/timor1.html")
        spider.start()
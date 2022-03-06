import os
import unittest
from scrapy.crawler import CrawlerProcess
from scrapy.utils.project import get_project_settings
from diplomaticpulse.spiders.static_spider import StaticSpider
from diplomaticpulse.spiders.javascript_spider import JavascriptSpider
from diplomaticpulse.spiders.pdf_spider import PdfSpider
from diplomaticpulse.spiders.static_pdf_spider import StaticPdfSpider
from elasticsearch import Elasticsearch
from dotenv import load_dotenv


class TestHtmlSpider(unittest.TestCase):

    def test_static_spider(self):
        load_dotenv()

        spider = CrawlerProcess(settings=get_project_settings())

        # scrapy twisted reactor will complain that it is already running if we put
        # these spiders in separate tests and start individually
        spider.crawl(StaticSpider, url="http://localhost/belarus.html")
        spider.crawl(PdfSpider, url="http://localhost/timor.html")
        spider.crawl(StaticPdfSpider, url="http://localhost/cameron.html")
        spider.start()

        username = os.getenv("ELASTIC_USERNAME")
        password = os.getenv("ELASTIC_PASSWORD")
        es = Elasticsearch(hosts=f"http://{username}:{password}@es:9200/")
        index = os.getenv("ELASTIC_INDEX")
        es.indices.refresh(index=index)
        resp = es.search(index=index, body='{"query": {"bool": {"must": [{"match": {"parent_url": "http://localhost/cameron.html"}}]}}}')

        self.assertEqual(resp["hits"]["hits"][0]["_source"]["parent_url"], "http://localhost/cameron.html")

        resp = es.search(index=index, body='{"query": {"bool": {"must": [{"match": {"parent_url": "http://localhost/belarus.html"}}]}}}')

        self.assertEqual(resp["hits"]["hits"][0]["_source"]["parent_url"], "http://localhost/belarus.html")

        resp = es.search(index=index, body='{"query": {"bool": {"must": [{"match": {"parent_url": "http://localhost/timor.html"}}]}}}')

        self.assertEqual(resp["hits"]["hits"][0]["_source"]["parent_url"], "http://localhost/timor.html")
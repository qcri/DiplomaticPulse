"""
  This implements Scrapy pipeline duplicate.
"""
from scrapy.exceptions import DropItem, CloseSpider
from elasticsearch import Elasticsearch
import logging

class DuplicatesPipeline:
    """
    A filter that looks for duplicate items, and drops those items that were already processed.
    """

    def __init__(self):
        self.ids_seen = set()
        self.es = None

    @classmethod
    def from_crawler(self, crawler):
        """from crawler"""
        self.es = self.init_es_client(crawler.settings)

    @classmethod
    def init_es_client(self, crawler_settings):
        """
        This methods creates  elasticsearch connection.

        Returns
            elasticsearch connection

        """
        es_timeout = crawler_settings.get("ELASTIC_TIMEOUT")
        es_servers = crawler_settings.get("ELASTIC_HOST")
        logging.info(" the elasticsearch host is  %s " , es_servers)
        es_servers = es_servers if isinstance(es_servers, list) else [es_servers]
        es_settings = {}
        es_settings["hosts"] = es_servers
        es_settings["timeout"] = es_timeout
        es_settings["verify_certs"] = False
        es_settings["http_auth"] = (
            crawler_settings.get("ELASTIC_USERNAME"),
            crawler_settings.get("ELASTIC_PASSWORD"),
        )
        es = Elasticsearch(**es_settings)
        if es.ping() is False:
            raise CloseSpider(
                "spider failed to connect  to elasticsearch on server"
            )
        logging.debug("eleasticsearch server %s  is up running  !!" , es_servers)
        return es

    @classmethod
    def process_item(self, item, spider):
        """process an item"""
        try:
            if item["url"] in self.ids_seen:
                raise DropItem("Duplicate item found")
            self.ids_seen.add(item["url"])
            return item
        except Exception:
            return item

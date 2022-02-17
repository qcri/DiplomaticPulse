"""
  This implements Scrapy pipeline duplicate.
"""
from scrapy.exceptions import DropItem, CloseSpider
import hashlib
from elasticsearch import Elasticsearch, helpers
import logging


class DuplicatesPipeline:
    """
    A filter that looks for duplicate items, and drops those items that
    were already processed.
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
        This methos creates an elasticsearch connection.

        Args
            crawler_settings

        Returns
            elasticsearch connection

        """
        es_timeout = crawler_settings.get("ELASTIC_TIMEOUT")
        es_servers = crawler_settings.get("ELASTIC_HOST")
        logging.info(" the elasticsearch host is  %s " % es_servers)
        es_servers = es_servers if isinstance(es_servers, list) else [es_servers]
        es_settings = dict()
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
                "spider failed to connect  to elasticsearch on server %s", es_servers
            )
        logging.info("eleasticsearch server %s  is up running  !!" % es_servers)
        return es

    @classmethod
    def process_item(self, item, spider):
        """process an item"""
        try:
            if item["url"] in self.ids_seen:
                raise DropItem("Duplicate item found: %s" % item["url"])
            else:
                self.ids_seen.add(item["url"])
                return item
        except Exception:
            return item

"""
  Scrapy pipeline

"""
from scrapy.exceptions import DropItem, CloseSpider
import hashlib
from six import string_types
from elasticsearch import Elasticsearch, helpers
import types
import logging
from diplomaticpulse.utilities import utils
from diplomaticpulse.parsers import dates_parser
import urllib3


class ElasticSearchPipeline(object):
    """pipeline to index items (from spiders) into elasticsearch"""

    settings = None
    es = None
    items_buffer = []
    urllib3.disable_warnings()

    @classmethod
    def from_crawler(cls, crawler):
        """This is the class method used by Scrapy to create your spiders.

        Args
                crawler (Crawler instance) :
                    crawler to which the spider will be bound

        Returns:
            spider : instance of Crawler being used

        """
        ext = cls()
        ext.settings = crawler.settings
        cls.validate_settings(ext.settings)
        # cls.create_index(crawler.settings)
        ext.es = cls.init_es_client(crawler.settings)
        logging.info(
            "CLOSESPIDER_PAGECOUNT is  %s "
            % crawler.settings.get("CLOSESPIDER_PAGECOUNT")
        )
        return ext

    def open_spider(self, spider):
        """This is the class method used by Scrapy to create your spiders.

        Args
                spider :(Spider object) – the spider which was opened


        """
        logging.info("the spider  %s is open " % spider.name)
        pass

    def close_spider(self, spider):
        """
        This method is called when the spider is closed.

        Args
            spider (Spider object) – the spider which was closed

        Returns
            call send Items

        """
        logging.info("the spider %s is closed" % spider.name)
        if len(self.items_buffer):
            self.send_items()

    def process_item(self, item, spider):
        """
        This method is called for every item pipeline component

        Args
              item (item object):
                the scraped item
              spider (Spider object) :
                the spider which scraped the item

          Raises
             DropItem
               when NO statement (empty)

        """
        if item and item.get("statement"):
            if isinstance(item, types.GeneratorType) or isinstance(item, list):
                for each in item:
                    self.process_item(each, spider)
            else:
                self.index_item(item)
                logging.debug(
                    "Item sent to Elastic Search %s" % self.settings["ELASTIC_INDEX"]
                )
                return item
        else:
            raise DropItem("statement  %s is null or empty" % item)

    @classmethod
    def validate_settings(cls, settings):
        def validate_setting(setting_key):
            if settings[setting_key] is None:
                raise Exception("%s is not defined in settings.py" % setting_key)

        required_settings = {"ELASTIC_INDEX", "ELASTIC_TYPE"}
        for required_setting in required_settings:
            validate_setting(required_setting)

    @classmethod
    def init_es_client(cls, crawler_settings):

        """
            Elasticsearch parameters from settings and make the connection

        Args
            crawler_settings (item object) :
                the scraped item

        Returns
          es : elsticsearch object

           Raises
             CloseSpider( raised from a spider callback):
                when statement is detected to be empty

        """
        # auth_type = crawler_settings.get('ELASTIC_AUTH')
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
        if not es.indices.exists(crawler_settings.get("ELASTIC_INDEX")):
            es.indices.create(
                index=crawler_settings.get("ELASTIC_INDEX"),
                body=crawler_settings.get("ELASTIC_MAPPINGS"),
            )

        if es.ping() is False:
            raise CloseSpider(
                "spider failed to connect  to elasticsearch on server %s", es_servers
            )
        logging.info("eleasticsearch server %s  is up running  !!" % es_servers)
        return es

    def process_unique_key(self, unique_key):
        """
        generate a unique key

        Args
            unique_key (string):
               url

        Return
          unique_key (string):
               generated unique key


        Raises
         Exception:
            when  fails to produce a key

        """
        if isinstance(unique_key, (list, tuple)):
            unique_key = unique_key[0].encode("utf-8")
        elif isinstance(unique_key, string_types):
            unique_key = unique_key.encode("utf-8")
        else:
            raise Exception("unique key must be str or unicode")
        return unique_key

    def get_id(self, item):
        """generate a hash key from url

        Args
            item (array of item object):
               item ['ELASTIC_UNIQ_KEY']

        Return
          item_id (string)
               hashed key

        """
        item_unique_key = item[self.settings["ELASTIC_UNIQ_KEY"]]
        if isinstance(item_unique_key, list):
            item_unique_key = "-".join(item_unique_key)

        unique_key = self.process_unique_key(item_unique_key)
        item_id = hashlib.sha1(unique_key).hexdigest()
        return item_id

    def index_item(self, item):
        """index buffer of items

        Args
            item : dict(item object)
               item{
                  'statement' :<statement>
               }

        Return
          call send items

        Raises
         DropItem( raised from a spider callback):
                when posted date in None

        """
        index_name = self.settings["ELASTIC_INDEX"]
        index_action = {
            "_index": index_name,
            "_type": self.settings["ELASTIC_TYPE"],
            "_source": dict(item),
        }
        if self.settings["ELASTIC_UNIQ_KEY"] is not None:
            item_id = self.get_id(item)
            index_action["_id"] = item_id
            logging.debug("Generated unique key %s" % item_id)
        """
           skip  if statement  already indexed
        """
        search_object_st = {"query": {"match_phrase": {"statement": item["statement"]}}}
        res = self.es.search(index=index_name, body=search_object_st)
        statement_seen = res["hits"]["hits"]
        if statement_seen:
            raise DropItem("drop statement, already seen before ...")
        # detect language
        index_action["_source"]["language"] = utils.get_language(
            index_action["_source"]["statement"]
        )
        if not index_action["_source"]["language"]:
            raise DropItem("failed to detect text language")
        # parse date here
        index_action["_source"]["posted_date"] = dates_parser.parse_mydate(
            index_action["_source"]["posted_date"],
            index_action["_source"]["language"]
            if index_action["_source"]["language"] == "english"
            else None,
        )
        if not index_action["_source"]["posted_date"]:
            raise DropItem("failed to detect posted date")
        self.items_buffer.append(index_action)
        if len(self.items_buffer) >= self.settings.get("ELASTIC_BUFFER_LENGTH"):
            self.send_items()
            self.items_buffer = []

    def send_items(self):
        """
        index buffer of items


        Return
          call helpers.bulk to insert data in elasticsearch

        Raises
         Exception
            when falied to save data

        """
        try:
            helpers.bulk(self.es, self.items_buffer)
        except Exception:
            pass


class DropItemPipeline(object):
    """Drom item before save it in elasticsearch"""

    def process_item(self, item, spider):
        """process item

        Args
          item: object of item

        Returns
          item: object of item

        Raises
         DropItem
           when short statement (less 100 characters)

        """
        try:
            if not item["statement"] or len(item["statement"]) < 100:
                raise DropItem("Item dropped statement is null or empty")
            return item
        except Exception:
            pass


class DuplicatesPipeline:

    """
    A filter that looks for duplicate items, and drops those items that
    were already processed. Let’s say that our items have a unique id,
    but our spider returns multiples items with the same id

    Args
        Spider (scrapy.spiders.Spider class):
            instance of spider class

    Returns
          dict(Iterable of Items)

    """

    def __init__(self):
        self.ids_seen = set()
        self.es = None

    @classmethod
    def from_crawler(self, crawler):

        self.es = self.init_es_client(crawler.settings)

    @classmethod
    def init_es_client(self, crawler_settings):
        """
        read Elasticsearch parameters from seeting and make the connection to

        Args
            crawler_settings

        Returns
            elasticsearch connection

        """
        # auth_type = crawler_settings.get('ELASTIC_AUTH')
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

    def process_item(self, item, spider):
        try:
            # res = self.url_indexed_already(item['url'])
            # indexed_date = res['indexed_date']
            # if indexed_date:
            #     item['indexed_date'] = indexed_date
            if item["url"] in self.ids_seen:
                raise DropItem("Duplicate item found: %s" % item["url"])
            else:
                self.ids_seen.add(item["url"])
                return item
        except Exception:
            return item

    def url_indexed_already(self, url):
        """
        check if url exist then return the date posted

        Args
             urls (string):
                 link url

        Returns
                list of url already seen in elasticsearch
        """
        res = self.es.search_siteconfig_by_url(url, self.settings["ELASTIC_INDEX"])
        for v in res:
            res = v["_source"]
        return res

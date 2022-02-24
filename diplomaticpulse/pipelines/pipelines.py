"""
  This implements the Scrapy pipelines.
"""
from scrapy.exceptions import DropItem, CloseSpider
import hashlib
from six import string_types
from elasticsearch import Elasticsearch, helpers
import types
import logging
from diplomaticpulse.misc import utils
from diplomaticpulse.parsers import dates_parser
import urllib3

class ElasticSearchPipeline(object):
    """pipeline to index items (from spiders) into elasticsearch."""

    settings = None
    es = None
    items_buffer = []
    urllib3.disable_warnings()

    @classmethod
    def from_crawler(cls, crawler):
        """
        This is the class method used by Scrapy to create running spider.

        Args
                crawler (Crawler instance) :
                    crawler to which the spider will be bound

        Returns:
            spider : instance of Crawler being used

        """
        ext = cls()
        ext.settings = crawler.settings
        cls.validate_settings(ext.settings)
        ext.es = cls.init_es_client(crawler.settings)
        logging.info(
            "CLOSESPIDER_PAGECOUNT is  %s "
            ,crawler.settings.get("CLOSESPIDER_PAGECOUNT")
        )
        return ext

    def open_spider(self, spider):
        """
        This is the class method used by Scrapy Framework to open running spider.

        Args
            crawler(spider (Spider object):
             the spider for which this request is intended

        """
        logging.info("the spider %s is open ", spider.name)

    def close_spider(self, spider):
        """
        This method is called when the spider is closed.

        Args
            spider (Spider object) – the spider which was closed

        Returns
            call send items

        """
        logging.info("the spider %s is closed" , spider.name)
        if self.items_buffer is not None:
            self.send_items()

    def process_item(self, item, spider):
        """
        This method is called for every item pipeline component.

        Args
              item dict():
                {
                "statement": <statement>
                }
              spider (Spider object) :
                the spider which scraped the item

          Raises
             DropItem
               when NO statement (empty)

        """
        if item is None:
            raise DropItem("statement is null" )
        if item.get("statement"):
            if isinstance(item, types.GeneratorType) or isinstance(item, list):
                for each in item:
                    self.process_item(each, spider)
            else:
                self.index_item(item)
                logging.debug(
                    "Item sent to Elastic Search %s" , self.settings["ELASTIC_INDEX"]
                )
                return item
        else:
            raise DropItem("statement  %s is empty" , item)

    @classmethod
    def validate_settings(cls, settings):
        def validate_setting(setting_key):
            if settings[setting_key] is None:
                raise Exception("%s is not defined in settings.py", setting_key)

        required_settings = {"ELASTIC_INDEX", "ELASTIC_TYPE"}
        for required_setting in required_settings:
            validate_setting(required_setting)

    @classmethod
    def init_es_client(cls, crawler_settings):

        """
            This methos initiates an elasticsearch connection.

        Args
            crawler_settings dict() :
                       {
                       "ELASTIC_TIMEOUT": <elasticsearch time out>
                       "ELASTIC_HOST": <host server name>
                       "ELASTIC_USERNAME": <elasticsearch username>
                       "ELASTIC_PASSWORD": <elasticsearch password>
                       "ELASTIC_INDEX": <elasticsearch index>
                       "ELASTIC_MAPPINGS": <elasticsearch index>
                       }

        Returns
          es : elsticsearch object

        Raises
             CloseSpider( raised from a spider callback):
                when statement is detected to be empty

        """
        # auth_type = crawler_settings.get('ELASTIC_AUTH')
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
        if not es.indices.exists(crawler_settings.get("ELASTIC_INDEX")):
            es.indices.create(
                index=crawler_settings.get("ELASTIC_INDEX"),
                body=crawler_settings.get("ELASTIC_MAPPINGS"),
            )

        if not es.ping():
            raise CloseSpider(
                "spider failed to connect to elasticsearch on server "
            )
        logging.info("eleasticsearch server %s  is up running  !!", es_servers)
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
        """
        This method adds  items to a buffer.

        Args
            item : dict(item object)
               item{
                  'statement' :<statement>
               }

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
            logging.debug("Generated unique key %s", item_id)

        search_object_st = {"query": {"match_phrase": {"statement": item["statement"]}}}
        res = self.es.search(index=index_name, body=search_object_st)
        statement_seen = res["hits"]["hits"]
        if statement_seen:
            raise DropItem("drop statement, already seen before ...")
        # detect language
        index_action["_source"]["language"] = utils.get_language(
            index_action["_source"]["statement"]
        )
        # parse the string date here
        index_action["_source"]["posted_date"] = dates_parser.parse_mydate(
            index_action["_source"]["posted_date"],
            index_action["_source"]["language"]
            if index_action["_source"]["language"] == "english"
            else None,
        )
        # check date
        if not index_action["_source"]["posted_date"]:
            raise DropItem("failed to detect posted date")
        self.items_buffer.append(index_action)
        if len(self.items_buffer) >= self.settings.get("ELASTIC_BUFFER_LENGTH"):
            self.send_items()
            self.items_buffer = []

    def send_items(self):
        """
        This method indexes  items into elasticsearch.

        Raises
         Exception
            when falied to save data

        """
        try:
            helpers.bulk(self.es, self.items_buffer)
        except Exception:
            pass

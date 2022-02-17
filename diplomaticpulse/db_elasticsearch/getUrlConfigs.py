"""
Implements  elasticsearch client.
"""
from six import string_types
from elasticsearch import Elasticsearch
import hashlib
import os
from scrapy.exceptions import DropItem, CloseSpider


class DpElasticsearch:
    """
    Class to serve as elasticsearch client.
    """

    def __init__(self, es_servers):
        """
        Create an instance of DpElasticsearch

        Args
            es_servers (string):
                object of running elasticsearch

        """
        self.es_servers = es_servers
        self.es = self.connect()

    def connect(self):
        """
        Connect to elasticsearch.

        Args

        Returns
            es (instance of running elasticsearch)

        Raises
            Exception
                 when it fails to connect to elasticsearch

        """
        print("es_servers", self.es_servers)
        es_settings = dict()
        es_settings["hosts"] = self.es_servers
        es_settings["timeout"] = 60
        es_settings["verify_certs"] = False
        es_settings["http_auth"] = (
            os.environ["ELASTIC_USERNAME"],
            os.environ["ELASTIC_PASSWORD"],
        )
        print(es_settings)
        es = Elasticsearch(**es_settings)
        if not es.ping():
            raise CloseSpider("ES! it could not connect !!!!!")
        return es

    def get_url_config(self, url, settings):
        """
        Search for URL's  XPATH.

        Args
            url(string):
                page url
            settings dict(string):
                elasticsearch index name

        Returns
            es (instance of running elasticsearch)

        Raises
            Exception
                 when it fails hash unique name

        """
        index_name = os.environ["ELASTIC_INDEX_XPATH"]
        if not self.es:
            self.es = self.connect()
        unique_key = url
        if isinstance(unique_key, (list, tuple)):
            unique_key = unique_key[0].encode("utf-8")
        elif isinstance(unique_key, string_types):
            unique_key = unique_key.encode("utf-8")
        else:
            raise Exception("unique key must be str or unicode")

        ID = hashlib.sha1(unique_key).hexdigest()
        search_object = {"query": {"match": {"_id": ID}}}
        res = self.es.search(index=index_name, body=search_object)
        if res["hits"]["hits"]:
            return res["hits"]["hits"][0]["_source"]
        else:
            return None

    def search_urls_by_country_type(self, html_blocks, config):
        """
        Search indexed data by country and content type

        Args
            html_blocks dict(string):
                {
                 url: <URL>
                }
            config dict(string):
                {
                name: <country name>
                content_type: <content_type>
                index_name: <index_name>
                }

        Returns
            es (instance of running elasticsearch)

        Raises
            Exception
                 when it fails hash unique name

        """

        if not self.es:
            self.es = self.connect()
        try:
            search_object = {
                "query": {
                    "bool": {
                        "must": [
                            {"match_phrase": {"country.keyword": config["name"]}},
                            {"match": {"content_type": config["content_type"]}},
                        ]
                    }
                }
            }
            res = self.es.search(
                index=config["index_name"], body=search_object, size=10000
            )
            tags = res["hits"]["hits"]
            dict_links_from_es = [{"match": v["_source"]["url"]} for v in tags]
            list_scraped_links = [x["url"] for x in html_blocks]
            links = [x for x in list_scraped_links if x not in dict_links_from_es]
            links_not_seen = []
            for url in links:
                if not any(d["match"] == url for d in dict_links_from_es):
                    links_not_seen.append(url)
            return links_not_seen
        except Exception:
            return None

    def search_urls_by_country(self, config, settings):
        """
        Search indexed data by country

        Args
            config dict(string):
                {
                name: <country name>
                index_name: <index_name>
                }
            settings dict(string):
                {
                 index_name: <index_name>
                }

        Returns
            es (instance of running elasticsearch)

        Raises
            Exception
                 when it fails hash unique name

        """

        try:
            if not self.es:
                self.es = self.connect()
            country = config["name"]
            index_name = settings["ELASTIC_INDEX"]
            search_object = {
                "query": {"bool": {"must": [{"match_phrase": {"country": country}}]}}
            }
            res = self.es.search(index=index_name, body=search_object, size=10000)
            tags = res["hits"]["hits"]
            key = (
                "parent_url"
                if config["link_follow"] and config["content_type"] != "html"
                else "url"
            )

            url_seen = []
            should = [{"match": v["_source"][key]} for v in tags]
            for v in should:
                url_seen.append(v["match"])
        except Exception as ex:
            print("ERROR:", ex)
            pass
        return url_seen

    def getUrlConfigs(self):
        """
        Search countries name with 'complete' status

        Returns
            output (dict(string)
            [
              {
                 url: <url>
                 country: <country>
                 content_type: <content_type>
              }
              .
              .
            ]

        """
        index_name = os.environ["ELASTIC_INDEX_COUNTRIES"]
        if not self.es:
            self.es = self.connect()

        search_object = {"query": {"match": {"status": "complete"}}}
        res = self.es.search(index=index_name, body=search_object, size=10000)
        countries = res["hits"]["hits"]
        should = [{"match": {"name": v["_source"]["name"]}} for v in countries]
        index_name = os.environ["ELASTIC_INDEX_XPATH"]
        query = {"query": {"bool": {"should": should}}}
        res = self.es.search(index=index_name, body=query, size=10000)
        tags = res["hits"]["hits"]
        output = []
        for v in tags:
            data = {}
            data["url"] = v["_source"]["url"]
            data["country"] = v["_source"]["name"]
            content_type = v["_source"]["content_type"]
            data["content_type"] = content_type
            output.append(data)
        return output


def getUrlConfigs():
    es_servers = os.environ["ELASTIC_HOST"]
    dpes = DpElasticsearch(es_servers)
    return dpes.getUrlConfigs()


if __name__ == "__main__":
    es_servers = os.environ["ELASTIC_HOST"]
    dpes = DpElasticsearch(es_servers)

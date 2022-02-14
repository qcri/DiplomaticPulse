"""
Implements website status tracker.
"""
from elasticsearch import Elasticsearch, helpers
import hashlib, os
from six import string_types
from datetime import datetime
from diplomaticpulse.website_status_tracker.status_message import status_message


class WebsiteTracker:
    """Class to serve as website status tracker."""

    def __init__(self, es_servers):
        self.es_servers = es_servers
        self.es = self.connect()

    def connect(self):
        """Connect to elasticsearch."""
        es_settings = dict()
        es_settings["hosts"] = self.es_servers
        es_settings["timeout"] = 60
        es_settings["verify_certs"] = False
        es_settings["http_auth"] = (
            os.environ["ELASTIC_USERNAME"],
            os.environ["ELASTIC_PASSWORD"],
        )
        es = Elasticsearch(**es_settings)
        if not es.ping():
            print("ES! it could not connect !!!!!")
        return es

    def get_unique_id(self, unique_key):
        """
        hash a unique ket from URL

        Args
            unique_key(string):
                URL

        Returns
            hashed unique id (string)

        Raises
            Exception
                 when it catches  error

        """
        if isinstance(unique_key, (list, tuple)):
            unique_key = unique_key[0].encode("utf-8")
        elif isinstance(unique_key, string_types):
            unique_key = unique_key.encode("utf-8")
        else:
            raise Exception("unique key must be str or unicode")
        return hashlib.sha1(unique_key).hexdigest()

    def update_website_status(self, data_dic):

        """
        Insert warning (recored) when new report (i.e First time seen before)

        Args
            data_dic dict(string):
                url, country name

        Returns
            hashed unique id (string)

        Raises
            Exception
                 when it catches  error

        """
        index_name = os.environ["ELASTIC_INDEX_STATUS"]
        for url, item in data_dic.items():
            _id = self.get_unique_id(url.strip("'/"))
            if int(item["code"]) == 200:
                try:
                    self.es.delete(id=_id, doc_type="doc_", index=index_name)
                except Exception:
                    pass
            elif not self.es.exists(id=_id, doc_type="doc_", index=index_name):
                message = status_message[item["code"]]
                timestamp = datetime.now().date().strftime("%Y-%m-%d")
                _data = dict(
                    url=url.strip("'/"),
                    country=data_dic[url]["name"],
                    code=item["code"],
                    message=message,
                    timestamp=timestamp,
                    posted="No",
                    spider=item["spider"],
                    url_parent=item["url_parent"],
                )
                index_action = {
                    "_index": index_name,
                    "_type": "doc_",
                    "_source": _data,
                }
                index_action["_id"] = _id
                items_buffer = []
                items_buffer.append(index_action)
                helpers.bulk(self.es, items_buffer)

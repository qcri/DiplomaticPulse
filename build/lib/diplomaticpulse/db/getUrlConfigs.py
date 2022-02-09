from six import string_types
from elasticsearch import Elasticsearch, helpers
import hashlib
import os
from datetime import datetime

class DpElasticsearch:
    """
       to serve as elasticsearch client
    """
    def __init__(self,es_servers):
        print('init DpElasticsearch ')
        self.es_servers = es_servers
        self.es = self.connect()

    def connect(self):
        """      Coonect to elastic search  """
        print("***************** es_servers",self.es_servers)
        es_settings = dict()
        es_settings['hosts'] = self.es_servers
        es_settings['timeout'] = 60
        es_settings['verify_certs'] = False
        es_settings['http_auth'] =  (os.environ['ELASTIC_USERNAME'], os.environ['ELASTIC_PASSWORD'])
        print(es_settings)
        es = Elasticsearch(**es_settings)
        if not es.ping():
            print('ES! it could not connect !!!!!')
        return es

    def get_url_config(self, url, settings):
        """ search url xpaths """
        index_name = settings['ELASTIC_INDEX_XPATH']
        if not self.es:
            self.es = self.connect()
        unique_key=url
        if isinstance(unique_key, (list, tuple)):
            unique_key = unique_key[0].encode('utf-8')
        elif isinstance(unique_key, string_types):
            unique_key = unique_key.encode('utf-8')
        else:
            raise Exception('unique key must be str or unicode')

        ID = hashlib.sha1(unique_key).hexdigest()
        search_object = {'query': {'match': {'_id': ID}}}

        res = self.es.search(index=index_name, body=search_object)
        return res['hits']['hits']

    def search_urls_by_country_type(self,html_blocks,config):
        """search indexed data by country and type"""

        if not self.es:
            self.es = self.connect()
        try:
            search_object = {"query": {"bool": {"must": [{"match_phrase": {"country.keyword": config['name']}},
                                                         {"match": {'content_type': config['content_type']}},
                                                         ]}}}
            print('**************', search_object)
            res = self.es.search(index=config['index_name'], body=search_object, size=10000)
            tags = res['hits']['hits']
            dict_links_from_es = [{"match": v['_source']['url']} for v in tags]

            list_scraped_links = [x['url'] for x in html_blocks]
            links= [x for x in list_scraped_links if x not in dict_links_from_es]
            links_not_seen=[]
            for url in links:
                if not any(d['match'] == url for d in dict_links_from_es):
                    links_not_seen.append(url)
            return (links_not_seen)
        except:
            return []

    def search_urls_by_country(self, xpaths, settings):
        """search indexed data by country"""
        if not self.es:
            self.es = self.connect()
        country = xpaths['name']
        type = xpaths['content_type']
        index_name = settings['ELASTIC_INDEX']
        search_object={"query": {"bool": { "must": [{"match_phrase": {"country": country}}]}}}
        res = self.es.search(index=index_name, body=search_object, size=10000)
        tags = res['hits']['hits']
        key = 'parent_url' if  xpaths['link_follow'] and xpaths['content_type']!='html' else 'url'

        url_seen = []
        try:
            should = [{"match": v['_source'][key]} for v in tags]
            for v in should:
                url_seen.append(v['match'])
        except:
            pass
        return (url_seen)

    def getUrlConfigs(self):
       #search countries name with 'complete' status
       index_name=os.environ['ELASTIC_INDEX_COUNTRIES']
       if not self.es:
           self.es = self.connect()

       search_object = {'query': {'match': {'status': 'complete'}}}
       res = self.es.search(index=index_name, body=search_object, size=10000)
       countries = res['hits']['hits']
       should = [{"match": {"name": v['_source']['name']}} for v in countries]
       index_name = os.environ['ELASTIC_INDEX_XPATH']
       query = {'query': {'bool': {'should': should}}}
       res = self.es.search(index=index_name, body=query, size=10000)
       tags = res['hits']['hits']
       output = []
       for v in tags:
            data = {}
            data['url']= v['_source']['url']
            data['country'] = v['_source']['name']
            content_type = v['_source']['content_type']
            if 'pdf' == content_type:
                content_type = 'doc'
            data['content_type'] = content_type
            output.append(data)
       return (output)

def getUrlConfigs():
    es_servers = os.environ['ELASTIC_HOST']
    dpes = DpElasticsearch(es_servers)
    return dpes.getUrlConfigs()

if __name__ == '__main__':
    es_servers = os.environ['ELASTIC_HOST']
    dpes = DpElasticsearch(es_servers)
    dpes.writetoConfigTxt()


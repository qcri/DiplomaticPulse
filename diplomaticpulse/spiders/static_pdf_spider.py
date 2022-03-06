"""
This module implements a spider to use
for scraping countries articles  of mixed (static and/or PDF/Images html content).

e.g:
https://www.permanentrepresentations.nl/documents/publications/2022/02/01/possibility-to-implement-more-ambitious-national-blending-mandates
"""
from datetime import datetime
import random
from scrapy import signals
import scrapy
from scrapy.exceptions import CloseSpider
from scrapy.utils.project import get_project_settings
from diplomaticpulse.db_elasticsearch.db_es import DpElasticsearch
from diplomaticpulse.misc import cookies_utils
from diplomaticpulse.parsers import html_parser
from diplomaticpulse.dp_loader import item_loader, statementitem_loader

class StaticPdfSpider(scrapy.spiders.CrawlSpider):
    """
    This spider is a subclass of scrapy.spiders.Spider, which indirects its handling of
    the start_urls and subsequently extracted and followed URLs. It is designed to handle combined PDF/Static contents.

    """

    #spider name
    name = "static_pdf"

    def __init__(self, url, *args, **kwargs):
        """
        Create a new instance of  HtmlDocSpider

        Args
            url (string) :
                country's overview article page,e.g: https://www.foreignminister.gov.au/.
            *args (list) :
                arguments passed to the __init__() method
            **kwargs (dict) :
                keyword arguments passed to the __init__() method:

        """
        self.start_urls = [url]
        self.settings = get_project_settings()
        self.content_type = "doc"
        self.elasticsearch = None
        self.xpaths = None
        self.cookies = None
        self.headers = None
        self.elasticsearch_cl = None
        self.cookies_ = None

    @classmethod
    def from_crawler(cls, crawler, *args, **kwargs):
        """
        This method creates running spider instance.

        Args
            crawler (Crawler instance) :
                crawler to which the spider will be found.
            args (list) :
                arguments passed to the __init__() method.
            kwargs (dict) :
                keyword arguments passed to the __init__() method:

        Returns:
            spider :
                instance of spider being running

        """
        spider = super().from_crawler(crawler, *args, **kwargs)
        crawler.signals.connect(spider.spider_opened, signal=signals.spider_opened)
        return spider

    def spider_opened(self, spider):
        """
        This is the class method used by Scrapy Framework to open running spider.

        Args
            spider(spider (Spider object):
             the spider for which this request is intended

        Raises
             CloseSpider( raised from a spider callback):
                when no URL configuration found

        """
        self.elasticsearch_cl = DpElasticsearch(self.settings["ELASTIC_HOST"])
        self.xpaths = self.elasticsearch_cl.get_url_config(self.start_urls[0], self.settings)
        if not self.xpaths:
            raise CloseSpider("No xpaths indexed for the url")
        self.xpaths["index_name"] = self.settings["ELASTIC_INDEX"]
        self.xpaths["content_type"] = self.content_type
        self.headers = {"User-Agent": random.choice(self.settings["USER_AGENT_LIST"])}
        self.cookies_ = cookies_utils.get_cookies(self.xpaths)


    def start_requests(self):
        """
        This method returns an iterable with the first Requests to crawl for this spider. It is called by
        Scrapy when the spider is opened for scraping.
        """
        for url in self.start_urls:
            self.logger.debug("starting  url  %s ", url)
            yield scrapy.Request(
                url,
                dont_filter=True,
                headers=self.headers,
                callback=self.parse,
                cookies=self.cookies_,
            )

    def parse(self, response):
        """
        This is the default callback used by Scrapy Framework to process downloaded responses.
        It extracts links from all start_urls and follow each URL  by sending a request.

        Args:
            response (response (Response object) – the response being processed):
                    html content to parse

        Returns:
            request :
                Iterable of Requests

        """
        self.logger.debug("a response arrived from %s ", response.url)
        url_html_blocks = html_parser.get_html_block_links(response, self.xpaths)
        self.logger.debug(
            "scraped html blocks %s from starting page", (url_html_blocks)
        )
        first_time_seen_links = self.elasticsearch_cl.search_urls_by_country_type(
            url_html_blocks, self.xpaths
        )
        self.logger.debug("first time seen urls  %s ", len(first_time_seen_links))
        for url in first_time_seen_links:
            article_info = next(
                (data for data in url_html_blocks if data["url"] == url), None
            )
            self.logger.debug("send request for url %s", response.urljoin(url))
            yield scrapy.Request(
                response.urljoin(url),
                callback=self.parse_static,
                headers=self.headers,
                cookies=self.cookies_,
                cb_kwargs=dict(data=article_info),
            )

    def parse_static(self, response, data):
        """
        This is the specified callback used by Scrapy to process downloaded responses.

        Args:
            response (response (Response object) – the response being processed)
             content to parse

            data : dict(String)
                Python dict in the following format:
                   data{
                   'title' : <title of the article>
                   'posted_date' : <published date of article >
                   }

        Returns:
            Dict : (Iterable of items)
                Python dict in the following format:
                {
                'link' : <link URL>
                'title' : <title of the article>
                'statement' : <statement content of the article >
                'posted_date' :< published date of the article>
                'indexed_date' :<indexed date of the article >
                'country' : <country name>
                'parent_url' : <parent url (country overview page URL)>
                'content_type' : response content type>
              }

        """
        self.logger.debug("start parsing  middle page from %s !", response.url)
        if data["posted_date"] is None:
            data["posted_date"] = response.xpath(self.xpaths["posted_date"]).get()
        data["url"] = response.url
        url = response.xpath(self.xpaths["link_follow"]).get()
        if url:
            yield scrapy.Request(
                response.urljoin(url),
                callback=self.parse_doc,
                headers=self.headers,
                cb_kwargs=dict(data=data),
            )
        else:
            self.logger.debug("start parsing  item from %s !", response.url)
            Item_loader = item_loader.loader(response, data, self.xpaths,None)
            Item_loader.add_value("country", self.xpaths["name"])
            Item_loader.add_value("parent_url", self.start_urls[0])
            Item_loader.add_value(
                "indexed_date", (datetime.now()).strftime("%Y-%m-%d %H:%M:%S")
            )
            Item_loader.add_value("content_type", self.content_type)
            yield Item_loader.load_item()

    def parse_doc(self, response, data):
        """This is the specified callback used by Scrapy to process downloaded pdf.

        Args:
            response : response (Response object) – the response being processed
                       content to parse

            data  : dict(String)
                Python dict in the following format:
                   data{
                   'title' : <title of the article>
                   'posted_date' : <article published date>
                   }

        Returns:
            Dict : { Iterable of items}
            Python dict in the following format:
              {
                'link' : <article URL>
                'title' : <title of the article>
                'statement' : <article statement content>
                'posted_date' :<article published date>
                'indexed_date' :<article indexed date>
                'country' : <country name>
                'parent_url' : <parent url (country overview page URL)>
                'content_type' : response content type>
              }

        """
        self.logger.debug("start parsing file %s ", response.url)
        item = statementitem_loader.loader(response, data, self.xpaths)
        item["content_type"] = self.content_type
        item["indexed_date"] = (datetime.now()).strftime("%Y-%m-%d %H:%M:%S")
        item["country"] = self.xpaths["name"]
        item["parent_url"] = self.start_urls[0]
        item["url"] = response.url
        yield item

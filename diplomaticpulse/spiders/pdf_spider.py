"""
This module implements a spider to use for scraping countries articles
(PDF and Images html content).

e.g: https://www.mofa.gov.lr/public2/2content.php?sub=23&related=7&third=23&pg=sp&pt=Speeches
"""
from datetime import datetime
import random
import scrapy
from scrapy.spiders import CrawlSpider
from scrapy import signals
from scrapy.utils.project import get_project_settings
from scrapy.exceptions import CloseSpider
from diplomaticpulse.db_elasticsearch.db_es import DpElasticsearch
from diplomaticpulse.parsers import html_parser
from diplomaticpulse.misc import cookies_utils, utils
from diplomaticpulse.dp_loader import statementitem_loader


class PdfSpider(CrawlSpider):
    """
    This spider is a subclass of scrapy.spiders.Spider, which indirects its handling of
    the start_urls and subsequently extracted and followed URLs. It is designed to handle
    PDF/Images websites contents.

    Attributes
        url (string) : country's overview article page,e.g: https://www.foreignminister.gov.au/.
        args (list) : arguments passed to the __init__() method
        kwargs (dict) : keyword arguments passed to the __init__() method:

    """

    # spider name
    name = "pdf"

    def __init__(self, url, *args, **kwargs):
        """
        Create a new instance of  PdfSpider

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
        self.tracker = None
        self.elasticsearch = None
        self.xpaths = None
        self.cookies = None
        self.headers = None
        self.elasticsearch_cl = None
        self.extensions = [".pdf"]

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
        self.xpaths = self.elasticsearch_cl.get_url_config(
            self.start_urls[0], self.settings
        )
        if not self.xpaths:
            raise CloseSpider("No xpaths indexed for the url")

        self.xpaths["index_name"] = self.settings["ELASTIC_INDEX"]
        self.headers = {"User-Agent": random.choice(self.settings["USER_AGENT_LIST"])}
        self.cookies = cookies_utils.get_cookies(self.xpaths)


    def start_requests(self):
        """
        This method returns an iterable with the first Requests to crawl for this spider. It is called by
        Scrapy when the spider is opened for scraping.
        """
        for url in self.start_urls:
            yield scrapy.Request(
                url, callback=self.parse, headers=self.headers, cookies=self.cookies
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

        self.logger.debug("parsing url %s request response ", response.url)
        url_html_blocks = html_parser.get_html_block_links(response, self.xpaths)
        first_time_seen_links = self.elasticsearch_cl.search_urls_by_country_type(
            url_html_blocks, self.xpaths
        )
        self.logger.debug("first time seen urls  %s ", len(first_time_seen_links))
        self.logger.debug(
            "scraped html blocks %s from starting page", len(url_html_blocks)
        )
        for url in first_time_seen_links:
            article_info = next(
                (data for data in url_html_blocks if data["url"] == url), None
            )
            if utils.get_url_extension(url) in self.extensions:
                self.logger.debug("sending request of url %s", url)
                yield scrapy.Request(
                    url,
                    callback=self.parseitem,
                    cb_kwargs=dict(data=article_info),
                    headers=self.headers,
                    cookies=self.cookies
                )

    def parseitem(self, response, data):
        """
        This is the specified callback used by Scrapy to process downloaded responses.

        Parameters:
            response : response (Response object) – the response being processed

            data  : dict(String)
                    Python dict in the following format:
                   data{
                   'title' : <title of the article>
                   'posted_date' : <article published date>
                   }

        Returns:
            Dict : ( Iterable of items)
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

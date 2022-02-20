"""
This module implements a spider to use
for scraping countries articles (static html content).
e.g: https://www.foreignminister.gov.au/ .
"""
from datetime import datetime
import random
import scrapy
from scrapy import signals
from scrapy.utils.project import get_project_settings
from scrapy.exceptions import CloseSpider
from diplomaticpulse.db_elasticsearch.getUrlConfigs import DpElasticsearch
from diplomaticpulse.parsers import html_parser
from diplomaticpulse.loader import itemLoader
from diplomaticpulse.misc import errback_http, cookies_utils


class HtmlSpider(scrapy.spiders.Spider):
    """
    This spider is a subclass of scrapy.spiders.Spider, which indirects its handling of
    the start_urls and subsequently extracted and followed URLs. It is designed to handle
    static website's content.
    """

    # spder name
    name = "static"

    def __init__(self, url, *args, **kwargs):
        """
        Create a new instance of  HtmlSpider

        Args
            url (string) :
                country's overview article page,e.g: https://www.foreignminister.gov.au/.
            *args (list) :
                arguments passed to the __init__() method
            **kwargs (dict) :
                keyword arguments passed to the __init__() method:

        """

        self.settings = None
        self.elasticsearch = None
        self.xpaths = None
        self.cookies = None
        self.headers = None
        self.content_type = "static"
        self.start_urls = [url]

    @classmethod
    def from_crawler(cls, crawler, *args, **kwargs):
        """
        This is the class method used by Scrapy framework to create a running spider.

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
            crawler(spider (Spider object):
             the spider for which this request is intended

        Raises
             CloseSpider( raised from a spider callback):
                when no URL info found

        """
        self.settings = get_project_settings()
        self.elasticsearch = DpElasticsearch(self.settings["ELASTIC_HOST"])
        self.xpaths = self.elasticsearch.get_url_config(
            self.start_urls[0], self.settings
        )
        if not self.xpaths:
            raise CloseSpider("No xpaths indexed for the url")

        self.xpaths["index_name"] = self.settings["ELASTIC_INDEX"]
        self.headers = {"User-Agent": random.choice(self.settings["USER_AGENT_LIST"])}
        self.cookies = cookies_utils.get_cookies(self.xpaths)


    def start_requests(self):
        """
        This method must return an iterable with the first Requests to crawl for this spider.
        It is called by Scrapy Framework after the spider is opened for scraping.
        """

        for url in self.start_urls:
            self.logger.debug("starting url %s ", url)
            yield scrapy.Request(
                url, headers=self.headers, cookies=self.cookies, callback=self.parse
            )

    def parse(self, response):
        """
        This is the default callback used by Scrapy Framework to process downloaded responses.
        It extracts links from all start_urls and follow each URL  by sending a request.

        Args:
            response (response (Response object) – the response being processed):
                    html content to parse

        """
        self.logger.debug("parsing url %s request response  ", response.url)
        url_html_blocks = html_parser.get_html_block_links(response, self.xpaths)
        self.logger.debug(
            "scraped html blocks  %s from starting page", len(url_html_blocks)
        )
        first_time_seen_links = self.elasticsearch.search_urls_by_country_type(
            url_html_blocks, self.xpaths
        )
        self.logger.info("first time seen urls  %s ", len(first_time_seen_links))
        for url in first_time_seen_links:
            article_info = next(
                (data for data in url_html_blocks if data["url"] == url), None
            )
            self.logger.debug("sending request of url %s", url)
            # request
            yield scrapy.Request(
                response.urljoin(url),
                callback=self.parseitem,
                cookies=self.cookies,
                errback=errback_http.errback_httpbin,
                headers=self.headers,
                cb_kwargs=dict(data=article_info),
            )

    def parseitem(self, response, data):
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

        yield:
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
        self.logger.debug("start parsing  item from %s !", response.url)
        Item_loader = itemLoader.itemloader(response, data, self.xpaths)
        Item_loader.add_value("country", self.xpaths["name"])
        Item_loader.add_value("parent_url", self.start_urls[0])
        Item_loader.add_value(
            "indexed_date", (datetime.now()).strftime("%Y-%m-%d %H:%M:%S")
        )
        Item_loader.add_value("content_type", self.content_type)
        yield Item_loader.load_item()

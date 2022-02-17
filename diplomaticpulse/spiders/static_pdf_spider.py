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
from diplomaticpulse.db_elasticsearch.getUrlConfigs import DpElasticsearch
from diplomaticpulse.misc import cookies_utils, utils
from diplomaticpulse.parsers import html_parser
from diplomaticpulse.status_tracker.status_tracker import WebsiteTracker

from diplomaticpulse.item_loader import static_itemloader, pdf_itemloader


class HtmlDocSpider(scrapy.spiders.CrawlSpider):
    """
    This spider is a subclass of scrapy.spiders.Spider, which indirects its handling of
    the start_urls and subsequently extracted and followed URLs. It is designed to handle combined PDF/Static contents.

    """

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
        self.url_website_status = {}
        self.tracker = None
        self.elasticsearch = None
        self.xpaths = None
        self.cookies = None
        self.headers = None
        self.dic_website_status = None
        self.elasticsearch_cl = None
        self.cookies_ = none

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
        crawler.signals.connect(spider.spider_closed, signal=signals.spider_closed)
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
        self.dic_website_status = {}
        self.elasticsearch_cl = DpElasticsearch(self.settings["ELASTIC_HOST"])
        self.tracker = WebsiteTracker(self.settings["ELASTIC_HOST"])
        self.xpaths = self.elasticsearch_cl.get_url_config(self.start_urls[0], self.settings)
        if not self.xpaths:
            raise CloseSpider("No xpaths indexed for the url")
        self.xpaths["index_name"] = self.settings["ELASTIC_INDEX"]
        self.xpaths["content_type"] = self.content_type
        self.headers = {"User-Agent": random.choice(self.settings["USER_AGENT_LIST"])}
        self.cookies_ = cookies_utils.get_cookies(self.xpaths)

    def spider_closed(self, spider):
        """
        This method must return an iterable with the first Requests to crawl for this spider.
        It is called by Scrapy Framework after the spider is opened for scraping

        Returns:
            request: Iterable of Request

        """
        status = {}
        for url in self.url_website_status.items():
            status[url] = dict(
                code=self.url_website_status[url],
                url=url,
                name=self.xpaths["name"],
                spider=self.content_type,
                url_parent=self.start_urls[0],
            )
        self.tracker.update_website_status(status)

    def start_requests(self):
        """
        This method must return an iterable with the first Requests to crawl for this spider.
        It is called by Scrapy Framework after the spider is opened for scraping

        Returns:
            request: Iterable of Request

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
        self.url_website_status[response.url] = 10600 if not url_html_blocks else 200
        self.logger.debug(
            "scraped html blocks %s from starting page", len(url_html_blocks)
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
            Dict : (Iterable of Items)
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
            # self.url_website_status[response.url] = 200 if statement else 10700
            Item_loader = static_itemloader.itemloader(response, data, self.xpaths)
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
            Dict : { Iterable of Items}
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
        self.logger.info("start parsing file %s ", response.url)
        item = pdf_itemloader.itemloader(response, data, self.xpaths)
        item["content_type"] = self.content_type
        item["indexed_date"] = (datetime.now()).strftime("%Y-%m-%d %H:%M:%S")
        item["country"] = self.xpaths["name"]
        item["parent_url"] = self.start_urls[0]
        item["url"] = utils.check_url(response.url)
        self.url_website_status[response.url] = 200 if item["statement"] else 10700
        yield item

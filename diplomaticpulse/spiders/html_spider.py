"""
This module implements a spider to use
for scraping countries articles (static html content).
e.g: https://www.foreignminister.gov.au/ .
"""
import scrapy
from scrapy.loader import ItemLoader
from scrapy.loader.processors import TakeFirst, MapCompose
from scrapy.utils.project import get_project_settings
from scrapy.exceptions import CloseSpider
from diplomaticpulse.items import StatementItem
from datetime import datetime
from diplomaticpulse.db.getUrlConfigs import DpElasticsearch
from diplomaticpulse.website_status_tracker.status_tracker import WebsiteTracker
import random
from scrapy import signals
from diplomaticpulse.parsers import dates_parser, html_parser
from diplomaticpulse.misc import (
    errback_http,
    cookies_utils,
    utils
)

class HtmlSpider(scrapy.spiders.Spider):
    """
    This spider is a subclass of scrapy.spiders.Spider, which indirects its handling of
    the start_urls and subsequently extracted and followed URLs. It is designed to handle
    static website's content.
    """

    # spder name
    name = "html"

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

        self.logger.info("HTML Spider version 0.1.252")
        self.settings = get_project_settings()
        self.start_urls = [url]
        self.content_type = "html"
        self.url_website_status = {}

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
        self.es = DpElasticsearch(self.settings["ELASTIC_HOST"])
        self.tracker = WebsiteTracker(self.settings["ELASTIC_HOST"])
        self.xpaths = self.es.get_url_config(self.start_urls[0], self.settings)
        if not self.xpaths:
            raise CloseSpider("No xpaths indexed for the url")

        self.xpaths["index_name"] = self.settings["ELASTIC_INDEX"]
        self.headers = {"User-Agent": random.choice(self.settings["USER_AGENT_LIST"])}
        self.cookies = cookies_utils.get_cookies(self.xpaths)

    def spider_closed(self, spider):
        """
        This method is called when the spider being running is closing.

        Args
            spider (spider (Spider object):
                the spider for which this request is intended

        Returns:
            updates each url website status if any.

        """
        status = {}
        for url in self.url_website_status:
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
            self.logger.info("starting url %s ", url)
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

        Returns:
            request :
                Iterable of Requests

        """
        self.logger.info("parsing url %s request response  ", response.url)
        url_html_blocks = html_parser.get_html_block_links(response, self.xpaths)
        self.logger.info(
            "scraped html blocks  %s from starting page", len(url_html_blocks)
        )
        first_time_seen_links = self.es.search_urls_by_country_type(
            url_html_blocks, self.xpaths
        )
        self.logger.info("first time seen urls  %s ", len(first_time_seen_links))
        self.url_website_status[response.url] = 10600 if not url_html_blocks else 200
        for url in first_time_seen_links:
            article_info = next(
                (data for data in url_html_blocks if data["url"] == url), None
            )
            self.logger.info("sending request of url %s", url)
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
        self.logger.info("start parsing  item from %s !", response.url)
        Item_loader = ItemLoader(item=StatementItem(), response=response)
        Item_loader.default_input_processor = MapCompose(str())
        Item_loader.default_output_processor = TakeFirst()
        Item_loader.add_value("content_type", self.content_type)
        Item_loader.add_value("country", self.xpaths["name"])
        Item_loader.add_value(
            "indexed_date", (datetime.now()).strftime("%Y-%m-%d %H:%M:%S")
        )
        Item_loader.add_value("posted_date", dates_parser.get_date(data, response, self.xpaths))
        Item_loader.add_value("url", utils.check_url(response.url))
        Item_loader.add_value("parent_url", self.start_urls[0])
        Item_loader.add_value("title", html_parser.get_title(data["title"], response, self.xpaths))
        statement = html_parser.get_html_response_content(
            response, self.xpaths["statement"]
        )
        Item_loader.add_value("statement", statement)
        self.url_website_status[response.url] = 200 if statement else 10700
        yield Item_loader.load_item()

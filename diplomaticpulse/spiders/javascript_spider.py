"""
This module implements a spider for scraping countries diplomatic statements.
e.g: https://mfa.gov.il/MFA/PressRoom/2021/Pages/default.aspx
"""
from datetime import datetime
import random
from scrapy import signals
import scrapy
from scrapy.utils.project import get_project_settings
from scrapy.exceptions import CloseSpider
from scrapy_selenium import SeleniumRequest
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from diplomaticpulse.loader import bs4Loader
from diplomaticpulse.db_elasticsearch.getUrlConfigs import DpElasticsearch
from diplomaticpulse.misc import (
    cookies_utils
)
from diplomaticpulse.parsers import  beautifulsoup_parser


class JavascriptSpider(scrapy.Spider):
    """
    This spider is a subclass of scrapy.spiders.Spider, which indirects its handling of
    the start_urls and subsequently extracted and followed URLs.
    It is designed to handle dynamic website content.

    """

    # spider name
    name = "javascript"

    def __init__(self, url, *args, **kwargs):
        """
        Create a new instance of  JavascriptSpider

        Args
            url (string) :
                country's overview article page,e.g: https://www.foreignminister.gov.au/.
        """
        self.start_urls = [url]
        self.settings = get_project_settings()
        self.content_type = "javascript"
        self.elasticsearch = None
        self.xpaths = None
        self.cookies = None
        self.headers = None
        self.elasticsearch_cl = None
        self.web_driver = None
        self.options = None

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
        crawler.signals.connect(spider.spider_closed, signal=signals.spider_closed)
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
        self.headers = {"User-Agent": random.choice(self.settings["USER_AGENT_LIST"])}
        self.options = Options()
        self.options.add_argument("--headless")
        self.options.add_argument("--disable-gpu")
        self.web_driver = webdriver.Chrome(chrome_options=self.options)
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
        self.web_driver.quit()

    def start_requests(self):
        """
        This method returns an iterable with the first Requests to crawl for this spider. It is called by
        Scrapy when the spider is opened for scraping.
        """
        for url in self.start_urls:
            self.logger.info("starting  url  %s ", url)
            yield SeleniumRequest(
                url=url,
                dont_filter=True,
                headers=self.headers,
                wait_time=10,
                callback=self.parse,
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
        url_html_blocks = beautifulsoup_parser.get_text_from_html_block(
            response.url, self.xpaths, self.web_driver
        )
        self.logger.info("links from overview page: %s ", len(url_html_blocks))
        first_time_seen_urls = self.elasticsearch_cl.search_urls_by_country_type(
            url_html_blocks, self.xpaths
        )
        self.logger.info("first time seen urls %s: ", len(first_time_seen_urls))
        for url in first_time_seen_urls:
            article_info = next(
                (
                    article_info
                    for article_info in url_html_blocks
                    if article_info["url"] == url
                ),
                None,
            )
            self.logger.info("sending request of url %s", response.urljoin(url))
            yield scrapy.Request(
                response.urljoin(url),
                callback=self.parseitem,
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
            Dict : (Iterable of items)
                Python dict in the following format:
                {
                'link' : <link URL>
                'title' : <title of the article>
                'statement' : <article content of the article >
                'posted_date' :< published date of the article>
                'indexed_date' :<indexed date of the article >
                'country' : <country name>
                'parent_url' : <parent url (country overview page URL)>
                'content_type' : response content type>
              }

        """
        self.logger.info("start building item object of url %s ", response.url)
        Item_loader =  bs4Loader.loader(response, data, self.xpaths, self.web_driver)
        Item_loader.add_value("parent_url", self.start_urls[0])
        Item_loader.add_value("content_type", self.content_type)
        Item_loader.add_value("country", self.xpaths["name"])
        Item_loader.add_value(
            "indexed_date", (datetime.now()).strftime("%Y-%m-%d %H:%M:%S")
        )
        yield Item_loader.load_item()

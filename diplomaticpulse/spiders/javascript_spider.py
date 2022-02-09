"""
This module implements a spider to use
for scraping countries articles (Dynamic-Javascript html content).

e.g: https://mfa.gov.il/MFA/PressRoom/2021/Pages/default.aspx
"""
import scrapy
from scrapy.loader import ItemLoader
from scrapy.loader.processors import TakeFirst, MapCompose
from scrapy.utils.project import get_project_settings
from scrapy.exceptions import CloseSpider
from diplomaticpulse.items import StatementItem
from datetime import datetime
from diplomaticpulse.db.getUrlConfigs import DpElasticsearch
from diplomaticpulse.utilities import (
    cookies_utils,
    utils,
)
from diplomaticpulse.parsers import pdf_parser, html_parser, beautifulsoup_parser
import urllib.parse
import urllib.request
import random
from scrapy_selenium import SeleniumRequest
from scrapy import signals
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from diplomaticpulse.website_status_tracker.status_tracker import WebsiteTracker


class SeleniumSpider(scrapy.Spider):
    """
    This spider is a subclass of scrapy.spiders.Spider, which indirects its handling of
    the start_urls and subsequently extracted and followed URLs. It is designed to handle dynamic website's content.

    """

    # spider name
    name = "javascript_selenium"

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
        self.content_type = "javascript_selenium"
        self.settings = get_project_settings()
        self.logger.info("connecting to %s ", self.settings["ELASTIC_HOST"])
        self.start_urls = [url]
        self.head = False

    @classmethod
    def from_crawler(cls, crawler, *args, **kwargs):
        """This is the class method used by Scrapy to create your spiders.

        Args
            crawler (Crawler instance) :
                crawler to which the spider will be bound
            args (list) :
                arguments passed to the __init__() method
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
        This is the class method used by Scrapy to create your spiders.

        Args
            crawler(spider (Spider object):
             the spider for which this request is intended

        Raises
             CloseSpider( raised from a spider callback):
                when no data for running url

        Returns:
            spider :
                instance of running spider

        """
        self.dic_website_status = {}
        self.es = DpElasticsearch(self.settings["ELASTIC_HOST"])
        self.tracker = WebsiteTracker(self.settings["ELASTIC_HOST"])
        self.xpath_configs = self.es.get_url_config(self.start_urls[0], self.settings)
        if not self.xpath_configs:
            raise CloseSpider("No xpaths indexed for the url")
        self.xpaths = self.xpath_configs[0]["_source"]
        self.head = self.xpaths["head"]
        self.xpaths["index_name"] = self.settings["ELASTIC_INDEX"]
        self.headers = {"User-Agent": random.choice(self.settings["USER_AGENT_LIST"])}
        self.options = Options()
        self.options.add_argument("--headless")
        self.options.add_argument("--disable-gpu")
        self.web_driver = webdriver.Chrome(chrome_options=self.options)
        self.cookies_ = cookies_utils.get_cookies(self.xpaths)

    def spider_closed(self, spider):
        """
        Called when the spider being running closes.

        Args
            spider (spider (Spider object):
                the spider for which this request is intended

        """
        self.tracker.update_website_status(self.dic_website_status)
        self.web_driver.quit()

    def start_requests(self):
        """This method must return an iterable with the first Requests to crawl for this spider.
           It is called by Scrapy when the spider is opened for scraping

        Returns:
            request: Iterable of Request

        """
        for url in self.start_urls:
            self.logger.info("starting  url  %s ", url)
            if not self.head:
                yield SeleniumRequest(
                    url=url,
                    dont_filter=True,
                    headers=self.headers,
                    wait_time=10,
                    callback=self.parse,
                )
            else:
                yield SeleniumRequest(
                    url=url,
                    dont_filter=True,
                    headers=self.headers,
                    method="HEAD",
                    wait_time=10,
                    callback=self.parse,
                    cookies=self.cookies_,
                )

    def parse(self, response):
        """
        This is the default callback used by Scrapy to process downloaded responses,
         when their requests don’t specify a callback.
        Extract urls links from  start_urls and follow urls by sending request

        Args:
        response (response (Response object) – the response being process):
                    content to parse

        Returns:
            request :
                Iterable of Requests

        """
        self.logger.info("a response arrived from %s ", response.url)
        self.dic_website_status[response.url.strip("'/")] = dict(
            code=200,
            url=response.url,
            name=self.xpaths["name"],
            spider=self.content_type,
            url_parent=self.start_urls[0],
        )
        dict_html_blocks = beautifulsoup_parser.get_data_from_blocks(
            response, self.xpaths, self.web_driver
        )
        self.logger.info("--> links from overview page: %s ", len(dict_html_blocks))
        first_time_seen_links = self.es.search_urls_by_country_type(
            dict_html_blocks, self.xpaths
        )
        self.logger.info(" first time seen   urls %s:: ", len(first_time_seen_links))
        _code = 10600 if not dict_html_blocks else 200
        self.dic_website_status[response.url] = dict(
            code=_code,
            url=response.url,
            name=self.xpaths["name"],
            spider=self.content_type,
            url_parent=self.start_urls[0],
        )
        for url in first_time_seen_links:
            page_data = next(
                (data for data in dict_html_blocks if data["url"] == url), None
            )
            self.logger.info("send request for url %s", response.urljoin(url))
            if not self.head:
                yield scrapy.Request(
                    response.urljoin(url),
                    callback=self.parseitem,
                    headers=self.headers,
                    cb_kwargs=dict(data=page_data),
                )
            else:
                yield scrapy.Request(
                    response.urljoin(url),
                    callback=self.parseitem,
                    method="HEAD",
                    headers=self.headers,
                    cookies=self.cookies_,
                    cb_kwargs=dict(data=page_data),
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
        if response.headers["Content-Type"].startswith(b"application/pdf"):
            self.logger.info("start parsing file  %s ", response.url)
            item = StatementItem()
            raw = pdf_parser.parse_pdfminer(response.url, self.xpaths["ssl"])
            statement = raw["statement"] if raw else None
            item["statement"] = html_parser.format_text(statement)
            item["statement"] = html_parser.clean_html(statement, self.xpaths["tag"])
            item["statement"] = html_parser.format_text(item["statement"])
            title = html_parser.get_title(data["title"], response, self.xpaths)
            item["title"] = title if title else item["statement"][:200]
            posted_date = html_parser.get_date_from_pdf(
                data, raw, item["statement"], title
            )
            item["posted_date"] = posted_date
            item["content_type"] = self.content_type
            item["indexed_date"] = (datetime.now()).strftime("%Y-%m-%d %H:%M:%S")
            item["country"] = self.xpaths["name"]
            item["url"] = urllib.parse.unquote(response.url)
            item["parent_url"] = self.start_urls[0]
            _code = 200 if item["statement"] and item["title"] else 10700
            self.dic_website_status[response.url] = dict(
                code=_code,
                url=response.url,
                name=self.xpaths["name"],
                spider=self.content_type,
                url_parent=self.start_urls[0],
            )
            yield item

        else:
            self.logger.info("start parsing item url  %s ", response.url)
            Item_loader = ItemLoader(item=StatementItem(), response=response)
            statement, posted_date = beautifulsoup_parser.get_data_from_response(
                response, data, self.xpaths, self.web_driver
            )
            Item_loader.add_value("statement", statement)
            self.logger.info("start parsing  item from %s !", response.url)
            url = utils.check_url(response.url)
            Item_loader.default_input_processor = MapCompose(str())
            Item_loader.default_output_processor = TakeFirst()
            Item_loader.add_value("url", url)
            Item_loader.add_value("parent_url", self.start_urls[0])
            Item_loader.add_value(
                "indexed_date", (datetime.now()).strftime("%Y-%m-%d %H:%M:%S")
            )
            Item_loader.add_value("content_type", self.content_type)
            Item_loader.add_value("country", self.xpaths["name"])
            title = html_parser.get_title(data["title"], response, self.xpaths)
            title = title if title else statement[:200]
            Item_loader.add_value("title", title)
            Item_loader.add_value("posted_date", str(posted_date))
            _code = 200 if statement and title else 10700
            self.dic_website_status[response.url] = dict(
                code=_code,
                url=response.url,
                name=self.xpaths["name"],
                spider=self.content_type,
                url_parent=self.start_urls[0],
            )
            yield Item_loader.load_item()

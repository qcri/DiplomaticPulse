"""
This module implements a spider to use
for scraping countries articles (PDF and Images html content).

e.g: https://www.mofa.gov.lr/public2/2content.php?sub=23&related=7&third=23&pg=sp&pt=Speeches
"""
import scrapy
from scrapy.spiders import CrawlSpider
from scrapy.utils.project import get_project_settings
from diplomaticpulse.items import StatementItem
from diplomaticpulse.db.getUrlConfigs import DpElasticsearch
from diplomaticpulse.utilities import (
    errback_http,
    cookies_utils,
    utils,
)
from diplomaticpulse.parsers import pdf_parser, dates_parser, html_parser
import random
from datetime import datetime
from scrapy.exceptions import CloseSpider
from diplomaticpulse.website_status_tracker.status_tracker import WebsiteTracker
from scrapy import signals


class DocSpider(CrawlSpider):
    """
    This spider is a subclass of scrapy.spiders.Spider, which indirects its handling of
    the start_urls and subsequently extracted and followed URLs. It is designed to handle
    PDF/Images website's content.

    Attributes
        url (string) : country's overview article page,e.g: https://www.foreignminister.gov.au/.
        args (list) : arguments passed to the __init__() method
        kwargs (dict) : keyword arguments passed to the __init__() method:

    """

    # spider name
    name = "doc"

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
        self.content_type = "doc"
        self.settings = get_project_settings()
        self.logger.info("connecting to   %s ", self.settings["ELASTIC_HOST"])
        self.start_urls = [url]
        self.extensions = [".pdf"]

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
        self.xpaths["index_name"] = self.settings["ELASTIC_INDEX"]
        self.headers = {"User-Agent": random.choice(self.settings["USER_AGENT_LIST"])}
        self.cookies_ = cookies_utils.get_cookies(self.xpaths)

    def spider_closed(self, spider):
        """
        Called when the spider being running closes.

        Args
            spider (spider (Spider object):
                the spider for which this request is intended

        """
        self.tracker.update_website_status(self.dic_website_status)

    def start_requests(self):
        """
        This method must return an iterable with the first Requests to crawl for this spider.
        It is called by Scrapy when the spider is opened for scraping

        Returns:
            request: Iterable of Request

        """
        for url in self.start_urls:
            self.logger.info("starting  url  %s ", url)
            yield scrapy.Request(
                url, callback=self.parse, headers=self.headers, cookies=self.cookies_
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
        self.logger.info("A response from %s just arrived!", response.url)
        self.dic_website_status[response.url.strip("'/")] = dict(
            code=200,
            url=response.url,
            name=self.xpaths["name"],
            spider=self.content_type,
            url_parent=self.start_urls[0],
        )
        dict_html_blocks = html_parser.scraped_block_links(response, self.xpaths)
        first_time_seen_links = self.es.search_urls_by_country_type(
            dict_html_blocks, self.xpaths
        )
        self.logger.info("first time seen urls  %s ", len(first_time_seen_links))
        _code = 10600 if not dict_html_blocks else 200
        self.dic_website_status[response.url] = dict(
            code=_code,
            url=response.url,
            name=self.xpaths["name"],
            spider=self.content_type,
            url_parent=self.start_urls[0],
        )
        self.logger.info(
            "scraped html blocks %s from starting page", len(dict_html_blocks)
        )
        for url in first_time_seen_links:
            _dict_data = next(
                (data for data in dict_html_blocks if data["url"] == url), None
            )
            if utils.get_url_extension(url) in self.extensions:
                self.logger.info(" send request for url %s", url)
                yield scrapy.Request(
                    url,
                    callback=self.parseitem,
                    cb_kwargs=dict(data=_dict_data),
                    headers=self.headers,
                    cookies=self.cookies_,
                    errback=errback_http.errback_httpbin,
                )

    def parseitem(self, response, data):
        """This is the specified callback used by Scrapy to process downloaded responses.

        Parameters:
            response : response (Response object) – the response being processed

            data  : dict(String)
                    Python dict in the following format:
                   data{
                   'title' : <title of the article>
                   'posted_date' : <article published date>
                   }

        Returns:
            Dict : ( Iterable of Items)
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
        self.logger.info("start parsing file  %s ", response.url)
        item = StatementItem()
        raw = pdf_parser.parse_pdfminer(response.url, None)
        statement = raw["statement"] if raw else None
        item["statement"] = html_parser.format_html_text(statement)
        # item["statement"] = (statement)
        title = html_parser.get_title(data["title"], response, self.xpaths)
        item["title"] = title if title else item["statement"][:200]
        posted_date = dates_parser.get_date_from_pdf(
            data["posted_date"], raw, item["statement"], title
        )
        item["posted_date"] = posted_date
        item["content_type"] = self.content_type
        item["indexed_date"] = (datetime.now()).strftime("%Y-%m-%d %H:%M:%S")
        item["country"] = self.xpaths["name"]
        item["url"] = utils.check_url(response.url)
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

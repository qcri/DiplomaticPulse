"""
This module implements a spider to use
for scraping countries articles  of mixed (static and/or PDF/Images html content).

e.g: https://www.permanentrepresentations.nl/documents/publications/2022/02/01/possibility-to-implement-more-ambitious-national-blending-mandates
"""
import scrapy
from scrapy.exceptions import CloseSpider
from scrapy.utils.project import get_project_settings
from diplomaticpulse.items import StatementItem
from datetime import datetime
from diplomaticpulse.db.getUrlConfigs import DpElasticsearch
import urllib.parse
import random
from scrapy.loader import ItemLoader
from scrapy.loader.processors import TakeFirst, MapCompose
from diplomaticpulse.misc import cookies_utils, utils
from diplomaticpulse.parsers import pdf_parser, html_parser, dates_parser
from diplomaticpulse.website_status_tracker.status_tracker import WebsiteTracker
from scrapy import signals


class HtmlDocSpider(scrapy.spiders.CrawlSpider):
    """
    This spider is a subclass of scrapy.spiders.Spider, which indirects its handling of
    the start_urls and subsequently extracted and followed URLs. It is designed to handle odf and static content.

    """

    name = "html_doc"

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
        self.settings = get_project_settings()
        self.url = urllib.parse.unquote(url).replace('"', "")
        self.start_urls = [url]
        self.content_type = "doc"
        self.skip_extensions = [".doc", ".docx", ".img", ".jpg"]

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
        self.xpaths["content_type"] = self.content_type
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
        """This method must return an iterable with the first Requests to crawl for this spider.
           It is called by Scrapy when the spider is opened for scraping

        Returns:
            request: Iterable of Request

        """
        for url in self.start_urls:
            self.logger.info("starting  url  %s ", url)
            yield scrapy.Request(
                url,
                dont_filter=True,
                headers=self.headers,
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
        dict_html_blocks = html_parser.scraped_block_links(response, self.xpaths)
        self.logger.info(
            "---> scraped html blocks  %s  from starting page", len(dict_html_blocks)
        )
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
        for url in first_time_seen_links:
            _dict_data = next(
                (data for data in dict_html_blocks if data["url"] == url), None
            )
            self.logger.info("send request for url %s", response.urljoin(url))
            yield scrapy.Request(
                response.urljoin(url),
                callback=self.parse_static,
                headers=self.headers,
                cookies=self.cookies_,
                cb_kwargs=dict(data=_dict_data),
            )

            break

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
        self.logger.info("start parsing  middle page from %s !", response.url)
        if not data["posted_date"]:
            data["posted_date"] = response.xpath(self.xpaths["posted_date"]).get()
        data["url"] = response.url

        url = response.xpath(self.xpaths["link_follow"]).get()
        if url and utils.get_language(url) not in self.skip_extensions:
            yield scrapy.Request(
                response.urljoin(url),
                callback=self.parse_doc,
                headers=self.headers,
                cb_kwargs=dict(data=data),
            )
        elif not url:
            self.logger.info("start parsing  item from %s !", response.url)
            self.logger.info("start parsing  item from %s !", response.url)
            Item_loader = ItemLoader(item=StatementItem(), response=response)
            Item_loader.default_input_processor = MapCompose(str())
            Item_loader.default_output_processor = TakeFirst()
            statement = html_parser.get_response_content(
                response, self.xpaths["statement"]
            )
            Item_loader.add_value("statement", statement)
            title = html_parser.get_title(data["title"], response, self.xpaths)
            Item_loader.add_value("title", title)
            posted_date = dates_parser.get_date(data, response, self.xpaths)
            Item_loader.add_value("posted_date", str(posted_date))
            Item_loader.add_value("url", utils.check_url(response.url))
            Item_loader.add_value("parent_url", self.start_urls[0])
            Item_loader.add_value(
                "indexed_date", (datetime.now()).strftime("%Y-%m-%d %H:%M:%S")
            )
            Item_loader.add_value("content_type", self.content_type)
            Item_loader.add_value("country", self.xpaths["name"])
            _code = 200 if statement and title else 10700
            self.dic_website_status[response.url] = dict(
                code=_code,
                url=response.url,
                name=self.xpaths["name"],
                spider=self.content_type,
                url_parent=self.start_urls[0],
            )
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
        self.logger.info("start parsing file  %s ", response.url)
        item = StatementItem()
        raw = pdf_parser.parse_pdfminer(response.url, self.xpaths["ssl"])
        statement = raw["statement"] if raw else None
        item["statement"] = "".join(html_parser.format_html_text(statement))
        title = html_parser.get_title(data["title"], response, self.xpaths)
        item["title"] = title if title else item["statement"][:200]
        posted_date = dates_parser.get_date_from_pdf(
            data["posted_date"], raw["posted_date"], item["statement"], title
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

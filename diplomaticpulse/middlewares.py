"""
 See documentation in:
 https://docs.scrapy.org/en/latest/topics/spider-middleware.html
"""

from scrapy import signals


class DiplomaticpulseSpiderMiddleware(object):
    """
    The spider middleware is a framework of hooks into Scrapy’s spider processing mechanism where
    you can plug custom functionality to process the responses that are sent to Spiders for processing
     and to process the requests and items that are generated from spiders.

    Args
        object (scrapy.spiders.Spider class):
            instance of spider class

    """

    @classmethod
    def from_crawler(cls, crawler):
        """
        This is the class method used by Scrapy to create your spiders.

        Args
            crawler (Crawler instance) :
                crawler to which the spider will be bound

        Returns:
            spider (instance of spider)

        """
        s = cls()
        crawler.signals.connect(s.spider_opened, signal=signals.spider_opened)
        return s

    def process_spider_input(self, response, spider):
        """
        This method is called for each response that goes through the spider middleware and into the spider, for processing.

        Args
            response(response (Response object)):
                the response being processed
            spider (Spider object):
                the spider for which this response is intended

        Returns:
            spider : None
                     spider is running

        """
        return None

    def process_spider_output(self, response, result, spider):
        """
        This method is called with the results returned from the Spider, after it has processed the response.

        Args
            response (response (Response object) ;
                the response which generated this output from the spider
            result (an iterable of Request objects and item object) :
                the result returned by the spider
            spider (Spider object) :
                the spider whose result is being processed

        Returns:

        """
        for i in result:
            yield i

    def process_spider_exception(self, response, exception, spider):
        # Called when a spider or process_spider_input() method
        # (from other spider middleware) raises an exception.

        # Should return either None or an iterable of Request, dict
        # or Item objects.
        return []
        # pass

    def process_start_requests(self, start_requests, spider):
        """
        Called with the start requests of the spider, and works  similarly to the process_spider_output() method, except that it doesn’t have a response associated.

        Args
            It receives an iterable (in the start_requests parameter) and must return another iterable of Request objects.

        """
        for r in start_requests:
            yield r

    def spider_opened(self, spider):
        spider.logger.info("Spider opened: %s" % spider.name)


class DiplomaticpulseDownloaderMiddleware(object):
    """The downloader middleware is a framework of hooks into Scrapy’s request/response processing.
    It’s a light, low-level system for globally altering Scrapy’s requests and responses.

    Args
        object (scrapy.spiders.Spider class):
            instance of spider being processed

    """

    @classmethod
    def from_crawler(cls, crawler):
        """
        This is the class method used by Scrapy to create your spiders.

        Args
                crawler (Crawler instance) :
                    crawler to which the spider will be bound

        Returns:
             None, return a Response object, return a Request object, or raise IgnoreRequest.

        """
        s = cls()
        crawler.signals.connect(s.spider_opened, signal=signals.spider_opened)
        return s

    def process_request(self, request, spider):
        """This is the class method used by Scrapy to create your spiders.

        Args
                request (Request object) :
                    the request being processed
                spider (Spider object):
                    the spider for which this request is intended

        Returns:
             None, return a Response object, return a Request object, or raise IgnoreRequest.

        """
        return None


class CustomProxyMiddleware(object):
    """This is the class method used to handle proxies"""

    def process_request(self, request, spider):
        # request.meta["proxy"]= "https://???:???@23.105.5.249:29842"
        pass

    def process_response(self, request, response, spider):
        return response

    def process_exception(self, request, exception, spider):
        pass

    def spider_opened(self, spider):
        spider.logger.info("Spider opened: %s" % spider.name)

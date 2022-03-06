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
        This class method is used by Scrapy to create running spider.

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
        This method is called for each response that goes through the spider middleware and into the spider, for processing
        request response.

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
        This method is called with the results from the Spider, after it has processed the request response.

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
        """
          Called when a spider or process_spider_input() method
          (from other spider middleware) raises an exception.

          Should return either None or an iterable of Request, dict
          or Item objects.:
        """

        return []

    def process_start_requests(self, start_requests, spider):
        """
        Called with the start requests of the spider, and works  similarly to the process_spider_output() method, except that it doesn’t have a response associated.

        Args
            It receives an iterable (in the start_requests parameter) and must return another iterable of Request objects.

        """
        for r in start_requests:
            yield r

    def spider_opened(self, spider):
        spider.logger.info("Spider opened: %s",spider.name)


class DiplomaticpulseDownloaderMiddleware(object):
    """
    The downloader middleware is a framework of hooks into Scrapy’s request/response processing.
    Args
        object (scrapy.spiders.Spider class):
            instance of spider being processed

    """

    @classmethod
    def from_crawler(cls, crawler):
        """
        This method is used by Scrapy to create your running spider.

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
        """This method is used by Scrapy to process request.

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
    """This class is  used to handle proxies"""

    def process_request(self, request, spider):
        pass

    def process_response(self, request, response, spider):
        return response

    def process_exception(self, request, exception, spider):
        pass

    def spider_opened(self, spider):
        spider.logger.info("Spider opened: %s" , spider.name)

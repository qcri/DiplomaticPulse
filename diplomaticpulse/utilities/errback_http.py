
def errback_httpbin(self, failure):
    """
      The errback of a request is a function that will be called when an exception is raise while processing it.

      :param failure:
      :return:

    """
    # log all failures
    self.logger.error(repr(failure))

    # in case you want to do something special for some errors,
    # you may need the failure's type:

    if failure.check(HttpError):
        # these exceptions come from misc spider middleware
        # you can get the non-200 response
        response = failure.value.response
        self.logger.error('misc on %s', response.url)

    elif failure.check(DNSLookupError):
        # this is the original request
        request = failure.request
        self.logger.error('DNSLookupError on %s', request.url)

    elif failure.check(TimeoutError, TCPTimedOutError):
        request = failure.request
        self.logger.error('TimeoutError on %s', request.url)


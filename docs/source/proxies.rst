How to use Rotating Proxies
===========================
IP rotation using `rotating proxies`_ library is implemented to take care of possible
proxies use.

.. _rotating proxies: https://www.zyte.com/blog/scrapy-proxy/

You can use you own proxies as follow:

* add your proxies to ``proxy.py``
* enable the proxies using: through ``DOWNLOADER_MIDDLEWARES`` in :mod:`diplomaticpulse.settings`:

  ::

     DOWNLOADER_MIDDLEWARES = {
       'rotating_proxies.middlewares.RotatingProxyMiddleware': 610,
       'rotating_proxies.middlewares.BanDetectionMiddleware': 620
     }

Spiders
========================
We have developed 4 Scrapy spiders for Diplomatic Pulse  (one for each content type) to extract contents from various websites.

To view all spider,you can use command: ``scapy list`` they are:

* :mod:`diplomaticpulse.spiders.static_spider`, handles static html content.
* :mod:`diplomaticpulse.spiders.javascript_spider`, handles dynamic content.
* :mod:`diplomaticpulse.spiders.static_pdf_spider`, handles PDF and Images contents.
* :mod:`diplomaticpulse.spiders.pdf_spider`, handles mixed static html & PDF/Images contents.

There is at least one overview (https://www.foreignminister.gov.au ) page for each country. One country may have one or many
overview pages (multiple URLs).

The crawler (spider) visits the country's overview page then scrapes the existing links, then follows each link to extract
its content (title, date posted, statement); the content is saved into an `elasticsearch`_ database.



..  _elasticsearch: https://github.com/elastic/elasticsearch


Note: One could easily implements a new spider for new html content type.

Important
=================
Our Diplomatic Pulse spiders depend on the underlying format and structure of each websites's page, and when the website's layout changes  or wrong
our spiders tend to break. So succesfull running spiders depends heavily on a correct website's XPATH configuration,
therfore if country's website updates its templates then correct XPATHs should be updated respectively.

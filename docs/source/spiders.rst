Spiders
========================
We have developed 4 Scrapy spiders for Diplomatic pulse  (one for each content type) to extract contents from various websites, you can easily implements a new spider for a new html content type.

To view all spider,you can use command: ``scapy list`` they are:

* :mod:`diplomaticpulse.spiders.static_spider`, for static html content.
* :mod:`diplomaticpulse.spiders.javascript_spider`, for dynamic content.
* :mod:`diplomaticpulse.spiders.static_pdf_spider`, for static and PDF/Images contents.
* :mod:`diplomaticpulse.spiders.pdf_spider`, for PDF/Images contents.

There maybe at least one overview (https://www.foreignminister.gov.au ) page for each country. Though, a country may have more than one
overview page (multiple URLs).

The crawler (spider) visits the country's overview page then scrapes the existing links, then follows each link to extract
its content (title, date posted, statement); the content is saved into an `elasticsearch`_ database.



..  _elasticsearch: https://github.com/elastic/elasticsearch



Succesfull running spiders
=================
Our Diplomatic pulse spiders depend on the underlying format and structure of each websites's page, and when the website's layout changes  or wrong
our spiders tend to break. So succesfull running spiders depends heavily on a correct website's XPATH configuration,
therfore if country's website updates its templates then correct XPATHs should be updated respectively.

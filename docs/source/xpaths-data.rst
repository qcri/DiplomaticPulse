Website's XPATHs configuration
************************************
Country website (Overview) page
===============================
There is at least one overview page for each country, e.g: Australian: https://www.foreignminister.gov.aux
One country may have one or many overview pages (multiple URLs).
The crawler visits the country's overview page then scrapes the existing articles links, then follows each link to extract
its content (title, date posted, statement); the content is saved into an `elasticsearch`_ database.

.. _elasticsearch: https://www.elastic.co/guide/index.html

XPATHs Configuration Data
=========================
On launching the Diplomatic Pulse containers, the script ``setup.sh`` creates two Elasticsearch indexes on the fly: `countries`_
and `urlconfig`_; the indicies names are shown in ``.env`` file and could be easily renamed.

.. _countries:

countries
---------
The elasticsearch index: `countries`_ contains the  list names of countries. It is populated with the json data in `countries.json`_.

Metadata

* name, name of the country, for example: Australia.
* status, complete if all country's xpaths are valid, else pending.
* URL counter, total number of indexed URLs for the country.

.. _urlconfig:

urlconfig
---------
The eleasticsearch index: `urlconfig`_ contains the list of URL's xpath configuration. It is populated with the data
`urlconfig.json`_.

Metadata

* name, name of the country:
* URL, country's overview page link.
* posted date, published article's xpath.
* content_type, content type (spider name) .
* global,  html block (which contains title & article link, date posted) xpaths (extracted from overview page).
* link, article's link xpath (URL).
* title, acticle's title xpath.
* tag, Unawanted html element tag's xpath.
* us_date_format, US date format if exist.

.. _countries.json:

countries.json
--------------
``{"index": {"_id": "5cb4c9d828175ed3931ec52305b32f47173a8e04"}} "name": "Belgium"}``

.. _urlconfig.json:

urlconfig.json
--------------
``{"index": {"_id": "4917fefc12484a580347ebab907cfa05d3cd8132"}}``

``{"content_type": "static", "global": "//div[has-class(\"node-feed-item\")]", "url": "https://newyorkun.diplomatie.belgium.be",``
``"us_date_format": null, "posted_date": "//div[has-class(\"meta submitted\")]//text()", "link": "//h3/a/@href", "tag": null,``
``"title": "//h3/a/text()", "name": "Belgium", "link_follow": null, "statement": "//div[has-class(\"field-item even\")]"}``

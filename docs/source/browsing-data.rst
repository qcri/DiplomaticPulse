Browsing extracted indexed data
*******************************
In each visited country's webpage, the content is extracted and indexed into elasticsearch index ``dppa.st``.
The indexed data can be browsed using the `Dejavu`_ (free and open source web UI for Elasticsearch).

Assuming all containers are running on your local machine, go to:

* http://localhost:1358
* connect to index ``dppa.st`` with http://localhost:9200

.. _Dejavu: https://opensource.appbase.io/dejavu/

Diplomatic pulse  data quality
===============================

Diplomatic pulse checkes and cleans all data before indexed;

The Diplomatic pulse takes care of:

* unwanted html element tags: The scrapy spider middleware is used to process a response body to remove a configurable
  elements from html. The unwanted tags are set in the ``tag`` field shown in the ``urlconfig index``.
* spider middleware also guarantees that a content is only indexed once,i.e no duplication allowed.

Monitoring of Diplomatic pulse
===============================
Diplomatic pulse uses the Scrapy UI which runs on ``port 6800``, the role is to observe each crawler job history and status.

you can access UI here:

http://localhost:6800


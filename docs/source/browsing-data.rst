Browsing extracted indexed data
*******************************
Each visited country's webpage, the content is extracted and indexed into elasticsearch index ``dppa.st``.
The indexed data can be browsed using the `Dejavu`_ (free and open source web UI for Elasticsearch).

Assuming all containers are running on your local machine, go to:

* http://localhost:1358
* connect to index ``dppa.st`` with http://localhost:9200

.. _Dejavu: https://opensource.appbase.io/dejavu/

Diplomatic pulse  data quality
===============================

Diplomatic pulse data quality checked and cleaned before indexed;

The Diplomatic pulse takes care of:

* unwanted html element tags: The scrapy spider middleware is used to process a response body by removing a (configurable) set of
  elements from it. The unwated tags are set in the tag field shown in the urlconfig index.
* Spider middleware also guarantees that a content is only indexed once, no duplication allowed.
* handling various dates formats: the diplmatic Pulse handles all types of date formats including the US format
* raise exceptions: The diplmatic Pulse raises warning when crawler fails to read the content.

Monitoring of Diplomatic pulse
===============================
Diplomatic pulse uses the Scrapy UI which running on port 6800 to observe each crawler job history and status.

you can browse using:

http://localhost:6800


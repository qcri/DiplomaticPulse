Indexing data
*************
On launching Diplomatic pulse containers, the script ``setup.sh`` creates an empty index on the fly:``dppa.st``; There is a one
Crawler Spider instance for each country's overview page.

At the start, the crawler visits country's overview page, extracts and follows all statements links to scrape their contents title,
article statement, posted date. For each country web page, the contents are extracted and indexed into the Elasticsearch
index ``dppa.st``.

dppa.st
=======
* content_type: website content type(html/dyanimc/json/pdf/image).
* country: name of the country (eg: Australia).
* indexed_date: indexed timestamp, when the content was indexed.
* language: content language.
* parent_url: diplomatic country overview webpage URL.
* posted_date: published date (date posted) of the article.
* statement: content of the article (statement).
* title: title of content of the article.
* url: URL of the article.

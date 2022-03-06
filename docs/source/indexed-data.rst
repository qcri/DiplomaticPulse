Indexing data
*************
On launching Diplomatic pulse docker containers, the script ``setup.sh`` creates an empty index ``dppa.st`` on the fly; there is a one
Crawler Spider instance for each country's overview page.

At the start, the crawler visits country's overview page, extracts and follows all statements links to scrape their contents: ``title,
statement of the article, posted date``. For each country web page, the contents are extracted and indexed into the Elasticsearch index  which is``dppa.st``.

dppa.st index
=======
* content_type: website content type(html/dyanimc/json/pdf/image).
* country: name of the country (eg: Australia).
* indexed_date: indexed timestamp.
* language: content language.
* parent_url: overview webpage URL.
* posted_date: published date (date posted) of the article.
* statement: content of the article.
* title: title of the article.
* url: URL of the article.

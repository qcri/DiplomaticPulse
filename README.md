
<h1  style="font-size:60px;"align="center">
  <b>Diplomatic pulse</b>
</h1>
<p  style="font-size:40px;"align="center">
  <b>Crawling, Indexing, and Storage System for United Nations Member states Press Statements in Real Time.</b>
</p>


## Overview

This repository should provide much of the structure and parsing code needed to crawl and scrape various
countries Ministry of Foreign Affairs (MFA) web pages contents with very little effort. On launching our
Diplomatic pulse Scrapy crawlers, the Diplomatic pulse clones our back end data: XPATHs of each country's website 
layout to crawl and scrape the html contents. 


## Requirements
- Python 3.6+
- Docker version >=19.03.12

## Installing and executing 
A docker-compose.yml file is used, once you have Docker installed and started, change to the project directory and follow: 
```bash
git clone git@github.com:qcri/DiplomaticPulse.git
cd DiplomaticPulse
docker-compose up
```

See the install section in the documentation at https://diplomaticpulse.qcri.org/docs/installation.html for more details



## Browsing extracted indexed data

In each visited country's webpage, the content is extracted and indexed into elasticsearch index ``dppa.st``.
The indexed data can be browsed using the `Dejavu` (free and open source web UI for Elasticsearch).

Assuming all containers are running on your local machine, go to:

* http://localhost:1358
* connect to index ``dppa.st`` with ``http://localhost:9200``

<p align="center">
  <img width="95%" src="https://diplomaticpulse.qcri.org/static/dejavue-image.png" alt="Tasrif">
</p>




## Monitoring of Diplomatic pulse

Diplomatic pulse uses the Scrapy UI, which can be used to observe each crawler job history and status. 

You can access UI at [ http://localhost:5000/1/jobs/ ] using the username and password [SCRAPY_WEB_USERNAME,SCRAPY_WEB_PASSWORD] shown in the .env file.


## Full Documentation
Documentation is available online at  https://diplomaticpulse.qcri.org/docs and in the docs directory.

## Contributing
See https://diplomaticpulse.qcri.org/docs/contributing.html for details.




    



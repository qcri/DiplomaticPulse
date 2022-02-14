
<h1  style="color:DeepSkyBlue;font-size:60px;"align="center">
  <b>Diplomatic Pulse: Crawling, Indexing, and Storage System for United Nations states Member Press statements in Real Time.</b>
</h1>

#


This repository should provide much of the structure and parsing code needed to crawl and scrape various countries's Ministry of Foreign Affairs (MFA) web pages
contents with very little effort.
On launching our Diplomatic pulse scrapy crawlers, the Diplomatic Pulse clones our backend date: xpaths of each country to scrape its web content. 

The websites contents of each country consist of: 

 -`URL: ` link of article's  website.

 -`Title: `  the tile of the article

 -`Posted date: `  Published date of the article

 -`Statement: `the content of the article
 
The scraped data is saved into Elasticsearch database.

##Why Diplomatic Pulse
United Nations states Member Press statements are a primary sources on issues of debate in the UN’s peace and security context.
We have developed the “Diplomatic Pulse” system as search engine service for press statements of the UN’s 193 Member States, 
including their Foreign Ministries and Permanent Missions to the UN.
 Diplomatic Pulse crawls and scrapes all UN Member States websites contents in real time. It is built using free open source 
website crawling technologies ; Scrapy web crawling and web scarping framework to automate data scraping. The scraped contents are
saved and indexed using open source elasticsearch engine. 
The Diplomatic Pulse system is capable of detecting possible scraping detection errors,
it automatically sends alerts via emails

## Country Diplomatic website (Overview) page  
 There is at least one overview page for each country, e.g: Australian: `https://www.foreignminister.gov.au`. 
 One country may have one or many overview pages (multiple URLs).

The crawler visits the country's overview page then scrapes the existing articles links, then follows each link to extract  
its content (title, date posted, statement); the content is saved into an elasticsearch database 

##Diplomatic Pulse Spiders (Crawlers)
The Diplomatic Pulse contains a number of five scrapy spiders (one for each content type) to extract contents from various websites, you can use command `scrapy list` to list all spiders.  
they are:

- `html`  handles static html content 
- `Javascript`  handles dynamic content 
- `doc`  handles PDF and Images contents
- `json` handles json content
- `html_doc` handles mixed html & PDF/Images contents

 One could easily implement a new spider for new content type.




## Country website XPATHs

On launching Diplomatic Pulse containers, the script `setup.sh` creates three Elasticsearch indexes on the fly: `countries`, `urlconfig`, `dppa.st`;
the indicies names are shown in `.env` file abd could be easlily renamed, they are:
- `countries:` list names of countries, and is populated with  the json data in `countries.json`.
- `urlconfig: ` list of URL's xpath configuration, and  is populated with the  data `urlconfig.json`.


the elasticsearch index `countries` contains:
- `name`: name of the country, for example: Australia.
- `status`: complete if all country xpath are valid, else pending.
- `URL counter`: total number of indexed URLs for the country.

the elasticsearch index `urlconfig` contains:
- `name`: name of the country.
- `URL`: country's overview page link.
- `posted date`: published article's xpath.
- `content_type`: content type (spider name)  .
- `global`: html block (which contains title & article link, date posted) xpaths (extracted from overview page).
- `link`: article's link xpath (URL).
- `title`: acticle's title xpath.
- `tag`: Unawanted html element tag's xpath.
- `us_date_format`: US date format if exist.


## Important
Our Diplomatic Pulse spiders depend on the underlying format and structure of each websites's page, and when the website's layout changes  or wrong 
our spiders tend to break. So succesfull running spiders depends heavily on a correct website's XPATH configuration,
therfore if country's website updates its templates then correct XPATHs should be updated respectively.

## Indexing data
On launching Diplomatic Pulse containers, the script `setup.sh` creates an empty index on the fly: `dppa.st`;
There is a one Crawler `Spider instance` for each country's overview page. At the start, the crawler visits country's overview page,
extracts and follows all statements links to  scrape their contents `title, article statement, posted date`.
For each country web page, the contents are extracted and indexed into the Elasticsearch index `dppa.st`

the elasticsearch index `dppa.st` contains:
- `content_type`: website content type(html/dyanimc/json/pdf/image).
- `country`: name of the country (eg: Australia).
- `indexed_date`: indexed timestamp, when the content was indexed.
- `language`: content language.
- `parent_url`: diplomatic country overview webpage URL.
- `posted_date`: published date (date posted) of the article.
- `statement`: content of  the article (statement).
- `title`: title of content of  the article.
- `url`:  URL of the article.

## How to start Diplomatic Pulse  
A docker-compose.yml file is used, once you have Docker installed and started, change to the project directory and follow:
- This is a Scrapy project, so first you need a working Scrapy installation: https://docs.scrapy.org/en/latest/intro/install.html. 
-  clone Diplomatic Pulse code `git@github.com:qcri/DiplomaticPulse.git`
- `docker-compose up`- launch Diplomatic Pulse containers. 
- `docker-compose down` stop running containers. 


## How to use Rotating Proxies

IP rotation using `rotating proxies` library is implemented to take care of possible proxies use. You can use you own proxies as follow:

- add your proxies to `proxy.py` in format "http://username:password@ip:port"
- enable the proxies through `DOWNLOADER_MIDDLEWARES` in `settings.py` :
  `
DOWNLOADER_MIDDLEWARES =
{
    'rotating_proxies.middlewares.RotatingProxyMiddleware': 610,
    'rotating_proxies.middlewares.BanDetectionMiddleware': 620
}
`
  
## Browsing extracted indexed data
Each visited country webpage, the content is extracted and indexed into our elasticsearch index `dppa.st`. 

The indexed data can be browsed using the  `Dejavu` (free and open source web UI for Elasticsearch).

Assuming all containers are running on your local machine, go to:

 - `http://localhost:1358` , running dejavu 
 - connect to index `dppa.st` with  `http://localhost:9200`



##Diplomatic Pulse data quality 
Scraped contents data are checked and cleaned before indexed; Diplomatic Pulse takes care of: 
- `unwanted html element tags`: The scrapy spider middleware is used  to process a response body by removing a (configurable) set of elements from it. 
The unwated tags are set in the `tag` field shown in the urlconfig index.
  
- Spider middleware also guarentees that a content is only indexed once, no duplication allowed.

- `handling various dates formats`: the diplmatic Pulse handles all types of date formats including the US format

- `raise exceptions:` The diplmatic Pulse raises warning   and send it to  index `web_status` when crawler fails to read the content.

##Monitoring of Diplomatic Pulse running Spiders (crawlers) status
To observe  each crawler job history and status, we use the Scrapy UI which running on `port 6800`,  you can browse:

-`http://localhost:6800`

## Prequisites

A running Python and Scrapy installation is mandatory for this project
- `Ubuntu  >= 14.04 `
-` Python3.X, pip3`
- `Scrapy >= 2.xx`







    



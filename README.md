
# Diplomatic pulse 
This repository should provide much of the structure and parsing code needed to crawl various web pages to extract news, released statements published by countries with very little effort.
On launching scrapy crawlers, the diplomatic pulse system clones  our backend data (names and  websites XPATHs of member states of United Nations), extracts then follows all URLs. 

The content of each country's web page which consists of: title, date posted and article content is extracted and saved into Elasticsearch database. 

Dejavu is provided, to allow you to connect to any of the indexes present in our elasticsearch cluster to easily access and browse data.


## Country overview website page  
 There is at least one overview page for each country, e.g: Australian: `https://www.foreignminister.gov.au`. One country may have one or many overview pages (multiple URLs).

The crawler visits the country's overview page then scrapes the existing articles links, then follows each link to extract  its content; 
the content is saved into an elasticsearch database 

##Spiders
This project contains a number of five scrapy spiders to extract contents from various websites, you can use command `scrapy list` to list all spiders. 
One could easily implement a new spider for new content type.

The diplomatic pulse system contains one generic spider for  specific type of content, they are: 
- `html`  handles static html content 
- `Javascript selenium`  handles dynamic content 
- `doc`  handles PDF and Images contents
- `Json` handles json content
- `mixed` handles mixed html & PDF contents

 

Our spiders depend on the underlying format and structure of each websites's pages, and when these are changed  or wrong they tend to break. So succesfull
running spiders depends heavily on a correct websites's XPATH configuration, therfore if country's website updates its templates then correct XPATHs should be updated respectively.




## indexed site's configuration data structure

On launching all containers, the script `setup.sh` creates three Elasticsearch indexes: `countries`, `urlconfig`, `dppa.st`;
indicies names are shown in `.env` file.
- index `countries` is populated with  the `countries.json` data: list names of countries.
- index `urlconfig` is populated with the `urlconfig.json` data:  xpaths
- index `dppa.st` an empty index which to store the extracted article contents data : `[title, content, date posted, date indexed, url, content type, ... ]`

the index `countries` consists of:
- `name`: name of the country, for example: Australia

the index `urlconfig` consists of:
- `name`: name of the country
- `url`: country's overview page link
- `posted date`: published article's xpath
- `content_type`: content type (spider name)  
- `global`: html block (which contains title & link) xpath (extracted from overview page)
- `link`: article's link xpath 
- `title`: acticle's title xpath
- `tag`: Unawanted tag's xpath
- `us_date_format`: US date format if exist


## Indexing data
There is a one Crawler `Spider instance` for each country's overview page. at the start, the crawler visits country's overview page,
extracts and follows all statements links to  scrape their contents `title, article statement, posted date`.
For each country web page, the contents: `title, posted date and the statement content` are extracted and indexed into the Elasticsearch index `dppa.st`

## How to use diplomatic pulse system 
This is a Scrapy project, so first you need a working Scrapy installation: https://docs.scrapy.org/en/latest/intro/install.html. 
The second thing to do is to clone code. 

 A docker-compose.yml file is used, once you have Docker installed and started, change to the project directory and execute:

- `git clone ????` clone diplomatic pulse 
- `docker-compose pull`  -  check for updated images
- `docker-compose up`- launch system contains containers. To stop the containers, enter `docker-compose down` in another shell window.

`docker system prune` will delete the system-wide Docker images, containers, and volumes that are not in use when you want to recover space.

Extracted data will be sent to Elasticsearch cluster index `dppa.st` , see `.env` file.  


## How to use rotating proxies

IP rotation using `rotating proxies` library is implemented to take care of possible proxies use. You can use proxies as follow:

- add your proxies to `proxy.py` (see format)
- enable the proxies through `DOWNLOADER_MIDDLEWARES` in `settings.py` :
  `
DOWNLOADER_MIDDLEWARES =
{
    'rotating_proxies.middlewares.RotatingProxyMiddleware': 610,
    'rotating_proxies.middlewares.BanDetectionMiddleware': 620
}
`
  
## Browsing extracted indexed data
each visited webpage, the  content is extracted and indexed into our elasticsearch index `dppa.st`. 

To browse the data,  we use `Dejavu` (free and open source web UI for Elasticsearch).

Assuming all containers are running on your local machine, you need to visit:

 - http://localhost:1358 , running dejavu 
 - Then, you need to connect to  index `dppa.st` using  `http://localhost:9200`



##Indexed data quality 
Scraped contents data are checked and cleaned before indexing, diplomatic pulse system takes care of: 
- `unwanted html element`: The scrapy spider middleware is used  to process a response body by removing a (configurable) set of elements from it. 
The unwated tags are set in the `tag` field shown in the urlconfig.json.
If tag element exists, then tag element  elements  sre striped from indexed content.
  
- Spider middleware also guarentees that a content is only indexed once, no duplication allowed.

- `handling various dates formats`:
the system handles all types of date formats including the US format

- `raise warning`
The system raises warning   and send it to  index `web_status` when crawler fails to read the content.

##Monitoring all running crawlers status
To observe  each crawler job history and status, we use the Scrapy UI on `port 6800`,  you can browse:
http://localhost:6800/

## Prequisites

A running Python and Scrapy installation is mandatory for this project
- `Ubuntu  >= 14.04 `
-` Python3.X, pip3`
- `Scrapy >= 2.xx`

##Feedback
If you have any problem, feel free to fire issues in Github, I will reply ASAP.





    



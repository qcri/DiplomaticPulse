"""
This module implements a spider to use
for scraping countries articles (static html content),
e.g: https://www.foreignminister.gov.au/ .
"""
from urllib.parse import unquote
import re
from scrapy.selector import Selector

def get_html_response_content(response, xpath):
    """
    This method reads body content from Request response using XPATH method.

    Args:
        response (Request object): response body
        xpath(string): article xpath

    Returns
        text(string): formated html text

    Raises
        Exception: when it catches  error

    """
    try:
        return format_html_text(' '.join(response.xpath(xpath).getall()))
    except Exception:
        return None


def format_html_text(html):
    """
    This method formats html content.

    Args
        html (string):
                article content

    Returns
        text (string):
            formated html text

    Raises
        Exception
            when it catches  error

    """

    try:
        clean_text = re.findall("<p[^>]*>([^<]+)", re.sub("<br>(\\n){0,}", "\n", re.sub("<[/]*[^pb][^>]+>", " ", html)))
        clean_text = re.sub(r"\n{2,}", "\n", '\n'.join(clean_text))
        if not clean_text:
            # check if the element <p> present in html
            clean_text = re.sub("<br>(\\n){0,}", "\n", re.sub("<[/]*[^pb][^>]+>", " ", html))
        clean_text = re.sub("\xa0 {2,}", '', clean_text)
        clean_text = re.sub("\n\s*", '\n', clean_text)
        clean_text = re.sub("\t", "", clean_text)
        clean_text = re.sub("\r", "", clean_text)
        clean_text = re.sub("\xa0", "", clean_text)
        if '\n' not in clean_text:
            clean_text = clean_text.replace('.', '\n')

        return clean_text.strip()
    except Exception:
        return html


def format_html_pdf_text(raw_html):
    """
    This method formats PDF content.

    Args
        html (string):
            PDF article content

    Returns
        text (string):
            formated html text

    """
    try:
        CLEANR = re.compile('<.*?>')
        html = re.sub(CLEANR, '', raw_html)
        html = re.sub('[\n]+', '\n', html)
        html = re.sub('[\t]+', '', html)
        html = re.sub('[\r]+', '', html)
        html = re.sub('[\xa0]+', '', html)
        return html.strip()

    except Exception:
        return raw_html


def get_html_block_links(response, xpaths):
    """
    This method reads Request response - html block for each article (URL).

    Args
        response (Request response):
              response content
        xpaths : dic(json)
            Python dict in the following format:
            xpaths{
                   'global' : <URL global XPATH>
                   'link' : <URL XPATH>>
                   'title' : <title XPATH >
                   'posted_date' : <date posted XPATH >
            }

    Returns
    data : [string]
        data[
            <url>,<title>,<posted_date>
        ]

    """
    try:
        data = []
        html_blocks = response.xpath(xpaths["global"]).getall()
        for html in html_blocks:
            url = Selector(text=html).xpath(xpaths["link"]).get()
            if url is None:
                continue
            url = response.urljoin(url)
            title = Selector(text=html).xpath(xpaths["title"]).get()
            _date = Selector(text=html).xpath(xpaths["posted_date"]).get()
            data.append(dict(url=unquote(url), title=title, posted_date=_date))
        return data
    except Exception:
        return None


def get_title(title, response, xpaths):
    """
    This method scrapes article's title.

    Args
        title (string):
            article title
        response (Request response):
              response content
        xpaths : dict(json)
            Python dict in the following format:
            xpaths{
                'title' : <article  title XPATH >
                }

    Returns
        title : string
             title

    """
    try:
        if title is None:
            title = response.xpath(xpaths).get()
        return title.strip()
    except Exception:
        return title

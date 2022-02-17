"""
This module implements a spider to use
for scraping countries articles (static html content),
e.g: https://www.foreignminister.gov.au/ .
"""
from urllib.parse import unquote
import re
from scrapy.selector import Selector

def get_html_response_content(response, statement_xpath):
    """
    This method reads body content from Request response using XPATH method.

    Args:
        response (Request object): response body
        statement_xpath(string): article xpath

    Returns
        text(string): formated html text

    Raises
        Exception: when it catches  error

    """
    try:
        return " ".join(response.xpath(statement_xpath).getall())
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
        clean_text = re.findall("<p[^>]*>([^<]+)", html)
        clean_text = re.sub(r"\n{2,}", "\n", "\n".join(clean_text))
        if clean_text is None:
            clean_text = re.sub(
                "<br>(\\n){0,}", "\n", re.sub("<[/]*[^pb][^>]+>", " ", html)
            )
        clean_text = "".join(clean_text)
        return clean_text, clean_text if not None else html
    except Exception as ex:
        print("!!!!!!!!!!! ERROR", ex)
        return html


def format_html_pdf_text(html):
    """
    This method formats PDF content.

    Args
        html (string):
            PDF article content

    Returns
        text (string):
            formated html text

    """
    clean_text = re.findall(
        "<p[^>]*>([^<]+)",
        re.sub("<br>(\\n){0,}", "\n", re.sub("<[/]*[^pb][^>]+>", " ", html)),
    )
    if clean_text is None:
        # check html has  <p>
        clean_text = re.sub(
            "<br>(\\n){0,}", "\n", re.sub("<[/]*[^pb][^>]+>", " ", html)
        )
    if clean_text is None:
        clean_text = html

    clean_text = re.sub(r"(\. +)", r" ENDOFPARAGRAPH ", html)
    clean_text = re.sub(r"( *\n *)", r" ", clean_text)
    clean_text = re.sub(r"( *\r *)", r" ", clean_text)
    clean_text = re.sub(r"( *\t *)", r" ", clean_text)
    clean_text = re.sub(r"[0-9]+ +\x0c", "", clean_text)
    clean_text = clean_text.replace("\f", "")
    clean_text = re.sub(r"ENDOFPARAGRAPH", ".\n", clean_text)
    return clean_text


def get_html_block_links(response, xpaths):
    """
    This method reads Request response - html block for eacr article (URL).

    Args
        response (Request response):
              response content
        xpaths : dic(json)
            Python dict in the following format:
            xpaths{
                   'global' : <article global XPATH>
                   'link' : <article URL XPATH>>
                   'title' : <article  title XPATH >
                   'posted_date' : <article  date posted XPATH >
            }

    Returns
    data : []
        data[<url>,<title>,<posted_date>,]

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
    except Exception as ex:
        print("ERROR: ", ex)
        return None


def get_title(title, response, xpaths):
    """
    This method scrapes article title.

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
             article title

    """
    try:
        if title is None:
            title = response.xpath(xpaths["title"]).get()
        return title.strip()
    except Exception:
        return title

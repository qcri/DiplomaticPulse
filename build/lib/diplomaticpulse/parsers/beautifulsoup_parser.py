"""
This module implements beautifulsoup parsing
"""
from urllib.parse import unquote
import time
from bs4 import BeautifulSoup

from diplomaticpulse.parsers import html_parser, dates_parser


def get_soup(url, driver):
    """
    get Beautifulsoup soup object

    Args
        url (string):
            link url
        driver (Selenium driver type):
            driver object

    Returns
        soup(object of beautifulsoup)
    """
    try:
        driver.get(url)
        time.sleep(5)
        soup = BeautifulSoup(driver.page_source, "html.parser")
        return soup
    except Exception as e:
        print("Warming: failed to get Beatifulsoup object for ", e)
        return None


def remove_unwanted_tags(url, driver, xpaths):
    """
    remove unwanted tags element from html content

    Args
          url (string):
              link URL
        driver (Selenium driver):
        xpaths (string):
               unwated elements names

    Returns
         text (string):
            cleaned html text

    """
    try:
        if xpaths is None:
            return None
        soup = get_soup(url, driver)
        elements = xpaths["tags"].split("#")
        for elem in elements:
            tags = elem.split(",")
            if len(tags) > 1:
                for tag in soup.find_all(tags[0], class_=tags[1]):
                    tag.extract()
            else:
                tags_to_delete = soup.find_all(elem)
                for tag in tags_to_delete:
                    tag.extract()
        return soup
    except Exception as e:
        print("WARNING in remove_unwanted_tags: ", str(e))
        return None


def get_data_from_blocks(response, xpaths, driver):
    """
    scrape article  html block (as see in page overview)

    Args
        response (response type):
            page html
        xpaths dict(json):
            xpaths {
                'global' : <page html block XPATH ofr each article>
                'title' : <article's title XPATH>
                'posted_date' : <article's posted date XPATH>
                }
        driver (selenium driver type):
            driver object

    Returns
        res ([]):
            res [<title<,<url>,<link URL>,<posted date>]

    Raises
        Exception
             when it catches an error
    """
    try:
        soup = get_soup(response.url, driver)
        elements = xpaths["global"].split(",")
        raw = soup.find_all(elements[0], class_=elements[1])
        res = []
        for html in raw:
            url = response.urljoin(scrape_url(html, xpaths["link"]))
            title = get_text(html, xpaths["title"])
            date = get_text(html, xpaths["posted_date"])
            res.append(dict(url=unquote(url), title=title, posted_date=date))
        return res
    except Exception:
        return None


def get_data_from_response(response, data, xpaths, driver):
    """
    scrape the page content from response

    Args
        response (response type):
            Request response content
        xpaths dict(json):
            xpaths {
                'global' : <page html block XPATH ofr each article>
                'title' : <article's title XPATH>
                'posted_date' : <article's posted date XPATH>
                }
        driver : selenium driver type
            driver object

    Returns
        text (string):
            formated html content

    Raises
        Exception
             when it catches  error
    """
    try:
        elements = xpaths["statement"].split(",")
        soup = remove_unwanted_tags(response.url, driver, xpaths)
        if soup is None:
            soup = get_soup(response.url, driver)
        raw = soup.find_all(elements[0], class_=elements[1])
        text = []
        for txt in raw:
            text.append(txt.get_text())
        text = "\n".join(text)
    except Exception:
        pass
    finally:
        if text is None:
            text = html_utils.get_response_content(response, xpaths)

        # ger date
        date = data["posted_date"]
        if date is None:
            date = get_text(soup, xpaths["posted_date"])
        else:
            date = dates_parser.get_date(data, response, xpaths)
        return html_utils.format_html_text(text), date


def scrape_url(html, element):
    """scrape  link URL from response content

    Args
        html : response type
                page html
        element : Beautifull soup element ID

    Returns
        text (string)
            link URL
    Raises
        Exception
             when it catches  error

    """
    try:
        dispatcher = {
            "html.a": html_a_,
            "html.span": html_span_,
            "html.h2.a": html_h2_a_,
            "html": html_,
            "html_h3_a": html_h3_a_,
            "html_h6_a": html_h6_a_,
            "html_li_a": html_li_a_,
            "html_li": html_li_,
        }

        text = fire_me(dispatcher[element], html)

        return text
    except Exception:
        pass


def html_a_(html):
    """
    this function scrapes link from html

    Args
        html ( string)

    Returns
        text (string):
            link url
    """
    return html.a["href"]


def html_span_(html):
    """
    this function scrapes link from html

    Args
        html ( string)

    Returns
        text (string):
            link url
    """
    return html.span["href"]


def html_h2_a_(html):
    """
    this function scrapes link from html

    Args
        html ( string)

    Returns
        text (string):
            link url
    """
    return html.h2.a["href"]


def html_(html):
    """
    this function scrapes link from html

    Args
        html ( string)

    Returns
        text (string):
            link url
    """
    return html["href"]


def html_h3_a_(html):
    """
    this function scrapes link from html

    Args
        html ( string)

    Returns
        text (string):
            link url
    """
    return html.h3.a["href"]


def html_h6_a_(html):
    """
    this function scrapes link from html

    Args
        html ( string)

    Returns
        text (string):
            link url
    """
    return html.h6.a["href"]


def html_li_a_(html):
    """this function scrapes link from html

    Args
        html (string)

    Returns
        text: string
            link url
    """
    return html.li.a["href"]


def html_li_(html):
    """
    this function scrapes link from html

    Args
        html ( string)

    Returns
        text (string):
            link url
    """
    return html.li["href"]


def get_text(html, element):
    """
    this function scrapes  html content

    Args
        html (response type):
                page html
        element : beautifull soup element ID

    Returns
        text (string)
            html text

    Raises
        Exception
             when it catches  error

    """
    try:
        dispatcher = {
            "html.text": html_text,
            "html.a": html_a,
            "html.a_span": html_a_span,
            "html.span": html_span,
            "html.h1": html_h1,
            "html.h1_a": html_h1_a,
            "html.h2": html_h2,
            "html.h2_a": html_h2_a,
            "html.h3": html_h3,
            "html.h3_a": html_h3_a,
            "html.h6_a": html_h6_a,
            "html.h4": html_h4,
            "html.h4_a": html_h4_a,
            "strong": strong,
            "html.strong": html_strong,
            "html.time": html_time,
            "html.div": html_div,
            "html.small": html_small,
            "html.li_a": html_li_a,
            "html.li": html_li,
        }

        elements = element.split(",")
        if len(elements) > 1:
            return (html.find(elements[0], class_=elements[1]).text).strip()
        text = fire_me(dispatcher[element], html)
        return text
    except Exception:
        pass


def fire_me(func_name, html):
    """
     call function based on func_name

    Args
        func_list : list of function to call

    Returns
        text (string)
            html text
    """
    return func_name(html)


# below names of function
def html_text(html):
    """
    this function scrapes text from html

    Args
        html (string):
          statement content

    Returns
        text (string):
            html text
    """
    return html.text


def html_a(html):
    """
    this function scrapes text from html

    Args
        html (string):
          statement content

    Returns
        text (string):
            html text
    """
    return html.a.text


def html_a_span(html):
    """
    this function scrapes text from html

    Args
        html (string):
          statement content

    Returns
        text (string):
            html text
    """
    return html.a.span.text


def html_span(html):
    """
    this function scrapes text from html

    Args
        html (string):
          statement content

    Returns
        text (string):
            html text
    """
    return html.span.text


def html_h1(html):
    """
    this function scrapes text from html

    Args
        html (string):
          statement content

    Returns
        text (string):
            html text
    """
    return html.h1.text


def html_h1_a(html):
    return html.h1.a.text


def html_h2(html):
    """
    this function scrapes text from html

    Args
        html (string):
          statement content

    Returns
        text (string):
            html text
    """
    return html.h2.text


def html_h2_a(html):
    """
    this function scrapes text from html

    Args
        html (string):
          statement content

    Returns
        text (string):
            html text
    """
    return html.h2.a.text


def html_h3(html):
    """
    this function scrapes text from html

    Args
        html (string):
          statement content

    Returns
        text (string):
            html text
    """
    return html.h3.text


def html_h3_a(html):
    return html.h3.a.text


def html_h6_a(html):
    """
    this function scrapes text from html

    Args
        html (string):
          statement content

    Returns
        text (string):
            html text
    """
    return html.h6.a.text


def html_h4(html):
    """
    this function scrapes text from html

    Args
        html : string

    Returns
        text: string
            html text
    """
    return html.h4.text


def html_h4_a(html):
    """
    this function scrapes text from html

    Args
        html (string):
          statement content

    Returns
        text (string):
            html text
    """
    return html.h4.a.text


def strong(html):
    """
    this function scrapes text from html

    Args
        html (string):
          statement content

    Returns
        text (string):
            html text
    """
    return html.strong.text


def html_strong(html):
    """
    this function scrapes text from html

    Args
        html (string):
          statement content

    Returns
        text (string):
            html text
    """
    return html.strong.text


def html_time(html):
    """
    this function scrapes text from html

    Args
        html (string):
          statement content

    Returns
        text (string):
            html text
    """
    return html.time.text


def html_div(html):
    """
    this function scrapes text from html

    Args
        html (string):
          statement content

    Returns
        text (string):
            html text
    """
    return html.div.text


def html_small(html):
    """
    this function scrapes text from html

    Args
        html (string):
          statement content

    Returns
        text (string):
            html text
    """
    return html.small.text


def html_li_a(html):
    """
    this function scrapes text from html

    Args
        html (string):
          statement content

    Returns
        text (string):
            html text
    """
    return html.li.a.text


def html_li(html):
    """
    this function scrapes text from html

    Args
        html (string):
          statement content

    Returns
        text (string):
            html text
    """
    return html.li.text

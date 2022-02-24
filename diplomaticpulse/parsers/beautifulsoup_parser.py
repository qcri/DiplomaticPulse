"""
This module implements beautifulsoup object parsing
"""
from urllib.parse import unquote
import time
from bs4 import BeautifulSoup
from diplomaticpulse.parsers import dates_parser, html_parser


def get_text_from_html_block(url, xpaths_html, driver):
    """
    This method scrapes url html block info: URL,date posted,title for each link as seen in the page .
    when it founds URL link, it scrapes the corresponding title and possible posted date.

    Args
        response (response object):
           html content
        xpaths_html dict(json):
            xpaths_html {
                'global' : <tag,id>
                'title' : <title XPATH>
                'posted_date' : <posted date XPATH>
                }
        driver (selenium driver type):
            driver object

    Returns
        url_info dict(json):
            url_info
                 {
                    url: <URL>
                    {
                        posted_date: <date posted>
                        title: <title>
                    }
                 }

    Raises
        Exception
             when it catches generic error
    """

    if "global" not in xpaths_html or "link" not in xpaths_html:
        return None

    elements = xpaths_html["global"].split(",")
    if len(elements) < 2:
        return None

    # get soup
    url_info = []
    soup = get_soup(url, driver)
    title = None
    posted_date = None
    try:
        for rows in soup.find_all(elements[0], class_=elements[1]):
            url = get_url_from_soup(rows, xpaths_html["link"])
            if url is None:
                continue
            if "title" in xpaths_html:
                title = get_text(rows, xpaths_html["title"])
            if "posted_date" in xpaths_html:
                posted_date = get_text(rows, xpaths_html["posted_date"])
            url_info.append(dict(url=unquote(url), title=title, posted_date=posted_date))
        return url_info
    except Exception as ex:
        print("Error occured in get_text_from_html_block", ex)
        return url_info


def get_text_from_html_soup(response, xpaths, driver):
    """
    This method scrapes the page content from soup object.

    Args
        response (response object):
            Request response content
        xpaths (string): <page html XPATH >
        driver : selenium driver type
            driver object

    Returns
        html (string):
            formated html text

    Raises
        Exception
             when it catches  error
    """
    try:
        text = []

        # check  global xpaths
        elements = xpaths.split(",")
        if len(elements) < 2:
            return text

        soup = get_soup(response.url, driver)
        for rows in soup.find_all(elements[0], class_=elements[1]):
            text.append(rows.get_text())
        if text is None:
            text = html_parser.get_html_response_content(response, xpaths)
        return " ".join(text)
    except Exception as ex:
        print("Error occured in get_text_from_html_soup", ex)
        return None


def get_date_from_html_soup(response, data, xpath, driver):
    """
    This method scrapes the posted date from soup object.

    Args
        response (response object):
            Request response content
        xpath (string): <article's posted date XPATH>
                }
        data dic{string}:
            {
            'posted_date' : <string date>
            }

    Returns
        st_date (string):
            string date (posted date)

    """
    str_date = None
    if data and "posted_date" in data:
        str_date = data["posted_date"]

    if str_date is not None or response is None:
        return str_date

    soup = get_soup(response.url, driver)
    str_date = get_text(soup, xpath)
    if str_date is None:
        str_date = dates_parser.get_date(data, response, xpath)

    return str_date


def get_title_from_html_soup(response, title, xpath, driver):
    """
    This method scrapes the title from soup  object.

    Args
        response (response object):
            Request response content
        xpath (string): <title xpath>
        title(string) : text

    Returns
        st_date (string):
            string date (posted date)

    Raises
        Exception
             when it catches  error
    """
    try:
        if title is not None:
            return title
        soup = get_soup(response.url, driver)
        return get_text(soup, xpath)
    except Exception:
        return None


def get_soup(url, driver):
    """
    This methof gets Beautifulsoup soup object of an URL.

    Args
        url (string):
            link url
        driver (Selenium driver type):
            driver object

    Returns
        soup(object of beautifulsoup)

    Raise:
       Exception

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
    Remove unwanted tags element from html content.

    Args
        url (string):link URL
        driver (Selenium driver): driver
        xpaths dict(string):unwanted elements names

    Returns
         text (string):
            cleaned html text

    Raise:
       Exception

    """
    try:
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


def get_url_from_soup(html, element):
    """
    Scrape URL from response content.

    Args
        html : html (Beautifulsoup object):
               html content
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
            "html.a": href_html_a_bs4,
            "html.span": href_html_span_bs4,
            "html.h2.a": href_html_h2_a_bs4,
            "html": href_html_bs4,
            "html_h3_a": href_html_h3_a_bs4,
            "html_h6_a": href_html_h6_a_bs4,
            "html_li_a": href_html_li_a_bs4,
            "html_li": href_html_li_bs4,
        }
        text = fire_me(dispatcher[element], html)
        return text
    except Exception:
        return None


def href_html_a_bs4(html):
    """
    This function scrapes html from Beautifulsoup object using element(html.a["href"]).

    Args
        html (Beautifulsoup object):
             html content

    Returns
        text (string):
            link url
    """
    return html.a["href"]


def href_html_span_bs4(html):
    """
    This function scrapes html from Beautifulsoup object using element(html.span["href"]).

    Args
        html (Beautifulsoup object):
             html content

    Returns
        text (string):
            link url
    """
    return html.span["href"]


def href_html_h2_a_bs4(html):
    """
    This function scrapes html from Beautifulsoup object using element(html.h2.a["href"]).

    Args
       html (Beautifulsoup object):
             html content

    Returns
        text (string):
            link url
    """
    return html.h2.a["href"]


def href_html_bs4(html):
    """
    This function scrapes html from Beautifulsoup object using element(html["href"]).

    Args
        html (Beautifulsoup object):
             html content

    Returns
        text (string):
            link url
    """
    return html["href"]


def href_html_li_a_bs4(html):
    """
    This function scrapes html from Beautifulsoup object using element(html.li.a["href"]).

    Args
       html (Beautifulsoup object):
            html content

    Returns
        text (string):
            link url
    """
    return html.li.a["href"]


def href_html_h3_a_bs4(html):
    """
    This function scrapes html from Beautifulsoup object using element(html.h3.a["href"]).

    Args
       html (Beautifulsoup object):
            html content

    Returns
        text (string):
            link url
    """
    return html.h3.a["href"]


def href_html_h6_a_bs4(html):
    """
    This function scrapes html from Beautifulsoup object using element(html.h6.a["href"]).

    Args
       html (Beautifulsoup object):
            html content

    Returns
        text (string):
            link url
    """
    return html.h6.a["href"]


def href_html_li_a_(html):
    """
    This function scrapes html from Beautifulsoup object using element(html.li.a["href"]).

    Args
        html (Beautifulsoup object):
             html content

    Returns
        text: string
            link url
    """
    return html.li.a["href"]


def href_html_li_bs4(html):
    """
    This function scrapes link  using element(html.li["href"]).

    Args
        html (Beautifulsoup object):
             html content

    Returns
        text (string):
            link url
    """
    return html.li["href"]


def get_text(soup, element):
    """
    This function scrapes html from html Beautifulsoup object.

    Args
        soup (Beautifulsoup object):
             html soup content

        element : beautifull soup element Tag ID

    Returns
        text (string)
            html text

    Raises
        Exception
             when it catches  error

    """
    try:
        dispatcher = {
            "html.text": html_text_bs4,
            "html.a": html_a_bs4,
            "html.a_span": html_a_span_bs4,
            "html.span": html_span_bs4,
            "html.h1": html_h1_bs4,
            "html.h1_a": html_h1_a_bs4,
            "html.h2": html_h2_bs4,
            "html.h2_a": html_h2_a_bs4,
            "html.h3": html_h3_bs4,
            "html.h3_a": html_h3_a_bs4,
            "html.h6_a": html_h6_a_bs4,
            "html.h4": html_h4_bs4,
            "html.h4_a": html_h4_a_bs4,
            "strong": strong_bs4,
            "html.strong": html_strong_bs4,
            "html.time": html_time_bs4,
            "html.div": html_div_bs4,
            "html.small": html_small_bs4,
            "html.li_a": html_li_a_bs4,
            "html.li": html_li_bs4,
        }

        elements = element.split(",")
        if len(elements) > 1:
            return (soup.find(elements[0], class_=elements[1]).text).strip()
        text = fire_me(dispatcher[element], soup)
        return text.strip()
    except Exception:
        return None


def fire_me(func_name, html):
    """
     Call function based on func_name.

    Args
        func_list : list of function to call

    Returns
        text (string)
            html text
    """
    return func_name(html)


# below names of function
def html_text_bs4(html):
    """
    This function scrapes html from Beautifulsoup object using  elt[html].

    Args
         html (Beautifulsoup object):
              html content

    Returns
        text (string):
            html text
    """
    return html.text


def html_h2_bs4(html):
    """
    This function scrapes html from Beautifulsoup object using  elt[html.h2].

    Args
         html (Beautifulsoup object):
              html content

    Returns
        text (string):
            html text
    """
    return html.h2.text


def html_a_bs4(html):
    """
    This function scrapes html from Beautifulsoup object using  elt[]..

    Args
         html (Beautifulsoup object):
              html content

    Returns
        text (string):
            html text
    """
    return html.a.text


def html_a_span_bs4(html):
    """
    This function scrapes html from Beautifulsoup object using  elt[html.a.span]..

    Args
         html (Beautifulsoup object):
              html content

    Returns
        text (string):
            html text
    """
    return html.a.span.text


def html_span_bs4(html):
    """
    This function scrapes html from Beautifulsoup object using  elt[html.span]..

    Args
         html (Beautifulsoup object):
              html content

    Returns
        text (string):
            html text
    """
    return html.span.text


def html_h1_bs4(html):
    """
    This function scrapes html from Beautifulsoup object using  elt[]..

    Args
         html (Beautifulsoup object):
               html content

    Returns
        text (string):
            html text
    """
    return html.h1.text


def html_h1_a_bs4(html):
    """
    This function scrapes html from Beautifulsoup object using  elt[ html.h1.a.text].

    Args
         html (Beautifulsoup object):
              html content

    Returns
        text (string):
            html text
    """
    return html.h1.a.text


def html_h2(html):
    """
    This function scrapes html from Beautifulsoup object using  elt[html.h2.text].

    Args
         html (Beautifulsoup object):
              html content

    Returns
        text (string):
            html text
    """
    return html.h2.text


def html_h2_a_bs4(html):
    """
    This function scrapes html from Beautifulsoup object using  elt[html.h2.a.text].

    Args
         html (Beautifulsoup object):
              html content

    Returns
        text (string):
            html text
    """
    return html.h2.a.text


def html_h3_bs4(html):
    """
    This function scrapes html from Beautifulsoup object using  elt[html.h3.text].

    Args
         html (Beautifulsoup object):
               html content

    Returns
        text (string):
            html text
    """
    return html.h3.text


def html_h3_a_bs4(html):
    return html.h3.a.text


def html_h6_a_bs4(html):
    """
    This function scrapes html from Beautifulsoup object using  elt[html.h3.a.text].

    Args
         html (Beautifulsoup object):
              html content

    Returns
        text (string):
            html text
    """
    return html.h6.a.text


def html_h4_bs4(html):
    """
    This function scrapes html from Beautifulsoup object using  elt[html.h4.text].

    Args
         html (Beautifulsoup object):
              html content

    Returns
        text: string
            html text
    """
    return html.h4.text


def html_h4_a_bs4(html):
    """
    This function scrapes html from Beautifulsoup  using  elt[html.h4.a.text].

    Args
         html (Beautifulsoup object):
              html content

    Returns
        text (string):
            html text
    """
    return html.h4.a.text


def strong_bs4(html):
    """
    This function scrapes html from Beautifulsoup  using  elt[html.strong.text].

     Args
          html (Beautifulsoup object):
               html content

     Returns
         text (string):
             html text
    """
    return html.strong.text


def html_strong_bs4(html):
    """
    This function scrapes html from Beautifulsoup  using  elt[html.strong.text].

    Args
         html (Beautifulsoup object):
               html content

    Returns
        text (string):
            html text
    """
    return html.strong.text


def html_time_bs4(html):
    """
    This function scrapes html from Beautifulsoup  using  elt[html.time.text].

    Args
         html (Beautifulsoup object):
              html content

    Returns
        text (string):
            html text
    """
    return html.time.text


def html_div_bs4(html):
    """
    This function scrapes html from Beautifulsoup  using  elt[html.div.text].

    Args
         html (Beautifulsoup object):
              html content

    Returns
        text (string):
            html text
    """
    return html.div.text


def html_small_bs4(html):
    """
    This function scrapes html from Beautifulsoup  using  elt[ html.small.text].

    Args
        html (Beautifulsoup object):
          statement content

    Returns
        text (string):
            html text
    """
    return html.small.text


def html_li_a_bs4(html):
    """
    This function scrapes html from Beautifulsoup  using  elt[html.li.a.text].

    Args
        html (Beautifulsoup object):
             html content

    Returns
        text (string):
            html text
    """
    return html.li.a.text


def html_li_bs4(html):
    """
    This function scrapes html from Beautifulsoup  using  elt[html.li.text].

    Args
        html (Beautifulsoup object):
             html content

    Returns
        text (string):
            html text
    """
    return html.li.text
